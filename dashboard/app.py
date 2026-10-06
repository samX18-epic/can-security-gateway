import random
import sys
import time
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.behavior import EXPECTED_SOURCES
from app.detector import SecurityDetector
from app.gateway import Gateway
from app.risk import calculate_risk

st.set_page_config(
    page_title="Automotive CAN Security Monitor",
    page_icon="🛡️",
    layout="wide",
)

st.markdown(
    """
    <style>
        .main {
            background: linear-gradient(180deg, #0b1020 0%, #111827 100%);
            color: #e5e7eb;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        h1, h2, h3 {
            color: #f8fafc;
        }
        .stButton > button {
            width: 100%;
            border-radius: 0.75rem;
            border: 1px solid #3b82f6;
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            color: white;
            font-weight: 600;
            padding: 0.7rem 1rem;
        }
        .stButton > button:hover {
            background: linear-gradient(135deg, #1d4ed8, #1e40af);
            border-color: #60a5fa;
        }
        [data-testid="stSidebar"] {
            background: #0f172a;
        }
        .stMetric {
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid rgba(148, 163, 184, 0.25);
            border-radius: 0.9rem;
            padding: 0.8rem 0.9rem;
        }
        div[data-testid="stDataFrame"] {
            border-radius: 0.75rem;
            overflow: hidden;
            border: 1px solid rgba(148, 163, 184, 0.2);
        }
        .warning-box {
            background: rgba(250, 204, 21, 0.08);
            border: 1px solid rgba(250, 204, 21, 0.4);
            border-radius: 0.8rem;
            padding: 0.8rem 1rem;
            margin-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🛡️ Automotive CAN Security Gateway")
st.caption("Simulation-based IDS, risk classification, and gateway response for virtual vehicle traffic.")

st.markdown(
    """
    <div class="warning-box">
        <strong>Simulation only.</strong> This dashboard models virtual ECU traffic and intrusion patterns for educational and proof-of-concept evaluation. No real vehicle or CAN hardware is connected.
    </div>
    """,
    unsafe_allow_html=True,
)

ECUS = {
    0x100: ("Brake ECU", 100),
    0x120: ("Steering ECU", 50),
    0x180: ("ADAS ECU", 20),
    0x200: ("Speed ECU", 50),
    0x300: ("Instrument ECU", 10),
}


def make_frame(can_id, source, data, timestamp=None):
    """Create a simulated CAN frame."""
    return {
        "timestamp": timestamp if timestamp is not None else time.monotonic(),
        "can_id": can_id,
        "source": source,
        "data": list(data),
        "dlc": len(data),
    }


def normal_frame(can_id):
    """Generate plausible example payloads for virtual ECUs."""
    if can_id == 0x100:
        data = [random.choice([0, 1])] + [0] * 7
    elif can_id == 0x120:
        data = [random.randint(100, 155)] + [0] * 7
    elif can_id == 0x180:
        data = [random.randint(0, 1)] + [0] * 7
    elif can_id == 0x200:
        speed = random.randint(0, 120)
        data = list(speed.to_bytes(2, "little")) + [0] * 6
    else:
        data = [random.randint(0, 1)] + [0] * 7

    source = EXPECTED_SOURCES.get(can_id, "UNKNOWN")
    return make_frame(can_id, source, data)


def initialize_state():
    if "detector" not in st.session_state:
        st.session_state.detector = SecurityDetector()

    if "gateway" not in st.session_state:
        st.session_state.gateway = Gateway()

    if "events" not in st.session_state:
        st.session_state.events = []

    if "traffic" not in st.session_state:
        st.session_state.traffic = []

    if "blocked" not in st.session_state:
        st.session_state.blocked = 0

    if "processed" not in st.session_state:
        st.session_state.processed = 0


def process_frame(frame):
    """Run a frame through the detector, risk engine and gateway."""
    detector = st.session_state.detector
    gateway = st.session_state.gateway

    analysis = detector.analyze(frame)
    risk = calculate_risk(analysis)
    action = gateway.decide(risk, source=frame.get("source"))

    event = {
        "time": time.strftime("%H:%M:%S"),
        "CAN ID": f"0x{frame['can_id']:03X}",
        "Source": frame.get("source", "UNKNOWN"),
        "Payload": " ".join(f"{b:02X}" for b in frame["data"]),
        "Risk": risk.get("level", "UNKNOWN"),
        "Score": risk.get("score", 0),
        "Detection": ", ".join(risk.get("reasons", [])) or "No anomaly",
        "Gateway Action": action,
    }

    st.session_state.events.append(event)
    st.session_state.traffic.append({
        "time": time.strftime("%H:%M:%S"),
        "CAN ID": f"0x{frame['can_id']:03X}",
        "Risk": risk.get("level", "UNKNOWN"),
    })

    st.session_state.processed += 1

    if "BLOCK" in str(action):
        st.session_state.blocked += 1

    st.session_state.events = st.session_state.events[-500:]
    st.session_state.traffic = st.session_state.traffic[-500:]
    return event


initialize_state()

with st.sidebar:
    st.header("Simulation Controls")

    batch_size = st.slider(
        "Normal frames per batch",
        min_value=5,
        max_value=100,
        value=20,
        step=5,
    )

    st.markdown("### Inject an attack")

    attack_choice = st.selectbox(
        "Attack scenario",
        [
            "CAN ID spoofing",
            "Unknown CAN ID",
            "Payload manipulation",
            "Message flooding",
            "Replay-like repeated frame",
        ],
    )

    if st.button("🚨 Inject selected attack", type="primary"):
        if attack_choice == "CAN ID spoofing":
            frame = make_frame(
                0x200,
                "ATTACKER",
                list((250).to_bytes(2, "little")) + [0] * 6,
            )
            process_frame(frame)

        elif attack_choice == "Unknown CAN ID":
            process_frame(
                make_frame(0x555, "ATTACKER", [1, 2, 3, 4, 5, 6, 7, 8])
            )

        elif attack_choice == "Payload manipulation":
            process_frame(
                make_frame(
                    0x200,
                    EXPECTED_SOURCES.get(0x200, "UNKNOWN"),
                    [255, 255, 0, 0, 0, 0, 0, 0],
                )
            )

        elif attack_choice == "Message flooding":
            for _ in range(30):
                process_frame(
                    make_frame(
                        0x200,
                        EXPECTED_SOURCES.get(0x200, "UNKNOWN"),
                        [50, 0, 0, 0, 0, 0, 0, 0],
                    )
                )

        elif attack_choice == "Replay-like repeated frame":
            repeated = make_frame(
                0x200,
                EXPECTED_SOURCES.get(0x200, "UNKNOWN"),
                [40, 0, 0, 0, 0, 0, 0, 0],
            )
            process_frame(repeated)
            repeated["timestamp"] += 0.1
            process_frame(repeated)

        st.success("Scenario injected into the simulation.")

    if st.button("▶ Generate normal traffic"):
        ids = list(ECUS.keys())
        for _ in range(batch_size):
            process_frame(normal_frame(random.choice(ids)))

    if st.button("🧹 Reset dashboard"):
        for key in [
            "detector",
            "gateway",
            "events",
            "traffic",
            "blocked",
            "processed",
        ]:
            st.session_state.pop(key, None)
        st.rerun()


events = st.session_state.events
event_df = pd.DataFrame(events)

if not event_df.empty:
    suspicious = int((event_df["Risk"] != "LOW").sum())
    critical = int((event_df["Risk"] == "CRITICAL").sum())
else:
    suspicious = critical = 0

isolated = len(getattr(st.session_state.gateway, "isolated_sources", set()))

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Frames Processed", st.session_state.processed)
c2.metric("Suspicious Events", suspicious)
c3.metric("Critical Events", critical)
c4.metric("Blocked Frames", st.session_state.blocked)
c5.metric("Isolated Sources", isolated)

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Risk Distribution")
    if not event_df.empty:
        risk_counts = (
            event_df["Risk"].value_counts().rename_axis("Risk Level").reset_index(name="Events")
        )
        fig = px.bar(
            risk_counts,
            x="Risk Level",
            y="Events",
            color="Risk Level",
            title="Detected Events by Risk",
            template="plotly_dark",
        )
        st.plotly_chart(fig, width="stretch")
    else:
        st.info("Generate traffic or inject an attack to populate this chart.")

with right:
    st.subheader("CAN Traffic by Identifier")
    if not event_df.empty:
        id_counts = (
            event_df["CAN ID"].value_counts().rename_axis("CAN ID").reset_index(name="Frames")
        )
        fig = px.bar(
            id_counts,
            x="CAN ID",
            y="Frames",
            title="Processed Frames by CAN ID",
            template="plotly_dark",
        )
        st.plotly_chart(fig, width="stretch")
    else:
        st.info("No traffic recorded yet.")

st.divider()

st.subheader("Security Event Log")

if not event_df.empty:
    st.dataframe(
        event_df.iloc[::-1],
        hide_index=True,
        width="stretch",
    )

    csv = event_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇ Export security events as CSV",
        data=csv,
        file_name="can_security_events.csv",
        mime="text/csv",
    )
else:
    st.info("The event log is empty.")

with st.expander("Virtual ECU Configuration"):
    ecu_rows = [
        {
            "ECU": name,
            "CAN ID": f"0x{can_id:03X}",
            "Nominal Rate (Hz)": rate,
        }
        for can_id, (name, rate) in ECUS.items()
    ]
    st.dataframe(pd.DataFrame(ecu_rows), hide_index=True, width="stretch")

st.caption(
    "Prototype limitation: attack detection quality depends on the detector rules, simulated payloads, and project-defined traffic rates."
)
