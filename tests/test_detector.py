from app.detector import RateMonitor, ReplayDetector


def test_normal_rate():

    monitor = RateMonitor()

    for _ in range(10):
        rate = monitor.record(0x200)

    assert rate <= 100


def test_unknown_id_is_anomalous():

    monitor = RateMonitor()

    assert monitor.is_anomalous(0x555, 10) is True


def test_flooding_detected():

    monitor = RateMonitor()

    assert monitor.is_anomalous(0x200, 150) is True


def test_replay_detection():

    detector = ReplayDetector(minimum_replay_gap=0.5)

    frame = {
        "timestamp": 1.0,
        "can_id": 0x200,
        "source": "SPEED",
        "dlc": 8,
        "data": [80, 0, 0, 0, 0, 0, 0, 0],
    }

    assert detector.check(frame) is False

    replay = dict(frame)
    replay["timestamp"] = 1.1

    assert detector.check(replay) is True


def test_same_payload_after_long_gap():

    detector = ReplayDetector(minimum_replay_gap=0.5)

    frame = {
        "timestamp": 1.0,
        "can_id": 0x200,
        "source": "SPEED",
        "dlc": 8,
        "data": [80, 0, 0, 0, 0, 0, 0, 0],
    }

    assert detector.check(frame) is False

    later_frame = dict(frame)
    later_frame["timestamp"] = 2.0

    assert detector.check(later_frame) is False
