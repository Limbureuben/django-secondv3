# utils.py
from sightengine.client import SightengineClient # type: ignore
from django.conf import settings
import os

# Use your real keys here or store in settings
client = SightengineClient('your_api_user', 'your_api_secret')

def is_explicit_image(file_path):
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    result = client.check('nudity').set_file(full_path)

    nudity_data = result.get('nudity', {})
    raw_score = nudity_data.get('raw', 0)

    # You can adjust the threshold (0.5 = 50%)
    return raw_score > 0.5
