import requests
import json
from datetime import datetime

# Configuration - Replace with your actual values
API_KEY = "8c4cd1a3-67ab-4449-bdeb-90e8dd4238c4"
BASE_URL = "https://api.vapi.ai"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def get_call_details(call_id):
    """
    Get detailed information about a specific call
    
    Args:
        call_id (str): The ID of the call to retrieve
    
    Returns:
        dict: Complete call data including transcript, analysis, costs, etc.
    """
    try:
        response = requests.get(
            f"{BASE_URL}/call/{call_id}",
            headers=HEADERS
        )
        
        response.raise_for_status()
        call_data = response.json()
        
        print("✅ Call details retrieved successfully!")
        print("=" * 60)
        
        # Basic Call Information
        print(f"📞 Call ID: {call_data.get('id')}")
        print(f"📅 Created: {call_data.get('createdAt')}")
        print(f"🕐 Started: {call_data.get('startedAt')}")
        print(f"🕐 Ended: {call_data.get('endedAt')}")
        print(f"📊 Status: {call_data.get('status')}")
        print(f"📝 End Reason: {call_data.get('endedReason')}")
        print(f"💰 Cost: ${call_data.get('cost', 0)}")
        
        # Customer Information
        if 'customer' in call_data:
            customer = call_data['customer']
            print(f"👤 Customer: {customer.get('name', 'N/A')}")
            print(f"📱 Phone: {customer.get('number', 'N/A')}")
        
        # Call Analysis (if configured)
        if 'analysis' in call_data and call_data['analysis']:
            print("\n🔍 CALL ANALYSIS:")
            print("-" * 40)
            analysis = call_data['analysis']
            for key, value in analysis.items():
                print(f"{key}: {value}")
        
        # Artifacts (structured data you configured)
        if 'artifacts' in call_data and call_data['artifacts']:
            print("\n📋 ARTIFACTS (Structured Data):")
            print("-" * 40)
            for artifact in call_data['artifacts']:
                print(f"Type: {artifact.get('type', 'N/A')}")
                print(f"Content: {json.dumps(artifact.get('content', {}), indent=2)}")
                print()
        
        # Cost Breakdown
        if 'costs' in call_data and call_data['costs']:
            print("\n💰 COST BREAKDOWN:")
            print("-" * 40)
            costs = call_data['costs']
            for service, cost in costs.items():
                print(f"{service}: ${cost}")
        
        return call_data
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to get call details: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return None

def get_call_transcript(call_id):
    """
    Extract and display the transcript from call data
    
    Args:
        call_id (str): The ID of the call
    
    Returns:
        list: Transcript messages
    """
    call_data = get_call_details(call_id)
    
    if not call_data:
        return None
    
    # Look for transcript in different possible locations
    transcript = None
    
    # Check if transcript is in the main call data
    if 'transcript' in call_data:
        transcript = call_data['transcript']
    
    # Check if transcript is in artifacts
    elif 'artifacts' in call_data:
        for artifact in call_data['artifacts']:
            if artifact.get('type') == 'transcript':
                transcript = artifact.get('content')
                break
    
    if transcript:
        print("\n📝 CALL TRANSCRIPT:")
        print("=" * 60)
        
        if isinstance(transcript, list):
            for i, message in enumerate(transcript, 1):
                role = message.get('role', 'unknown')
                content = message.get('content', '')
                timestamp = message.get('timestamp', '')
                
                print(f"{i}. [{role.upper()}] {content}")
                if timestamp:
                    print(f"   Time: {timestamp}")
                print()
        else:
            print(transcript)
    else:
        print("❌ No transcript found for this call")
    
    return transcript

def get_recent_calls(limit=10):
    """
    Get list of recent calls
    
    Args:
        limit (int): Number of calls to retrieve (default: 10)
    
    Returns:
        list: List of recent calls
    """
    try:
        response = requests.get(
            f"{BASE_URL}/call?limit={limit}",
            headers=HEADERS
        )
        
        response.raise_for_status()
        calls_data = response.json()
        
        print(f"✅ Retrieved {len(calls_data)} recent calls")
        print("=" * 60)
        
        for i, call in enumerate(calls_data, 1):
            print(f"{i}. Call ID: {call.get('id')}")
            print(f"   Status: {call.get('status')}")
            print(f"   Created: {call.get('createdAt')}")
            print(f"   Cost: ${call.get('cost', 0)}")
            
            if 'customer' in call:
                customer_name = call['customer'].get('name', 'N/A')
                customer_phone = call['customer'].get('number', 'N/A')
                print(f"   Customer: {customer_name} ({customer_phone})")
            
            print()
        
        return calls_data
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to get recent calls: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return None

def extract_structured_data(call_id):
    """
    Extract only the structured data/artifacts from a call
    
    Args:
        call_id (str): The ID of the call
    
    Returns:
        dict: Structured data extracted from the call
    """
    call_data = get_call_details(call_id)
    
    if not call_data:
        return None
    
    structured_data = {}
    
    # Extract analysis data
    if 'analysis' in call_data and call_data['analysis']:
        structured_data['analysis'] = call_data['analysis']
    
    # Extract artifacts data
    if 'artifacts' in call_data and call_data['artifacts']:
        structured_data['artifacts'] = call_data['artifacts']
    
    # Extract key metrics
    structured_data['metrics'] = {
        'call_id': call_data.get('id'),
        'duration': call_data.get('duration'),
        'cost': call_data.get('cost'),
        'status': call_data.get('status'),
        'end_reason': call_data.get('endedReason'),
        'created_at': call_data.get('createdAt'),
        'started_at': call_data.get('startedAt'),
        'ended_at': call_data.get('endedAt')
    }
    
    # Extract customer info
    if 'customer' in call_data:
        structured_data['customer'] = call_data['customer']
    
    print("\n📊 STRUCTURED DATA EXTRACTED:")
    print("=" * 60)
    print(json.dumps(structured_data, indent=2))
    
    return structured_data

def save_call_data_to_file(call_id, filename=None):
    """
    Save complete call data to a JSON file
    
    Args:
        call_id (str): The ID of the call
        filename (str): Optional filename (default: call_data_CALLID.json)
    """
    call_data = get_call_details(call_id)
    
    if not call_data:
        return None
    
    if not filename:
        filename = f"call_data_{call_id}.json"
    
    try:
        with open(filename, 'w') as f:
            json.dump(call_data, f, indent=2)
        
        print(f"✅ Call data saved to {filename}")
        return filename
        
    except Exception as e:
        print(f"❌ Failed to save file: {e}")
        return None

# Example usage
if __name__ == "__main__":
    print("🚀 Vapi Call Data Retrieval")
    print("=" * 60)
    
    # Replace with an actual call ID from your previous calls
    CALL_ID = "574f5d38-72c0-43bc-915e-e532ee954fa7"
    
    print("Choose an option:")
    print("1. Get call details")
    print("2. Get call transcript")
    print("3. Get recent calls")
    print("4. Extract structured data")
    print("5. Save call data to file")
    
    choice = input("\nEnter your choice (1-5): ")
    
    if choice == "1":
        get_call_details(CALL_ID)
    elif choice == "2":
        get_call_transcript(CALL_ID)
    elif choice == "3":
        get_recent_calls(10)
    elif choice == "4":
        extract_structured_data(CALL_ID)
    elif choice == "5":
        save_call_data_to_file(CALL_ID)
    else:
        print("❌ Invalid choice")
        
    # Or run specific function directly:
    # get_call_details("your_call_id")
    # get_call_transcript("your_call_id")
    # get_recent_calls(5)
    # extract_structured_data("your_call_id")