from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime

app = FastAPI()

@app.post("/vapi/webhook")
async def vapi_webhook(request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}

    message_type = data.get("message", {}).get("type", "unknown")
    print(f"📡 VAPI WEBHOOK: type={message_type}")

    if message_type == "end-of-call-report":
        print(f"✅ End of call: {data.get('message', {}).get('analysis', {}).get('summary')}")
    elif message_type == "function-call":
        print(f"✅ Function call: {data.get('message', {})}")
    else:
        print(f"⚠️ Unknown message type: {message_type}")

    # REQUIRED: Vapi wants this format
    return JSONResponse(
        content={
            "status": "received",
            "timestamp": datetime.utcnow().isoformat()
        },
        status_code=200
    )
