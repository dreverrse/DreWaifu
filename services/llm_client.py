import requests


def send_request(url, headers, payload, timeout=60):
    r = requests.post(url=url, headers=headers, json=payload, timeout=timeout)
    r.raise_for_status()
    return r.json()
