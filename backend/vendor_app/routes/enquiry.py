from fastapi import APIRouter
from models.schemas import EnquiryRequest
from db.mongo import db
from datetime import datetime
import hashlib
# from ./utils.vapi_utils import call_vendor  # ✅ your util

router = APIRouter()

@router.post("/enquire")
def send_enquiry(req: EnquiryRequest):
    normalized_location = req.location.replace(" ", "")
    collection_name = f"{req.product}_{normalized_location}"
    collection = db[collection_name]

    inserted = []
    calls = []

    for vendor in req.vendors:
        unique_key = hashlib.md5(f"{vendor['name']}_{vendor['lat']}_{vendor['lon']}".encode()).hexdigest()

        # 1️⃣ Create base vendor doc if not present
        vendor_doc = {
            "_id": unique_key,
            "product": req.product,
            "location_bucket": f"{vendor['lat']},{vendor['lon']}",
            "name": vendor['name'],
            "address": vendor['address'],
            "phone": vendor['phone'],
            "availability": None,
            "price": None,
            "variants": [],
            "alternatives": [],
            "min_availability_time": None,
            "call_summary": None,
            "timestamp": datetime.utcnow(),
            "call_status": "Calling",
            "call_attempts": 0,
            "is_retry": False,
            "call_duration": None,
            "call_recording": None,
            "call_transcription": None,
            "location": {
                "lat": vendor['lat'],
                "lon": vendor['lon']
            },
            "remarks": "",
            # ✅ new field: call_ids array
            "call_ids": []
        }

        # 2️⃣ Upsert base doc if not present (existing doc won't overwrite call_ids)
        collection.update_one(
            {"_id": unique_key},
            {"$setOnInsert": vendor_doc},
            upsert=True
        )

        inserted.append(unique_key)

        # 3️⃣ Call the vendor using Vapi

        call_result = call_vendor(vendor, req.product, req.location)
        calls.append(call_result)

        # 4️⃣ If we got a call_id, push it to the doc's call_ids list
        call_id = call_result.get("call_id")
        if call_id:
            collection.update_one(
                {"_id": unique_key},
                {"$push": {"call_ids": call_id}}
            )

    return {
        "message": f"{len(inserted)} vendors processed in `{collection_name}`",
        "inserted": inserted,
        "calls": calls
    }

from fastapi.responses import JSONResponse

@router.get("/enquiries")
def get_all_enquiries():
    all_docs = []

    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        documents = list(collection.find({}))

        for doc in documents:
            doc["_id"] = str(doc["_id"])
            if "timestamp" in doc:
                doc["timestamp"] = doc["timestamp"].isoformat()
            doc["__collection__"] = collection_name  # useful for frontend/debugging

        all_docs.extend(documents)

    return JSONResponse(content={"enquiries": all_docs})










# to be put in a separate file utils/vapi_utils.py




import requests
import json

# === VAPI CONFIG ===
API_KEY = "8c4cd1a3-67ab-4449-bdeb-90e8dd4238c4"
ASSISTANT_ID = "98d8ba6f-d6e0-4e72-8100-d095a976c474"
PHONE_NUMBER_ID = "d4dfe093-298f-4033-90b6-27602eff8ef4"

BASE_URL = "https://api.vapi.ai"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def call_vendor(vendor: dict, product_name: str, location: str) -> dict:
    """
    Call a single vendor using Vapi with assistant overrides.
    """

    customer_phone = "+919527699807"  # This should ideally come from the request or be dynamically set
    vendor_name = vendor.get("name")
    vendor_name = str(vendor_name).strip()  # Ensure no leading/trailing spaces
    print(f"📞 Initiating call to {vendor_name}...")
    payload = {
        "type": "outboundPhoneCall",
        "assistantId": ASSISTANT_ID,
        "phoneNumberId": PHONE_NUMBER_ID,
        "customer": {
            "number": customer_phone
        },
        "name": "Enquiry ",
        "assistantOverrides": {
            "variableValues": {
                "product_name": product_name,
                "store_name": vendor_name,
                "location": location,
                "is_retry": False
            }
        }
    }

    try:
        response = requests.post(
            f"{BASE_URL}/call",
            headers=HEADERS,
            json=payload,
            timeout=30
        )

        response.raise_for_status()
        result = response.json()

        print(f"✅ Call initiated to {vendor_name} ({customer_phone}) | Call ID: {result.get('id')}")
        return {
            "vendor": vendor_name,
            "phone": customer_phone,
            "call_id": result.get("id"),
            "status": result.get("status")
        }

    except requests.exceptions.RequestException as e:
        print(json.dumps(payload, indent=2))

        print(f"❌ Failed to call {vendor_name}: {e}")
        if hasattr(e, "response") and e.response:
            print(f"Response: {e.response.text}")
        return {
            "vendor": vendor_name,
            "phone": customer_phone,
            "error": str(e)
        }
