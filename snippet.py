import base64

with open("dataset/human/human (11).mp3", "rb") as f:
    encoded = base64.b64encode(f.read()).decode("utf-8")

print(encoded)
