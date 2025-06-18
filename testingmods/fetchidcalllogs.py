import requests

# 1) CONFIGURATION
API_TOKEN    = "61030d2b-50af-4b4e-a7b6-52d9530a6dba"

ASSISTANT_ID = "8c08b468-e8d6-49f4-b04a-55e3f7bc98b3"
BASE_URL     = "https://api.vapi.ai"

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
}

# 2) FUNCTION TO FETCH A SINGLE PAGE OF CALLS
def fetch_calls_page(assistant_id, page=1, limit=1000):
    """
    Fetch one page of calls for an assistant.
    """
    params = {
        "assistantId": assistant_id,
        "page": page,
        "limit": limit,     # max 1000 per page
    }
    resp = requests.get(
        f"{BASE_URL}/calls",
        headers=HEADERS,
        params=params
    )
    resp.raise_for_status()
    return resp.json()  # expected shape: { "calls": [...], "page": n, "total": m }

# 3) PAGINATE THROUGH ALL PAGES
all_calls = []
page = 1

while True:
    data = fetch_calls_page(ASSISTANT_ID, page=page, limit=1000)
    calls = data.get("calls", [])
    if not calls:
        break
    all_calls.extend(calls)
    print(f"Fetched page {page}, {len(calls)} calls")
    page += 1

print(f"\n→ Total calls retrieved: {len(all_calls)}\n")

# 4) OUTPUT OR PROCESS YOUR CALL LOGS
for idx, call in enumerate(all_calls, start=1):
    print(f"{idx:3d}. Call ID: {call['id']} | Started: {call['createdAt']} | Status: {call['status']}")
