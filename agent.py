from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    openai,
    # deepgram,
    noise_cancellation,
    silero)
from livekit.plugins.turn_detector.multilingual import MultilingualModel

load_dotenv(".env.local")

instructions = """You are an empathetic coach. Validate feelings, ask a short clarifying question. Just be empathetic
Always answer short and ask followup questions"""
class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=instructions)


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt=openai.STT(model="gpt-4o-transcribe", detect_language=True),
        llm=openai.LLM(model="gpt-5-mini", max_completion_tokens=50),
        tts=openai.TTS(model="gpt-4o-mini-tts", voice="echo"),

        # stt=openai.STT(base_url="http://0.0.0.0:3001/v1", model="Systran/faster-whisper-small"),
        # llm=openai.LLM(base_url="http://134.103.120.127:8080/v1", model="", max_completion_tokens=50 ,api_key="LoL"),
        # tts=openai.TTS(base_url="http://0.0.0.0:8880/v1", model="kokoro", voice="bm_fable"),

        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(), 
        ),
    )

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
