# Threat Analysis and Risk Assessment (TARA)

## System
Automotive CAN Security Gateway

## Scope

The analysis considers simulated communication between virtual vehicle ECUs over a CAN bus and unauthorized manipulation of that communication.

| Asset | Threat | Attack Vector | Potential Impact | Detection / Mitigation |
|---|---|---|---|---|
| CAN communication | Message spoofing | Unauthorized CAN frame injection | Incorrect ECU information | Source validation + ID validation |
| Speed signal | Payload manipulation | Malicious signal injection | Incorrect vehicle-state information | Payload plausibility check |
| CAN bus availability | Flooding | High-rate frame injection | Communication degradation | Rate anomaly detection |
| CAN communication | Replay | Re-transmission of previously observed frame | Stale vehicle information | Replay timing detection |
| CAN network | Unknown message injection | Unauthorized CAN ID | Untrusted communication | CAN ID allowlisting |

## Security Goals

1. Detect unauthorized CAN messages.
2. Detect abnormal communication rates.
3. Detect implausible signal values.
4. Detect replay-like communication behavior.
5. Prevent suspicious traffic from reaching protected components.
6. Maintain an auditable security event trail.

## Traceability to Implementation

- `SEC-REQ-001`: Detect unexpected ECU sources  
  Implemented in `app/behavior.py` through `EXPECTED_SOURCES` and `ECUBehaviorMonitor.check_source()`.

- `SEC-REQ-002`: Detect unknown CAN IDs  
  Implemented in `app/ids.py` via `check_can_id()` and enforced in `app/detector.py`.

- `SEC-REQ-003`: Detect abnormal message rates  
  Implemented in `app/detector.py` via `RateMonitor`.

- `SEC-REQ-004`: Detect invalid payloads  
  Implemented in `app/detector.py` via `check_speed_payload()`.

- `SEC-REQ-005`: Detect replay-like repeated messages  
  Implemented in `app/detector.py` via `ReplayDetector`.

- `SEC-REQ-006`: Enforce risk-based gateway response  
  Implemented in `app/gateway.py` and `app/risk.py`.

- `SEC-REQ-007`: Maintain audit trail  
  Implemented in `app/logger.py` and logged through `VehicleSimulation` events.
