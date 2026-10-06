ALLOWED_IDS = {
    0x100: "BRAKE",
    0x120: "STEERING",
    0x180: "ADAS",
    0x200: "SPEED",
    0x300: "INSTRUMENT"
}


def check_can_id(can_id):

    return can_id in ALLOWED_IDS


def check_dlc(dlc):

    return 0 <= dlc <= 8


def validate_frame(frame):

    results = {
        "id_valid": check_can_id(frame["can_id"]),
        "dlc_valid": check_dlc(frame["dlc"])
    }

    results["valid"] = (
        results["id_valid"]
        and results["dlc_valid"]
    )

    return results
