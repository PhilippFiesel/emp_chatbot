from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from unity_connector import UnityConversationConnector


app = FastAPI()
unity_connector = UnityConversationConnector()

# Deploy Web UI
app.mount("/web", StaticFiles(directory="web"), name="web")

@app.post("/emotion")
async def set_emotion(request: Request):
    body = await request.json()
    emotion_id = body.get("emotion")

    emotion_map = {
        "emotion-happy": ("happy", 70),
        "emotion-sad": ("sad", 70),
        "emotion-angry": ("angry", 90),
        "emotion-neutral": ("neutral", 50),
    }

    emotion, value = emotion_map.get(emotion_id, ("neutral", 50))

    unity_connector.send_emotion(
        emotion=emotion,
        value=value,
        text=""  
    )

    print("Emotion-only → UNITY:", emotion)
    return JSONResponse({"status": "emotion sent"}, status_code=200)

@app.post("/speak")
async def speak(request: Request):
    body = await request.json()

    text = body.get("text", "").strip()
    emotion_id = body.get("emotion")

    if not text:
        return JSONResponse(
            {"error": "text missing"},
            status_code=400
        )

    print("WEB → PYTHON:", repr(text), emotion_id)

    # Emotion-Mapping (Web -> Unity)
    emotion_map = {
        "emotion-happy": ("happy", 70),
        "emotion-sad": ("sad", 70),
        "emotion-angry": ("angry", 90),
        "emotion-neutral": ("neutral", 50),
        None: ("neutral", 50),
    }

    emotion, value = emotion_map.get(
        emotion_id,
        ("neutral", 50)
    )

    unity_connector.send_emotion(
        emotion=emotion,
        value=value,
        text=text
    )

    return JSONResponse(
        {"status": "sent to unity"},
        status_code=200
    )

@app.post("/mute")
async def mute():
    unity_connector.send_mute(True)
    return JSONResponse({"status": "muted"}, status_code=200)


@app.post("/unmute")
async def unmute():
    unity_connector.send_mute(False)
    return JSONResponse({"status": "unmuted"}, status_code=200)


if __name__ == "__main__":
    print("Python → Unity Bridge gestartet")
    print("Web UI: http://localhost:8000/web/web_client.html")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
