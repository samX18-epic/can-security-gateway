from app.attacks import (
    create_spoofing_attack,
    create_payload_attack,
    create_unknown_id_attack,
    create_flooding_attack,
    create_replay_attack
)

from app.simulator import generate_speed_frame


def test_spoofing_attack():

    frame = create_spoofing_attack()

    assert frame["can_id"] == 0x200
    assert frame["source"] == "ATTACKER"


def test_payload_attack():

    frame = create_payload_attack()

    assert frame["can_id"] == 0x200
    assert frame["source"] == "ATTACKER"


def test_unknown_id_attack():

    frame = create_unknown_id_attack()

    assert frame["can_id"] == 0x555


def test_flooding_attack():

    frames = create_flooding_attack(100)

    assert len(frames) == 100

    for frame in frames:
        assert frame["can_id"] == 0x200


def test_replay_attack():

    original = generate_speed_frame(80)

    frames = create_replay_attack(original, 5)

    assert len(frames) == 5

    assert frames[0]["data"] == original["data"]
