import africastalking
import os
from cryptography.fernet import Fernet # type: ignore

# Initialize Africa's Talking
africastalking.initialize(os.getenv("AT_USERNAME"), os.getenv("AT_API_KEY"))
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
