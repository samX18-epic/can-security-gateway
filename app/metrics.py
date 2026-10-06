class SecurityMetrics:

    def __init__(self):

        self.total_frames = 0
        self.normal_frames = 0
        self.suspicious_frames = 0

        self.attack_counts = {
            "UNKNOWN_CAN_ID": 0,
            "SOURCE_IMPERSONATION": 0,
            "ABNORMAL_MESSAGE_RATE": 0,
            "INVALID_PAYLOAD": 0,
            "REPLAY_DETECTED": 0,
            "INVALID_DLC": 0,
        }

        self.gateway_actions = {
            "ALLOW": 0,
            "MONITOR": 0,
            "BLOCK": 0,
            "BLOCK_AND_ISOLATE": 0,
            "BLOCK_ISOLATED_SOURCE": 0,
        }

    def record(self, risk, action):

        self.total_frames += 1

        if risk["level"] == "LOW":
            self.normal_frames += 1
        else:
            self.suspicious_frames += 1

        for reason in risk["reasons"]:
            if reason in self.attack_counts:
                self.attack_counts[reason] += 1

        if action in self.gateway_actions:
            self.gateway_actions[action] += 1

    def detection_rate(self):

        if self.total_frames == 0:
            return 0.0

        return (
            self.suspicious_frames / self.total_frames
        ) * 100

    def summary(self):

        return {
            "total_frames": self.total_frames,
            "normal_frames": self.normal_frames,
            "suspicious_frames": self.suspicious_frames,
            "suspicious_percentage": round(
                self.detection_rate(),
                2,
            ),
            "attack_counts": self.attack_counts,
            "gateway_actions": self.gateway_actions,
        }
