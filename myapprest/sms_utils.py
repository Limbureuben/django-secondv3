import requests
from django.conf import settings

def send_sms(phone, message):
    url = 'https://apisms.beem.africa/v1/send'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {settings.BEEM_API_KEY}',  # base64 encoded "apiKey:secret"
    }

    payload = {
        "source_addr": "INFO",
        "schedule_time": "",
        "encoding": "0",
        "message": message,
        "recipients": [
            {"recipient_id": 1, "dest_addr": phone}
        ]
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
