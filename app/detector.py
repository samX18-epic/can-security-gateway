import time
from collections import defaultdict, deque

from app.behavior import ECUBehaviorMonitor
from app.ids import validate_frame


EXPECTED_RATES = {
    0x100: 100,
    0x120: 50,
    0x180: 20,
    0x200: 50,
    0x300: 10,
}


class RateMonitor:

    def __init__(self, window_seconds=1.0, multiplier=2.0):
        self.window_seconds = window_seconds
        self.multiplier = multiplier
        self.timestamps = defaultdict(deque)

    def record(self, can_id):
        now = time.monotonic()

        queue = self.timestamps[can_id]
        queue.append(now)

        while queue and now - queue[0] > self.window_seconds:
            queue.popleft()

        return len(queue)

    def is_anomalous(self, can_id, observed_rate):
        expected = EXPECTED_RATES.get(can_id)

        if expected is None:
            return True

        threshold = expected * self.multiplier

        return observed_rate > threshold


class ReplayDetector:

    def __init__(
        self,
        history_size=100,
        minimum_replay_gap=0.5,
    ):
        self.history_size = history_size
        self.minimum_replay_gap = minimum_replay_gap

        self.history = defaultdict(
            lambda: deque(maxlen=history_size)
        )

    def _signature(self, frame):
        return (
            frame["can_id"],
            tuple(frame["data"]),
        )

    def check(self, frame):

        can_id = frame["can_id"]
        signature = self._signature(frame)
        timestamp = frame["timestamp"]

        history = self.history[can_id]

        for previous_signature, previous_timestamp in history:

            if signature != previous_signature:
                continue

            elapsed = timestamp - previous_timestamp

            if elapsed < self.minimum_replay_gap:
                return True

        history.append(
            (signature, timestamp)
        )

        return False


def decode_speed(data):

    if len(data) < 2:
        raise ValueError("Insufficient data")

    return data[0] | (data[1] << 8)


def check_speed_payload(data):

    speed = decode_speed(data)

    return 0 <= speed <= 250


class SecurityDetector:

    def __init__(self):

        self.rate_monitor = RateMonitor()
        self.replay_detector = ReplayDetector()
        self.behavior_monitor = ECUBehaviorMonitor()

    def analyze(self, frame):

        validation = validate_frame(frame)

        can_id = frame["can_id"]

        observed_rate = self.rate_monitor.record(can_id)

        rate_anomaly = self.rate_monitor.is_anomalous(
            can_id,
            observed_rate,
        )

        replay_detected = self.replay_detector.check(frame)
        source_valid = self.behavior_monitor.check_source(frame)

        payload_valid = True

        if can_id == 0x200:

            try:
                payload_valid = check_speed_payload(
                    frame["data"]
                )

            except ValueError:
                payload_valid = False

        return {
            "timestamp": frame["timestamp"],
            "can_id": can_id,
            "source": frame["source"],
            "id_valid": validation["id_valid"],
            "dlc_valid": validation["dlc_valid"],
            "payload_valid": payload_valid,
            "source_valid": source_valid,
            "observed_rate": observed_rate,
            "expected_rate": EXPECTED_RATES.get(can_id),
            "rate_anomaly": rate_anomaly,
            "replay_detected": replay_detected,
        }
