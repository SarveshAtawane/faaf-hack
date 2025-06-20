from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PORTER_API_URL = "https://pfe-apigw-uat.porter.in/v1/get_quote"
PORTER_API_KEY = "659d4aaf-3797-4186-b7c3-2c231f5d0e22"

@app.post("/api/get-quote")
async def get_quote(request: Request):
    try:
        body = await request.json()
        print("Received request to get quote")
        print("Request body:", body)

        # Fix the customer field structure
        if "customer" in body and isinstance(body["customer"].get("phone"), str):
            number = body["customer"]["phone"]
            body["customer"]["mobile"] = {
                "country_code": "+91",
                "number": number
            }
            del body["customer"]["phone"]

        response = requests.get(
            PORTER_API_URL,
            headers={
                "X-API-KEY": PORTER_API_KEY,
                "Content-Type": "application/json"
            },
            json=body  # sending JSON in GET, like your curl
        )

        print("Response from Porter API:", response.status_code)
        print("Porter response body:", response.text)

        try:
            return JSONResponse(status_code=response.status_code, content=response.json())
        except ValueError:
            return JSONResponse(status_code=response.status_code, content={"error": response.text})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
