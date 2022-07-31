from numpy import double


class MetricSignal:
    def __init__(
        self,
        signal: bool = False,
        message: str = None,
        payload=None,
        score: double = 0,
    ) -> None:
        self.signal = signal
        self.payload = payload
        self.message = message
        self.score = score
