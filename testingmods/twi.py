from twilio.rest import Client

# Replace these with your actual credentials
account_sid = 'AC4068c0ac144ad22670183a44143191c6'
auth_token = '576ba4b3ce0376d6e733b2bd9fba6f4f'
client = Client(account_sid, auth_token)

call = client.calls.create(
    twiml='<Response><Say>Hello from Twilio!</Say></Response>',
    to='+917588708498',  # Verified number
    from_='+14132878258'  # Must be your Twilio number
)

print(call.sid)