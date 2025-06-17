from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from serpapi import GoogleSearch

app = FastAPI()

# Allow CORS from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    query: str
    location: str

@app.post("/search")
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
        "api_key": "ae8bad07321c4f18db972fe4d3fad8806c65bac32ffb2acd63dd6a27c8fe9f92"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    vendors = []
    for r in results.get("local_results", []):
        vendors.append({
            "name": r.get("title"),
            "address": r.get("address"),
            "phone": r.get("phone", "N/A"),
            "confidence": round(0.75 + 0.25 * len(r.get("address", "")) / 30, 2)
        })
    print(results)
    return {"results": vendors}
