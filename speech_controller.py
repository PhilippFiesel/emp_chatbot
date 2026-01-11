import asyncio

class SpeechController:
    def __init__(self):
        self.current_task = None

    def stop(self):
        if self.current_task and not self.current_task.done():
            self.current_task.cancel()

    def start_async_task(self, coro):
        loop = asyncio.get_running_loop()
        self.stop()
        self.current_task = loop.create_task(coro())
