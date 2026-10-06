import time

from app.attacks import (
    create_flood_frame,
    create_flooding_attack,
    create_payload_attack,
    create_spoofing_attack,
    create_unknown_id_attack,
)
from app.can_bus import VirtualCANBus
from app.detector import SecurityDetector
from app.gateway import SecurityGateway
from app.logger import SecurityLogger
from app.metrics import SecurityMetrics
from app.risk import calculate_risk
from app.traffic_generator import VehicleTrafficGenerator


def print_event(frame, detection, risk, action):

    print(
        f"[{risk['level']:8}] "
        f"ID={hex(frame['can_id']):>5} "
        f"SOURCE={frame['source']:<10} "
        f"RATE={detection['observed_rate']:<4} "
        f"ACTION={action:<18} "
        f"REASONS={','.join(risk['reasons'])}"
    )


def run_simulation(duration=20):

    bus = VirtualCANBus()
    detector = SecurityDetector()
    gateway = SecurityGateway()
    logger = SecurityLogger()
    metrics = SecurityMetrics()
    traffic_generator = VehicleTrafficGenerator()

    start = time.monotonic()
    attack_counter = 0
    flood_mode = False
    flood_end = 0.0

    print()
    print("=" * 100)
    print("AUTOMOTIVE CAN SECURITY SIMULATION")
    print("=" * 100)
    print()

    while time.monotonic() - start < duration:

        frames = traffic_generator.generate_ready_frames()

        for frame in frames:
            bus.send(frame)

        attack_counter += 1

        if attack_counter % 100 == 0:
            attack = create_spoofing_attack()
            bus.send(attack)
            print("\n>>> SPOOFING ATTACK INJECTED")

        if attack_counter % 180 == 0:
            attack = create_payload_attack()
            bus.send(attack)
            print("\n>>> PAYLOAD ATTACK INJECTED")

        if attack_counter % 250 == 0:
            attack = create_unknown_id_attack()
            bus.send(attack)
            print("\n>>> UNKNOWN-ID ATTACK INJECTED")

        if attack_counter % 500 == 0:
            flood_mode = True
            flood_end = time.monotonic() + 2
            print("\n>>> FLOODING ATTACK STARTED")

        if flood_mode:
            if time.monotonic() < flood_end:
                for _ in range(10):
                    bus.send(create_flood_frame())
            else:
                flood_mode = False
                print("\n>>> FLOODING ATTACK ENDED")

        while bus.pending_frames():

            received = bus.receive()

            detection = detector.analyze(received)
            risk = calculate_risk(detection)
            action = gateway.decide(
                risk,
                received["source"],
            )
            metrics.record(risk, action)

            if risk["level"] != "LOW":
                logger.log(
                    detection,
                    risk,
                    action,
                )
                print_event(
                    received,
                    detection,
                    risk,
                    action,
                )

        time.sleep(0.005)

    print()
    print("=" * 100)
    print("SIMULATION COMPLETE")
    print("=" * 100)
    print()
    print("Security events:")
    print("data/security_events.csv")
    print()
    print("SECURITY METRICS")
    print("=" * 60)

    summary = metrics.summary()
    print("Total frames:", summary["total_frames"])
    print("Normal frames:", summary["normal_frames"])
    print("Suspicious frames:", summary["suspicious_frames"])
    print("Suspicious percentage:", f"{summary['suspicious_percentage']}%")
    print("\nAttack detections:")
    for attack, count in summary["attack_counts"].items():
        print(f"  {attack:<25} {count}")

    print("\nGateway actions:")
    for action, count in summary["gateway_actions"].items():
        print(f"  {action:<25} {count}")


if __name__ == "__main__":
    run_simulation(20)
