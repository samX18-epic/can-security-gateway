import time

from app.simulator import generate_frame


class ECUStream:

    def __init__(self, ecu_name, frequency):

        self.ecu_name = ecu_name
        self.frequency = frequency

        self.period = 1.0 / frequency

        self.next_time = time.monotonic()

    def ready(self):

        return time.monotonic() >= self.next_time

    def generate(self):

        self.next_time += self.period

        return generate_frame(self.ecu_name)


class VehicleTrafficGenerator:

    def __init__(self):

        self.streams = [
            ECUStream("BRAKE", 100),
            ECUStream("STEERING", 50),
            ECUStream("ADAS", 20),
            ECUStream("SPEED", 50),
            ECUStream("INSTRUMENT", 10),
        ]

    def generate_ready_frames(self):

        frames = []

        for stream in self.streams:

            if stream.ready():

                frames.append(
                    stream.generate()
                )

        return frames
