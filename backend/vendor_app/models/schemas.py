from pydantic import BaseModel
from typing import List, Dict

class SearchRequest(BaseModel):
    query: str
    location: str

class EnquiryRequest(BaseModel):
    product: str
    vendors: List[Dict]
    location: str
