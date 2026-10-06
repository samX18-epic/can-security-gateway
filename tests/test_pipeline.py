from app.attacks import (
    create_payload_attack,
    create_unknown_id_attack,
)
from app.detector import SecurityDetector
from app.gateway import SecurityGateway
from app.risk import calculate_risk


def process(frame):

    detector = SecurityDetector()

    gateway = SecurityGateway()

    detection = detector.analyze(frame)

    risk = calculate_risk(detection)

    action = gateway.decide(risk)

    return detection, risk, action


def test_unknown_id_pipeline():

    frame = create_unknown_id_attack()

    detection, risk, action = process(frame)

    assert detection["id_valid"] is False

    assert risk["level"] in [
        "HIGH",
        "CRITICAL",
    ]

    assert action in [
        "BLOCK",
        "BLOCK_AND_ISOLATE",
    ]


def test_payload_attack_pipeline():

    frame = create_payload_attack()

    detection, risk, action = process(frame)

    assert detection["payload_valid"] is False

    assert risk["level"] in [
        "MEDIUM",
        "HIGH",
        "CRITICAL",
    ]

    assert action != "ALLOW"
