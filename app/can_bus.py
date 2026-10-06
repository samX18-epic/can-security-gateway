from collections import deque


class VirtualCANBus:

    def __init__(self):
        self.frames = deque()

    def send(self, frame):
        self.frames.append(frame)

    def receive(self):
        if not self.frames:
            return None

        return self.frames.popleft()

    def pending_frames(self):
        return len(self.frames)

    def clear(self):
        self.frames.clear()
