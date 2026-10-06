from app.risk import calculate_risk


def base_result():

    return {
        "id_valid": True,
        "dlc_valid": True,
        "source_valid": True,
        "payload_valid": True,
        "rate_anomaly": False,
        "replay_detected": False
    }


def test_normal_frame():

    result = base_result()

    risk = calculate_risk(result)

    assert risk["level"] == "LOW"
    assert risk["score"] == 0


def test_unknown_id():

    result = base_result()

    result["id_valid"] = False

    risk = calculate_risk(result)

    assert risk["score"] == 40
    assert risk["level"] == "HIGH"


def test_flooding():

    result = base_result()

    result["rate_anomaly"] = True

    risk = calculate_risk(result)

    assert risk["score"] == 30
    assert risk["level"] == "MEDIUM"


def test_multiple_attacks():

    result = base_result()

    result["id_valid"] = False
    result["rate_anomaly"] = True
    result["payload_valid"] = False

    risk = calculate_risk(result)

    assert risk["score"] == 100
    assert risk["level"] == "CRITICAL"
