import requests
import base64
from django.conf import settings

def send_sms(to_phone, message):
    url = "https://apisms.beem.africa/v1/send"
    
    api_key = settings.BEEM_API_KEY
    secret_key = settings.BEEM_SECRET_KEY
    sender_id = settings.BEEM_SENDER_ID

    credentials = f"{api_key}:{secret_key}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }

    data = {
        "source_addr": sender_id,
        "schedule_time": "",
        "encoding": "0",
        "message": message,
        "recipients": [
            {"recipient_id": "1", "dest_addr": to_phone}
        ]
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()
