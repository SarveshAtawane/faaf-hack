import requests
import json

# Configuration - Replace with your actual values
API_KEY = "61030d2b-50af-4b4e-a7b6-52d9530a6dba"
ASSISTANT_ID = "8c08b468-e8d6-49f4-b04a-55e3f7bc98b3"
PHONE_NUMBER_ID = "db8341b3-e89e-441f-8f16-4fd514700d65"
CUSTOMER_PHONE = "+917588708498"  # Customer's phone number

# API endpoint and headers
BASE_URL = "https://api.vapi.ai"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def create_simple_outbound_call():
    """
    Create a simple outbound call without any overrides
    """
    payload = {
        "type": "outboundPhoneCall",
        "assistantId": ASSISTANT_ID,
        "phoneNumberId": PHONE_NUMBER_ID,
        "customer": {
            "number": CUSTOMER_PHONE
        },
        "name": "Simple Outbound Call"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/call",
            headers=HEADERS,
            json=payload
        )
        
        response.raise_for_status()  # Raise exception for bad status codes
        result = response.json()
        
        print("✅ Simple call created successfully!")
        print(f"Call ID: {result.get('id')}")
        print(f"Status: {result.get('status')}")
        print(f"Type: {result.get('type')}")
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to create call: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return None

def create_outbound_call_with_overrides():
    """
    Create an outbound call with assistant overrides (dynamic variables)
    """
    payload = {
        "type": "outboundPhoneCall",
        "assistantId": ASSISTANT_ID,
        "phoneNumberId": PHONE_NUMBER_ID,
        "customer": {
            "number": CUSTOMER_PHONE,
        },
        "name": "Personalized Outbound Call",
        "assistantOverrides": {
            # Dynamic variables that can be used in your assistant's prompts
            "variableValues": {
                "product_name": "BLue Tulip Flowers",
                "store_name": "Floral farm",
                "location": "HSR",
                "date": "2023-10-01",
                "time": "10:00 AM",

            }
        }
    }

    try:
        response = requests.post(
            f"{BASE_URL}/call",
            headers=HEADERS,
            json=payload
        )
        
        response.raise_for_status()
        result = response.json()
        
        print("✅ Call with overrides created successfully!")
        print(f"Call ID: {result.get('id')}")
        print(f"Status: {result.get('status')}")
        print(f"Customer: {result.get('customer', {}).get('name')}")
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to create call with overrides: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return None

# Main execution
if __name__ == "__main__":
    # print("🚀 Starting Vapi Call Creation...")
    # print("=" * 50)
    
    # # Test 1: Simple call without overrides
    # print("\n1️⃣ Creating simple outbound call...")
    # simple_call = create_simple_outbound_call()
    
    # print("\n" + "=" * 50)
    
    # Test 2: Call with overrides
    print("\n2️⃣ Creating outbound call with overrides...")
    override_call = create_outbound_call_with_overrides()
    
    print("\n" + "=" * 50)
    print("✨ Done!")