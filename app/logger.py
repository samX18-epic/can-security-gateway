import csv
import os
from datetime import datetime


class SecurityLogger:

    def __init__(self, filepath="data/security_events.csv"):

        self.filepath = filepath

        os.makedirs(
            os.path.dirname(filepath),
            exist_ok=True,
        )

        if not os.path.exists(filepath):

            with open(
                filepath,
                "w",
                newline="",
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    "timestamp",
                    "can_id",
                    "source",
                    "observed_rate",
                    "expected_rate",
                    "id_valid",
                    "dlc_valid",
                    "payload_valid",
                    "rate_anomaly",
                    "replay_detected",
                    "risk_score",
                    "risk_level",
                    "reasons",
                    "gateway_action",
                ])

    def log(self, detection, risk, action):

        timestamp = datetime.now().isoformat(
            timespec="milliseconds"
        )

        with open(
            self.filepath,
            "a",
            newline="",
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                timestamp,
                hex(detection["can_id"]),
                detection["source"],
                detection["observed_rate"],
                detection["expected_rate"],
                detection["id_valid"],
                detection["dlc_valid"],
                detection["payload_valid"],
                detection["rate_anomaly"],
                detection["replay_detected"],
                risk["score"],
                risk["level"],
                "|".join(risk["reasons"]),
                action,
            ])
