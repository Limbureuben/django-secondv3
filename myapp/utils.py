from sightengine.client import SightengineClient # type: ignore
from django.conf import settings
import os


client = SightengineClient('159894964', 'hN3ySs6WQRKxENgNXgGmZF82RmPxpoLe')

def is_explicit_image(file_path):
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)

    try:
        result = client.check('nudity').set_file(full_path)
        nudity_data = result.get('nudity', {})
        raw_score = nudity_data.get('raw', 0)

        if raw_score > 0.5:
            print(f"[Explicit Check] File: {file_path} | Raw Nudity Score: {raw_score:.2f} 🚫 Not Acceptable")
            return False  # Not acceptable
        else:
            print(f"[Explicit Check] File: {file_path} | Raw Nudity Score: {raw_score:.2f} ✅ Acceptable")
            return True  # Acceptable

    except Exception as e:
        print(f"[Error] Failed to check image for nudity: {e}")
        return False

# client = SightengineClient('159894964', 'hN3ySs6WQRKxENgNXgGmZF82RmPxpoLe')

# def is_explicit_image(file_path):
#     full_path = os.path.join(settings.MEDIA_ROOT, file_path)
#     result = client.check('nudity').set_file(full_path)

#     nudity_data = result.get('nudity', {})
#     raw_score = nudity_data.get('raw', 0)

#     return raw_score > 0.5
