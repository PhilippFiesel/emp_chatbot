# tts_engine.py
import asyncio
from mute_controller import MuteController
from speech_controller import SpeechController

class TTSEngine:
    def __init__(self, say_fn, interrupt_fn, status_callback=None):
        """
        say_fn: async function provided by AgentSession (session.say)
        """
        self.say_fn = say_fn
        self.interrupt_fn = interrupt_fn
        self.status_callback = status_callback

        self.mute_controller = MuteController()
        self.speech_controller = SpeechController()

        self.mute_controller.add_listener(self._on_mute_change)

    def _on_mute_change(self, muted: bool):
        if muted:
            self.stop()

    async def speak(self, text: str):
        if self.mute_controller.is_muted():
            if self.status_callback:
                self.status_callback("SPEAK_SKIPPED_MUTED")
            return

        # 1️⃣ Stop lokale Task
        self.speech_controller.stop()

        # 2️⃣ Interrupt LiveKit (SYNC!)
        try:
            self.interrupt_fn()
        except Exception as e:
            print("[TTS] interrupt error:", e)

        # 3️⃣ WICHTIG: 1 Tick warten
        await asyncio.sleep(0)

        async def run():
            try:
                if self.status_callback:
                    self.status_callback("SPEAK_START")

                print(f"🗣️ TTS: {text}")

                # 4️⃣ Jetzt spricht er wieder zuverlässig
                await self.say_fn(text)

            except asyncio.CancelledError:
                print("⛔ TTS abgebrochen")
            except Exception as e:
                print("[TTS ERROR]", e)
            finally:
                if self.status_callback:
                    self.status_callback("SPEAK_END")

        self.speech_controller.start_async_task(run)

    def stop(self):
        def stop(self):
            self.speech_controller.stop()
            try:
                self.interrupt_fn()
            except Exception:
                pass

    def mute(self):
        self.mute_controller.mute()

    def unmute(self):
        self.mute_controller.unmute()
