from dotenv import load_dotenv
import os
import asyncio
import queue

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    openai,
    azure,
    noise_cancellation,
    silero,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from tts_engine import TTSEngine
import main

load_dotenv(".env.local")


instructions = """You are an empathetic coach.
Validate feelings, ask a short clarifying question.
Always answer short and ask followup questions.
"""


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=instructions)


async def entrypoint(ctx: agents.JobContext):
    # --- LiveKit Session ---
    session = AgentSession(
        #=openai.STT(model="gpt-4o-transcribe", detect_language=True),
        #llm=openai.LLM(model="gpt-5-mini", max_completion_tokens=50),
        #tts=openai.TTS(model="gpt-4o-mini-tts", voice="echo"),

        # stt=openai.STT(base_url="http://0.0.0.0:3001/v1", model="Systran/faster-whisper-small"),
        # llm=openai.LLM(base_url="http://134.103.120.127:8080/v1", model="", max_completion_tokens=50 ,api_key="LoL"),
        # tts=openai.TTS(base_url="http://0.0.0.0:8880/v1", model="kokoro", voice="bm_fable"),


        tts=azure.TTS(
            speech_key=os.getenv("AZURE_SPEECH_KEY"),
            speech_region=os.getenv("AZURE_SPEECH_REGION"),
        ),
        stt=azure.STT(
            speech_key=os.getenv("AZURE_SPEECH_KEY"),
            speech_region=os.getenv("AZURE_SPEECH_REGION"),
        ),
        llm=openai.LLM.with_azure(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        ),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    # --- Status events for WebSocket ---
    status_queue: queue.Queue[str] = queue.Queue()

    def status_callback(msg: str):
        status_queue.put(msg)

    # --- TTS Engine (IMPORTANT: session.say) ---
    tts_engine = TTSEngine(
        say_fn=session.say,
        interrupt_fn=session.interrupt,
        status_callback=status_callback,
    )

    # --- Start LiveKit ---
    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # --- Expose to FastAPI ---
    loop = asyncio.get_running_loop()
    main.app.state.loop = loop
    main.app.state.tts_engine = tts_engine
    main.app.state.status_queue = status_queue

    # --- Start FastAPI server ---
    main.start_api_in_thread(
        port=int(os.getenv("TTS_API_PORT", "8000"))
    )

    print("✅ LiveKit Agent gestartet")
    print("🌐 Web UI: http://localhost:8000/web/web_client.html")
    #print("🌐 Web UI: http://localhost:8000/web/frontend.html")
    print("🔊 HTTP API: POST /speak /stop /mute /unmute")

    # --- Initial greeting ---
    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )

    # --- Keep alive ---
    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    agents.cli.run_app(
        agents.WorkerOptions(entrypoint_fnc=entrypoint)
    )
