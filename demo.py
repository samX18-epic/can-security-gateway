from app.simulator import generate_speed_frame
from app.attacks import (
    create_spoofing_attack,
    create_payload_attack,
    create_unknown_id_attack
)

from app.detector import SecurityDetector
from app.risk import calculate_risk
from app.gateway import SecurityGateway


detector = SecurityDetector()
gateway = SecurityGateway()


def process_frame(name, frame):

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    print("CAN ID:", hex(frame["can_id"]))
    print("Source:", frame["source"])
    print("Data:", frame["data"])

    detection = detector.analyze(frame)

    risk = calculate_risk(detection)

    action = gateway.decide(risk)

    print("\nDetection:")
    print(detection)

    print("\nRisk:")
    print(risk)

    print("\nGateway Action:")
    print(action)


# 1. Normal traffic

normal_frame = generate_speed_frame(80)

process_frame(
    "NORMAL FRAME",
    normal_frame
)


# 2. Spoofing

spoofed_frame = create_spoofing_attack()

process_frame(
    "SPOOFING ATTACK",
    spoofed_frame
)


# 3. Payload manipulation

payload_attack = create_payload_attack()

process_frame(
    "PAYLOAD MANIPULATION",
    payload_attack
)


# 4. Unknown CAN ID

unknown_attack = create_unknown_id_attack()

process_frame(
    "UNKNOWN CAN ID ATTACK",
    unknown_attack
)
