# main.py
import threading
import queue
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from unity_connector import UnityConversationConnector


app = FastAPI()
unity_connector = UnityConversationConnector()

# Mount /web -> ./web/
app.mount("/web", StaticFiles(directory="web"), name="web")

# Will be injected from agent.py:
# app.state.loop = ...
# app.state.tts_engine = ...
# app.state.status_queue = ...
"""
@app.post("/speak")
async def speak(request: Request):
    body = await request.json()
    text = body.get("text", "")
    if not text:
        return JSONResponse({"error": "text missing"}, status_code=400)

    tts_engine = getattr(app.state, "tts_engine", None)
    loop = getattr(app.state, "loop", None)

    if not tts_engine or not loop:
        return JSONResponse({"error": "server not ready"}, status_code=503)

    asyncio.run_coroutine_threadsafe(tts_engine.speak(text), loop)
    return JSONResponse({"status": "accepted"}, status_code=202)
"""
@app.post("/speak")
async def speak(request: Request):
    body = await request.json()
    text = body.get("text", "")
    emotion_id = body.get("emotion")

    if not text:
        return JSONResponse({"error": "text missing"}, status_code=400)

    # --- Emotion → Unity (ALT-KOMPATIBEL) ---
    emotion_map = {
        "emotion-happy": ("happy", 70),
        "emotion-sad": ("sad", 40),
        "emotion-angry": ("angry", 90),
    }

    if emotion_id in emotion_map:
        emotion, value = emotion_map[emotion_id]
        unity_connector.send_emotion(emotion, value)

    # --- TTS ---
    tts_engine = getattr(app.state, "tts_engine", None)
    loop = getattr(app.state, "loop", None)

    if not tts_engine or not loop:
        return JSONResponse({"error": "server not ready"}, status_code=503)

    asyncio.run_coroutine_threadsafe(
        tts_engine.speak(text),
        loop
    )

    return JSONResponse({"status": "accepted"}, status_code=202)

@app.post("/stop")
async def stop():
    tts_engine = getattr(app.state, "tts_engine", None)
    loop = getattr(app.state, "loop", None)

    if not tts_engine or not loop:
        return JSONResponse({"error": "server not ready"}, status_code=503)

    loop.call_soon_threadsafe(tts_engine.stop)
    return JSONResponse({"status": "stopped"})


@app.post("/mute")
async def mute():
    tts_engine = getattr(app.state, "tts_engine", None)
    loop = getattr(app.state, "loop", None)

    if not tts_engine or not loop:
        return JSONResponse({"error": "server not ready"}, status_code=503)

    loop.call_soon_threadsafe(tts_engine.mute)
    return JSONResponse({"status": "muted"})


@app.post("/unmute")
async def unmute():
    tts_engine = getattr(app.state, "tts_engine", None)
    loop = getattr(app.state, "loop", None)

    if not tts_engine or not loop:
        return JSONResponse({"error": "server not ready"}, status_code=503)

    loop.call_soon_threadsafe(tts_engine.unmute)
    return JSONResponse({"status": "unmuted"})


@app.websocket("/ws/events")
async def ws_events(ws: WebSocket):
    await ws.accept()

    status_queue: queue.Queue = getattr(app.state, "status_queue", None)
    if status_queue is None:
        await ws.send_json({"error": "status_queue missing"})
        await ws.close()
        return

    try:
        while True:
            status = await asyncio.to_thread(status_queue.get)
            await ws.send_json({"event": status})
    except WebSocketDisconnect:
        return


def run_api_server(host="0.0.0.0", port=8000):
    uvicorn.run("main:app", host=host, port=port, log_level="info")


def start_api_in_thread(host="0.0.0.0", port=8000):
    thread = threading.Thread(target=run_api_server, kwargs={"host": host, "port": port}, daemon=True)
    thread.start()
    return thread
