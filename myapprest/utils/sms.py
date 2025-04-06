import africastalking
import os
from cryptography.fernet import Fernet # type: ignore

# Initialize Africa's Talking
africastalking.initialize(os.getenv("sandbox"), os.getenv("atsk_ce5403b17335ff50b7e5d3b5a10469710fc73853a932daf7523692084de1911d196e23f3"))
sms = africastalking.SMS

# Decrypt phone number
FERNET_KEY = os.getenv("FERNET_KEY")
fernet = Fernet(FERNET_KEY)

def send_confirmation_sms(encrypted_phone_number, reference_number):
    try:
        phone_number = fernet.decrypt(encrypted_phone_number.encode()).decode()
        message = f"Your report with reference number {reference_number} has been confirmed and processed. Thank you!"
        sms.send(message, [phone_number])
        return True
    except Exception as e:
        print(f"Failed to send SMS: {e}")
        return False
