from app.gateway import SecurityGateway


def test_low_risk():

    gateway = SecurityGateway()

    risk = {
        "level": "LOW"
    }

    assert gateway.decide(risk) == "ALLOW"


def test_medium_risk():

    gateway = SecurityGateway()

    risk = {
        "level": "MEDIUM"
    }

    assert gateway.decide(risk) == "MONITOR"


def test_high_risk():

    gateway = SecurityGateway()

    risk = {
        "level": "HIGH"
    }

    assert gateway.decide(risk) == "BLOCK"


def test_critical_risk():

    gateway = SecurityGateway()

    risk = {
        "level": "CRITICAL"
    }

    assert gateway.decide(risk, "ATTACKER") == "BLOCK_AND_ISOLATE"


def test_isolated_source_blocked():

    gateway = SecurityGateway()

    gateway.isolated_sources.add("ATTACKER")

    risk = {
        "level": "HIGH"
    }

    assert gateway.decide(risk, "ATTACKER") == "BLOCK_ISOLATED_SOURCE"
