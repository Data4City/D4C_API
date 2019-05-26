import queue


class EvictQueue(queue.Queue):
    def __init__(self, maxsize):
        self.discarded = 0
        super().__init__(maxsize)

    def put(self, item, block=False, timeout=None):
        while True:
            try:
                super().put(item, block=False)
            except queue.Full:
                try:
                    self.get_nowait()
                    self.discarded += 1
                except queue.Empty:
                    pass
