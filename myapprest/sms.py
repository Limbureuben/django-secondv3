import requests
import os
import requests
from requests.auth import HTTPBasicAuth

def send_sms(phone, message):
    url = "https://apisms.beem.africa/v1/send"
    data = {
        "source_addr": "ARDHI UN",
        "encoding": 0,
        "message": message,
        "recipients": [
            {
                "recipient_id": 1,
                "dest_addr": phone
            }
        ]
    }
    username = os.environ.get("BEEM_API_KEY")
    password = os.environ.get("BEEM_SECRET_KEY")

    response = requests.post(url, json=data, auth=HTTPBasicAuth(username, password))
    response.raise_for_status()
    return response.json()
