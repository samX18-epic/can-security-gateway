# Hazard Analysis and Risk Assessment (HARA)

## System Context
The simulated CAN gateway protects virtual vehicle ECUs from hazardous communication conditions that could mislead the vehicle state or degrade network availability.

## Hazard Identification

| Hazard ID | Hazard Description | Scenario | Potential Consequence |
|---|---|---|---|
| HAZ-01 | Spoofed ECU source | ATTACKER injects a valid CAN ID with an unexpected source | Incorrect actuator or sensor interpretation |
| HAZ-02 | Invalid CAN ID | Unauthorized CAN ID appears on the bus | Untrusted data enters the network |
| HAZ-03 | Flooding condition | Excessive message rate observed | Network degradation or denial-of-service effect |
| HAZ-04 | Plausibility violation | Implausible speed or signal value | Wrong vehicle-state estimation |
| HAZ-05 | Replay condition | Previously seen payload reappears too quickly | Stale or duplicated vehicle information |

## Severity and Risk Considerations

- The highest risk scenarios are those that mislead safety-relevant signals or degrade communications under load.
- Rate anomalies and spoofed source identities are treated as critical indicators because they may produce incorrect vehicle behavior.
- The risk engine aggregates these conditions before the gateway decides on blocking or isolation.

## Safety Goal

The system shall detect and restrict suspicious traffic before it can create a hazardous or misleading vehicle-state condition.
