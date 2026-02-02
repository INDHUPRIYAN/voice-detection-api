import base64, requests, json

def test_api(mp3_path, lang):
    with open(mp3_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

    payload = {
        "language": lang,
        "audioFormat": "mp3",
        "audioBase64": b64
    }

    headers = {
        "x-api-key": "sk_test_123456789",
        "Content-Type": "application/json"
    }

    r = requests.post(
        "http://127.0.0.1:8000/api/voice-detection",
        headers=headers,
        json=payload
    )

    print(r.json())

test_api("dataset/ai/ai_data  (103).mp3", "Tamil")
