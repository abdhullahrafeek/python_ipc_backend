from .stream_state import StreamState

class SharedState:
    def __init__(self):
        self._streams: dict[str, StreamState] = {}

    def register_stream(self, name: str, type: str):
        stream = StreamState(name, type)
        self._streams[name] = stream
        return stream

    def get_streams(self):
        return self._streams