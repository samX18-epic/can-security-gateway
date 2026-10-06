import random
import time


ECUS = {
    "BRAKE": {
        "can_id": 0x100,
        "frequency": 100,
    },
    "STEERING": {
        "can_id": 0x120,
        "frequency": 50,
    },
    "ADAS": {
        "can_id": 0x180,
        "frequency": 20,
    },
    "SPEED": {
        "can_id": 0x200,
        "frequency": 50,
    },
    "INSTRUMENT": {
        "can_id": 0x300,
        "frequency": 10,
    },
}


def create_frame(can_id, source, data):
    return {
        "timestamp": time.monotonic(),
        "can_id": can_id,
        "source": source,
        "dlc": len(data),
        "data": data,
    }


def generate_speed_frame(speed=None):
    if speed is None:
        speed = random.randint(0, 120)

    speed = max(0, min(speed, 250))

    data = [
        speed & 0xFF,
        (speed >> 8) & 0xFF,
        0,
        0,
        0,
        0,
        0,
        0,
    ]

    return create_frame(0x200, "SPEED", data)


def generate_brake_frame(brake_pressed=None):
    if brake_pressed is None:
        brake_pressed = random.choice([0, 1])

    data = [
        brake_pressed,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ]

    return create_frame(0x100, "BRAKE", data)


def generate_steering_frame(angle=None):
    if angle is None:
        angle = random.randint(-450, 450)

    encoded_angle = angle + 450

    data = [
        encoded_angle & 0xFF,
        (encoded_angle >> 8) & 0xFF,
        0,
        0,
        0,
        0,
        0,
        0,
    ]

    return create_frame(0x120, "STEERING", data)


def generate_adas_frame():
    status = random.choice([0, 1])

    data = [
        status,
        random.randint(0, 100),
        0,
        0,
        0,
        0,
        0,
        0,
    ]

    return create_frame(0x180, "ADAS", data)


def generate_instrument_frame(speed=None):
    if speed is None:
        speed = random.randint(0, 120)

    data = [
        speed & 0xFF,
        (speed >> 8) & 0xFF,
        0,
        0,
        0,
        0,
        0,
        0,
    ]

    return create_frame(0x300, "INSTRUMENT", data)


def generate_frame(ecu_name):
    generators = {
        "BRAKE": generate_brake_frame,
        "STEERING": generate_steering_frame,
        "ADAS": generate_adas_frame,
        "SPEED": generate_speed_frame,
        "INSTRUMENT": generate_instrument_frame,
    }

    if ecu_name not in generators:
        raise ValueError(f"Unknown ECU: {ecu_name}")

    return generators[ecu_name]()
