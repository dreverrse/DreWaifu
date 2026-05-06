import os
import requests
import base64

STABILITY_API_KEY = os.getenv("STABILITY_API_KEY", "")


def generate_image(prompt, width=512, height=512):
    if not STABILITY_API_KEY:
        return None, "STABILITY_API_KEY belum diset."

    url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image"
    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {
        "text_prompts": [{"text": prompt}],
        "width": width,
        "height": height,
        "samples": 1,
    }
    r = requests.post(url, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()
    image_b64 = data["artifacts"][0]["base64"]
    image_bytes = base64.b64decode(image_b64)
    return image_bytes, None
