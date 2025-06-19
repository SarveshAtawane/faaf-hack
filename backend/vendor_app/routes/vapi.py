# routes/vapi.py

from fastapi import APIRouter, Request
from db.mongo import db
from datetime import datetime
import json

router = APIRouter()

@router.post("//vapi/webhook")
async def vapi_webhook_listener(request: Request):
    try:
        body = await request.json()

        print(f"\n{'='*80}")
        print(f"📡 [WEBHOOK RECEIVED] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")

        message = body.get('message', {})
        # call = body.get('call', {})

        message_type = message.get('type', 'unknown')
        # call_id = (
        #     call.get('id')
        #     or message.get('callId')
        #     or body.get('callId')
        # )

        print(f"👉 MESSAGE TYPE: {message_type}")
        # print(f"👉 CALL ID: {call_id}")

        # === 1️⃣  Print "CALL ONGOING" when status update ===
        if message_type == 'status-update':
            status = message.get('status')
            if status == 'ongoing':
                print(f"📞 CALL ONGOING...")

        # === 2️⃣  When call ends, print & update DB ===
        if message_type == 'end-of-call-report':
            analysis = message.get('analysis', {})
            summary = analysis.get('summary')
            structured_data = analysis.get('structuredData')
            recording_url = message.get('recordingUrl')
            duration = message.get('duration')
            
            print(f"\n📝 SUMMARY:\n{summary}")
            print(f"\n📊 STRUCTURED DATA:\n{json.dumps(structured_data, indent=2)}")
            print(f"🎙️ RECORDING URL: {recording_url}")
            print(f"⏱️ DURATION: {duration}")
            # print(message.get('call').get('id'))
            print(message.get('recordingUrl'))
            call_id =message.get('call').get('id')
            print(f"👉 CALL ID: {call_id}")
            # ✅  Update the vendor doc containing this call_id
            matched = False
            for collection_name in db.list_collection_names():
                collection = db[collection_name]
                vendor_doc = collection.find_one({"call_ids": call_id})
                if vendor_doc:
                    matched = True
                    update_fields = {
                        "call_summary": summary,
                        "call_status": "Completed",
                        "call_duration": duration,
                        "call_recording": recording_url,
                        "call_transcription": summary,  # optional
                        "structured_data": structured_data,  # ✅ added
                        "timestamp": datetime.utcnow()
                        # "url": recording_url  # optional, if you want to store the URL
                    }
                    collection.update_one(
                        {"_id": vendor_doc["_id"]},
                        {"$set": update_fields}
                    )
                    print(f"✅ Updated vendor doc in `{collection_name}` with call details & structured data.")
                    break

            if not matched:
                print(f"⚠️ No vendor document found with call_id `{call_id}`")

        print(f"{'='*80}\n")
        return {"status": "received", "timestamp": datetime.now().isoformat()}

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return {"status": "error", "message": str(e)}
