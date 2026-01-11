class MuteController:
    def __init__(self):
        self._muted = False
        self._listeners = []

    def add_listener(self, fn):
        self._listeners.append(fn)

    def mute(self):
        self._muted = True
        for fn in self._listeners:
            fn(True)

    def unmute(self):
        self._muted = False
        for fn in self._listeners:
            fn(False)

    def is_muted(self):
        return self._muted
