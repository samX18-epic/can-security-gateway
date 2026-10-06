class SecurityGateway:

    def __init__(self):
        self.isolated_sources = set()

    def decide(self, risk, source=None):

        level = risk["level"]

        if source in self.isolated_sources:
            return "BLOCK_ISOLATED_SOURCE"

        if level == "LOW":
            return "ALLOW"

        if level == "MEDIUM":
            return "MONITOR"

        if level == "HIGH":
            return "BLOCK"

        if level == "CRITICAL":
            if source is not None:
                self.isolated_sources.add(source)
            return "BLOCK_AND_ISOLATE"

        return "BLOCK"

    def is_isolated(self, source):
        return source in self.isolated_sources

    def clear_isolation(self):
        self.isolated_sources.clear()


Gateway = SecurityGateway
