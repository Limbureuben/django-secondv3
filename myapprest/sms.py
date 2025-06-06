import requests
import os

def send_sms(to_number, message):
    api_url = 'https://apisms.beem.africa/v1/send'
    api_key = os.getenv('BEEM_API_KEY')
    secret_key = os.getenv('BEEM_SECRET_KEY')
    sender_id = os.getenv('BEEM_SENDER_ID')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {api_key}:{secret_key}'
    }

    payload = {
        'source_addr': sender_id,
        'encoding': 0,
        'schedule_time': '',
        'message': message,
        'recipients': [{'recipient_id': 1, 'dest_addr': to_number}]
    }

    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
