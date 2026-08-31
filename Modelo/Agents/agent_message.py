class AgentMessage:

    def __init__(
        self,
        source_agent,
        route_id,
        departure_time,
        arrival_time=None,
        estimated_delay=0.0,
        confidence=0.0
    ):

        self.source_agent = source_agent
        self.route_id = route_id
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.estimated_delay = estimated_delay
        self.confidence = confidence

    def __repr__(self):

        return (
            f"AgentMessage("
            f"source={self.source_agent}, "
            f"route={self.route_id}, "
            f"departure={self.departure_time}, "
            f"arrival={self.arrival_time}, "
            f"delay={self.estimated_delay}, "
            f"confidence={self.confidence}"
            f")"
        )