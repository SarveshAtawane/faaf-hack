from fastapi import APIRouter
from models.schemas import SearchRequest
from serpapi import GoogleSearch

router = APIRouter()

@router.post("/search")
def search_vendors(req: SearchRequest):
    if "," in req.location:
        lat, lng = req.location.split(",")
        ll = f"@{lat.strip()},{lng.strip()},16z"
    else:
        ll = "@19.9940148,73.804693,16z"

    params = {
        "engine": "google_maps",
        "q": req.query,
        "ll": ll,
        "api_key": "ae8bad07321c4f18db972fe4d3fad8806c65bac32ffb2acd63dd6a27c8fe9f92"  # put this in .env or config
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    vendors = []
    for r in results.get("local_results", []):
        phone = r.get("phone")
        if phone:
            vendors.append({
                "name": r.get("title"),
                "address": r.get("address"),
                "phone": phone,
                "lat": r.get("gps_coordinates")['latitude'],
                "lon": r.get("gps_coordinates")['longitude']
            })

    return {"results": vendors}
