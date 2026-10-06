# Requirements Traceability Matrix

## Purpose
This matrix connects the TARA/HARA analysis to the implemented system behavior and the automated tests.

| Requirement ID | Requirement | Implementation | Risk Signal | Gateway Response | Test Coverage |
|---|---|---|---|---|---|
| SEC-REQ-001 | Detect unexpected ECU sources | `app/behavior.py` | `SOURCE_IMPERSONATION` | `BLOCK` / `BLOCK_AND_ISOLATE` | `tests/test_behavior.py`, `tests/test_pipeline.py` |
| SEC-REQ-002 | Detect unknown CAN IDs | `app/ids.py`, `app/detector.py` | `UNKNOWN_CAN_ID` | `BLOCK` | `tests/test_pipeline.py` |
| SEC-REQ-003 | Detect abnormal message rate | `app/detector.py` | `ABNORMAL_MESSAGE_RATE` | `MONITOR` / `BLOCK` | `tests/test_detector.py` |
| SEC-REQ-004 | Detect invalid payloads | `app/detector.py` | `INVALID_PAYLOAD` | `MONITOR` / `BLOCK` | `tests/test_pipeline.py` |
| SEC-REQ-005 | Detect replay-like repeated traffic | `app/detector.py` | `REPLAY_DETECTED` | `BLOCK` | `tests/test_detector.py` |
| SEC-REQ-006 | Use risk-based gateway handling | `app/risk.py`, `app/gateway.py` | aggregated risk score | `ALLOW`, `MONITOR`, `BLOCK`, `BLOCK_AND_ISOLATE` | `tests/test_gateway.py`, `tests/test_risk.py` |
| SEC-REQ-007 | Preserve an audit trail | `app/logger.py` | event log entry | recorded in CSV | `vehicle_simulation.py` |

## Traceability Narrative

- TARA identifies that source spoofing is a threat.
- The project implements source validation in `app/behavior.py`.
- The risk engine increases the score for source impersonation in `app/risk.py`.
- The gateway responds with blocking or isolation in `app/gateway.py`.
- Automated tests validate the behavior in the test suite.

This creates a clear chain from threat analysis to implemented behavior to validation.
