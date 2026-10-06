from app.behavior import ECUBehaviorMonitor


def test_correct_ecu_source():

    monitor = ECUBehaviorMonitor()

    frame = {
        "can_id": 0x200,
        "source": "SPEED",
    }

    assert monitor.check_source(frame) is True


def test_source_impersonation():

    monitor = ECUBehaviorMonitor()

    frame = {
        "can_id": 0x200,
        "source": "ATTACKER",
    }

    assert monitor.check_source(frame) is False
