from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from serpapi import GoogleSearch

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
    for vendor in req.vendors:
        print("-" * 40)
        print(f"Vendor: {vendor.get('name')}")
        print(f"Address: {vendor.get('address')}")
        print(f"Phone: {vendor.get('phone')}")
        print(f"Location: {vendor.get('lat')}, {vendor.get('lon')}")
    return {
        "message": "Enquiry successfully received",
        "vendor_count": len(req.vendors)
    }

