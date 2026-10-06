# Automotive CAN Security Gateway

A simulation-based automotive cybersecurity project that models virtual CAN traffic, intrusion detection, risk scoring, gateway enforcement, and event logging for an automotive security interview or proof-of-concept demo.

## Overview

This project illustrates a rule-based CAN security pipeline:

- virtual ECUs generate normal traffic
- attack scenarios are injected into the bus
- the IDS checks ID validity, payload plausibility, rate anomalies, replay timing, and source authenticity
- a risk engine aggregates suspicious signals into a risk level
- a gateway decides whether to allow, monitor, or block traffic
- security events are logged to CSV and surfaced in a Streamlit dashboard

This is a simulation-only prototype and not a real vehicle network implementation.

## Architecture

```text
Virtual ECUs
    ↓
Traffic Generator
    ↓
Virtual CAN Bus
    ↓
Attack Injection
    ↓
Security Detector
 ├─ ID validation
 ├─ DLC validation
 ├─ Rate anomaly detection
 ├─ Payload plausibility
 ├─ Replay timing checks
 └─ ECU source validation
    ↓
Risk Engine
    ↓
Gateway Policy
    ↓
Security Logger
    ↓
Dashboard / Metrics / CSV Audit Trail
```

## Project structure

```text
can-security-gateway/
├── app/
│   ├── __init__.py
│   ├── attacks.py
│   ├── behavior.py
│   ├── can_bus.py
│   ├── detector.py
│   ├── gateway.py
│   ├── ids.py
│   ├── logger.py
│   ├── metrics.py
│   ├── risk.py
│   ├── simulator.py
│   └── traffic_generator.py
├── dashboard/
│   └── app.py
├── data/
│   └── security_events.csv
├── tests/
│   ├── test_attacks.py
│   ├── test_behavior.py
│   ├── test_detector.py
│   ├── test_gateway.py
│   ├── test_pipeline.py
│   └── test_risk.py
├── .gitignore
├── demo.py
├── pytest.ini
├── requirements.txt
├── vehicle_simulation.py
└── README.md
```

## Features

- simulated ECUs with expected CAN identifiers and frequencies
- traffic scheduling by ECU nominal rate
- rule-based anomaly detection pipeline
- source impersonation and replay logic
- risk scoring and gateway decisioning
- CSV-based event logging
- interactive Streamlit dashboard for attack injection and monitoring

## Setup

### Prerequisites

- Python 3.9+
- pip

### Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run tests

```bash
pytest -q
```

## Run the command-line simulation

```bash
python vehicle_simulation.py
```

## Run the dashboard

```bash
streamlit run dashboard/app.py
```

Then open the local URL shown by Streamlit, typically:

```text
http://127.0.0.1:8501
```

## Threat scenarios included

- unknown CAN ID injection
- source impersonation
- payload manipulation
- flooding / high-rate traffic bursts
- replay-like repeated messages

## Formal analysis artifacts

This project includes formal engineering artifacts in the `docs/` folder:

- [docs/TARA.md](docs/TARA.md) — threat analysis and risk assessment
- [docs/HARA.md](docs/HARA.md) — hazard and risk assessment
- [docs/FMEA.md](docs/FMEA.md) — failure mode and effects analysis
- [docs/requirements_traceability.md](docs/requirements_traceability.md) — traceability between requirements, code, and tests

These documents map the threat assumptions to the actual implementation in the codebase, including the IDS logic, gateway response, and automated tests.

## Notes

This project is intentionally deterministic and explainable rather than ML-driven. It is designed to communicate a rule-based automotive security concept clearly and to be easy to explain in an interview or technical review.

## Limitations

- simulation only
- educational payloads and assumptions
- no real ECU hardware or vehicle network integration
- not intended as production-ready automotive security software

## License

This project is intended for educational and portfolio use.
