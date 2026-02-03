import base64
import tempfile
import os
import joblib
import numpy as np
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from utils_audio import extract_features_from_file

app = FastAPI(title="AI Generated Voice Detection API")

# Load model
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

# API key from environment
API_KEY = os.getenv("API_KEY")

SUPPORTED_LANGUAGES = [
    "Tamil",
    "English",
    "Hindi",
    "Malayalam",
    "Telugu"
]

class AudioRequest(BaseModel):
    language: str
    audioFormat: str
    audioBase64: str

@app.get("/")
def health():
    return {
        "status": "ok",
        "message": "AI Generated Voice Detection API running"
    }

@app.post("/api/voice-detection")
def detect_voice(request: AudioRequest, x_api_key: str = Header(None)):

    # 🔐 API Key Validation
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # 🌍 Language Validation
    if request.language not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail="Unsupported language")

    # 🎧 Audio format validation
    if request.audioFormat.lower() != "mp3":
        raise HTTPException(status_code=400, detail="Only MP3 format supported")

    # Decode Base64
    try:
        audio_bytes = base64.b64decode(request.audioBase64)
    except:
        raise HTTPException(status_code=400, detail="Invalid Base64 audio")

    # Save temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(audio_bytes)
        temp_path = tmp.name

    try:
        features = extract_features_from_file(temp_path)

        if features is None:
            raise HTTPException(status_code=400, detail="Audio too short or corrupted")

        features = scaler.transform([features])
        prediction = model.predict(features)[0]
        prob = model.predict_proba(features)[0]

        confidence = float(np.max(prob))

        if prediction == 1:
            classification = "AI_GENERATED"
            explanation = "Synthetic speech patterns detected"
        else:
            classification = "HUMAN"
            explanation = "Natural variations found in speech"

        return {
            "status": "success",
            "language": request.language,
            "classification": classification,
            "confidenceScore": round(confidence, 2),
            "explanation": explanation
        }

    finally:
        os.remove(temp_path)
