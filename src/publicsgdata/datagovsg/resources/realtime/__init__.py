from publicsgdata.datagovsg.resources.realtime.pm25 import AsyncPM25Resource, PM25Resource


class RealtimeResource:
    def __init__(self, client: object) -> None:
        self.pm25 = PM25Resource(client)  # type: ignore[arg-type]


class AsyncRealtimeResource:
    def __init__(self, client: object) -> None:
        self.pm25 = AsyncPM25Resource(client)  # type: ignore[arg-type]
