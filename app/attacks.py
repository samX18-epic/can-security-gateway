import copy
import time

from app.simulator import generate_speed_frame


def create_spoofing_attack():
    """
    Valid CAN ID, but attacker-controlled payload.
    """

    frame = generate_speed_frame(80)

    frame["source"] = "ATTACKER"

    frame["data"] = [
        250,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ]

    return frame


def create_payload_attack():
    """
    Legitimate CAN ID with physically implausible payload.
    """

    frame = generate_speed_frame(80)

    frame["source"] = "ATTACKER"

    frame["data"] = [
        255,
        255,
        0,
        0,
        0,
        0,
        0,
        0,
    ]

    return frame


def create_unknown_id_attack():

    return {
        "timestamp": time.monotonic(),
        "can_id": 0x555,
        "source": "ATTACKER",
        "dlc": 8,
        "data": [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
        ],
    }


def create_flood_frame():

    frame = generate_speed_frame(80)

    frame["source"] = "ATTACKER"

    return frame


def create_flooding_attack(count=100):

    frames = []

    for _ in range(count):

        frames.append(create_flood_frame())

    return frames


def create_replay_attack(original_frame, count=5):

    frames = []

    for _ in range(count):

        replayed = copy.deepcopy(original_frame)

        replayed["source"] = "ATTACKER"
        replayed["timestamp"] = time.monotonic()

        frames.append(replayed)

    return frames
