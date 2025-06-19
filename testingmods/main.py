from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import json
import uvicorn

app = FastAPI(
    title="Vapi.ai Webhook Listener",
    description="Listens to Vapi.ai webhooks and prints final call info",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("//vapi/webhook")
async def vapi_webhook_listener(request: Request):
    try:
        body = await request.json()

        print(f"\n{'='*80}")
        print(f"📡 [WEBHOOK RECEIVED] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")

        message = body.get('message', {})
        call = body.get('call', {})

        message_type = message.get('type', 'unknown')
        call_id = (
                call.get('id')
                or message.get('callId')
                or body.get('callId')
            )

        print(f"👉 MESSAGE TYPE: {message_type}")
        print(f"👉 CALL ID: {call_id}")

        # === 1️⃣  Print "CALL ONGOING" when status update ===
        if message_type == 'status-update':
            status = message.get('status')
            if status == 'ongoing':
                print(f"📞 CALL ONGOING...")

        # === 2️⃣  When call ends, print summary + structured + recording link ===
        if message_type == 'end-of-call-report':
           

            analysis = message.get('analysis', {})
            summary = analysis.get('summary')
            structured_data = analysis.get('structuredData')

            # Recording link can be in call or message artifact
  

            print(f"\n📝 SUMMARY:\n{summary}")
            print(f"\n📊 STRUCTURED DATA:\n{json.dumps(structured_data, indent=2)}")
            print(message.get('call').get('id'))
            print(message.get('recordingUrl'))

        print(f"{'='*80}\n")
        return {"status": "received", "timestamp": datetime.now().isoformat()}

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return {"status": "error", "message": str(e)}


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "message": "Webhook listener is running"
    }

@app.get("/")
async def root():
    return {
        "message": "Vapi.ai Webhook Listener is running!",
        "webhook_url": "/vapi-webhook",
        "health_check": "/health",
        "docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
