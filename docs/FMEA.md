# Failure Mode and Effects Analysis (FMEA)

## Scope
This FMEA assesses simulated failure modes relevant to the CAN gateway prototype.

| Failure Mode | Cause | Local Effect | System Effect | Detection Method | Mitigation |
|---|---|---|---|---|---|
| Unknown CAN ID | Unauthorized frame injection | Bypass of allowlist | Suspicious or untrusted traffic accepted | ID validation | Block traffic and log event |
| Source impersonation | ECU identity changed to ATTACKER | Incorrect trust decision | Risk score elevated | Source validation | HIGH / CRITICAL gateway response |
| Payload corruption | Signal bytes manipulated | Wrong vehicle-state reading | False operational decisions | Payload plausibility check | Reject invalid payload |
| Flooding | Excessive frame volume | Message storms | Rate anomaly and degradation | Rate monitor | Monitor / block traffic |
| Replay attack | Repeated historical frame | Stale information | Misleading vehicle context | Replay timing detector | Block repeated suspicious replay |

## Risk Prioritization

The most important failure modes are those that affect safety-relevant messages and bus availability. The current prototype addresses them by combining detection and risk scoring before enforcement.
