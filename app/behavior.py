EXPECTED_SOURCES = {
    0x100: "BRAKE",
    0x120: "STEERING",
    0x180: "ADAS",
    0x200: "SPEED",
    0x300: "INSTRUMENT",
}


class ECUBehaviorMonitor:

    def __init__(self):
        self.violations = 0

    def check_source(self, frame):

        expected_source = EXPECTED_SOURCES.get(
            frame["can_id"]
        )

        if expected_source is None:
            return False

        return frame["source"] == expected_source
