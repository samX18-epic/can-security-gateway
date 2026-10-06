def calculate_risk(result):

    score = 0
    reasons = []

    if not result["id_valid"]:
        score += 40
        reasons.append("UNKNOWN_CAN_ID")

    if not result["dlc_valid"]:
        score += 20
        reasons.append("INVALID_DLC")

    if not result["source_valid"]:
        score += 40
        reasons.append("SOURCE_IMPERSONATION")

    if result["rate_anomaly"]:
        score += 30
        reasons.append("ABNORMAL_MESSAGE_RATE")

    if not result["payload_valid"]:
        score += 30
        reasons.append("INVALID_PAYLOAD")

    if result["replay_detected"]:
        score += 30
        reasons.append("REPLAY_DETECTED")

    if score >= 70:
        level = "CRITICAL"
    elif score >= 40:
        level = "HIGH"
    elif score >= 20:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "score": score,
        "level": level,
        "reasons": reasons,
    }
