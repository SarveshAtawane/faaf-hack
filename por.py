import requests
import json
import uuid

def create_porter_order():
    # API endpoint
    url = "https://pfe-apigw-uat.porter.in/v1/orders/create"
    
    # Headers
    headers = {
        "x-api-key": "659d4aaf-3797-4186-b7c3-2c231f5d0e22",
        "Content-Type": "application/json"
    }
    
    # Generate a unique request ID
    request_id = str(uuid.uuid4())
    
    # Request payload
    payload = {
        "request_id": request_id,
        "delivery_instructions": {
            "instructions_list": [
                {
                    "type": "text",
                    "description": "handle with care"
                }
            ]
        },
        "pickup_details": {
            "address": {
                "apartment_address": "27",
                "street_address1": "Sona Towers",
                "street_address2": "Krishna Nagar Industrial Area",
                "landmark": "Hosur Road",
                "city": "Bengaluru",
                "state": "Karnataka",
                "pincode": "560029",
                "country": "India",
                "lat": 12.935025,
                "lng": 77.609261,
                "contact_details": {
                    "name": "Test Pickup User",
                    "phone_number": "+919999999999"
                }
            }
        },
        "drop_details": {
            "address": {
                "apartment_address": "45",
                "street_address1": "Prestige Tech Park",
                "street_address2": "Kadubeesanahalli",
                "landmark": "Near Marathahalli Bridge",
                "city": "Bengaluru",
                "state": "Karnataka",
                "pincode": "560103",
                "country": "India",
                "lat": 12.934533,
                "lng": 77.690114,
                "contact_details": {
                    "name": "Test Drop User",
                    "phone_number": "+919888888888"
                }
            }
        },
        "additional_comments": "This is a test comment"
    }
    
    try:
        # Make the POST request
        response = requests.post(url, headers=headers, json=payload)
        
        # Print request details
        print("Request Details:")
        print(f"URL: {url}")
        print(f"Request ID: {request_id}")
        print(f"Status Code: {response.status_code}")
        print("-" * 50)
        
        # Print response
        print("Response:")
        if response.headers.get('content-type', '').startswith('application/json'):
            # Pretty print JSON response
            print(json.dumps(response.json(), indent=2))
        else:
            # Print raw text response
            print(response.text)
            
        # Print response headers (optional)
        print("-" * 50)
        print("Response Headers:")
        for key, value in response.headers.items():
            print(f"{key}: {value}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        print(f"Raw response: {response.text}")

if __name__ == "__main__":
    create_porter_order()