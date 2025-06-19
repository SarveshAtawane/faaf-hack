from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from serpapi import GoogleSearch
from pymongo import MongoClient
import hashlib
# MongoDB connection
client = MongoClient("mongodb://localhost:27017")  # adjust if using Atlas or remote
db = client["vendor_db"]
collection = db["vendors"]
from datetime import datetime

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Models
# -----------------------------
class SearchRequest(BaseModel):
    query: str
    location: str

class EnquiryRequest(BaseModel):
    product: str
    vendors: List[Dict]
    location: str

# -----------------------------
# Search API
# -----------------------------
@app.post("/search")
def search_vendors(req: SearchRequest):
    # Parse lat/lon
    if "," in req.location:
        lat, lng = req.location.split(",")
        ll = f"@{lat.strip()},{lng.strip()},16z"
    else:
        ll = "@19.9940148,73.804693,16z"  # default fallback

    params = {
        "engine": "google_maps",
        "q": req.query,
        "ll": ll,
        "api_key": "ae8bad07321c4f18db972fe4d3fad8806c65bac32ffb2acd63dd6a27c8fe9f92"  # replace with your key
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    vendors = []
    for r in results.get("local_results", []):
        print(r)
        print(" - "*50)
        phone = r.get("phone")
        if phone:  # filter only those with phone number
            print(r.get("title"), r.get("address"), phone, r.get('gps_coordinates')['latitude'], r.get('gps_coordinates')['longitude'])
            vendors.append({
                "name": r.get("title"),
                "address": r.get("address"),
                "phone": phone,
                "lat": r.get('gps_coordinates')['latitude'],
                "lon": r.get('gps_coordinates')['longitude']
            })

    return {"results": vendors}

# -----------------------------
# Enquiry API
# -----------------------------
@app.post("/enquire")
def send_enquiry(req: EnquiryRequest):
    print(f"Enquiry for product: {req.product}")
    inserted_ids = []

    for vendor in req.vendors:
        # Create a unique hash index (store name + lat + lon)
        unique_key = hashlib.md5(f"{vendor.name}_{vendor.lat}_{vendor.lon}".encode()).hexdigest()

        # Create document
        vendor_doc = {
            "_id": unique_key,
            "product": req.product,
            "location_bucket": f"{vendor.lat},{vendor.lon}",
            "name": vendor.name,
            "address": vendor.address,
            "phone": vendor.phone,
            "availability": None,
            "price": None,
            "variants": [],
            "alternatives": [],
            "min_availability_time": None,
            "call_summary": None,
            "timestamp": datetime.utcnow(), # current UTC time
            "call_status": "pending",  # initial status
        }


        # Insert or update (upsert)
        result = collection.update_one(
            {"_id": unique_key},
            {"$set": vendor_doc},
            upsert=True
        )

        inserted_ids.append(unique_key)

    return {
        "message": "Enquiry stored in MongoDB",
        "inserted": inserted_ids,
        "vendor_count": len(inserted_ids)
    }
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

@app.get("/enquiries")
def get_all_enquiries():
    # Fetch all documents from MongoDB
    documents = list(collection.find({}))

    # Convert ObjectId and datetime to JSON-friendly format
    for doc in documents:
        doc["_id"] = str(doc["_id"])  # keep hash string
        if "timestamp" in doc:
            doc["timestamp"] = doc["timestamp"].isoformat()

    return JSONResponse(content={"enquiries": documents})
