class MetricSignal:
    def __init__(self, signal : bool = False, message: str = None,payload = None) -> None:
        self.signal = signal
        self.payload = payload
        self.message = message
    