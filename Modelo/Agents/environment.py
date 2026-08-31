class Environment:

    def __init__(
        self,
        rain=0.0,
        visibility=10000.0,
        wind_speed=0.0,
        traffic=0.0,
        road_type="unknown"
    ):

        # ==========================================
        # DADOS CLIMÁTICOS
        # ==========================================

        self.rain = rain
        self.visibility = visibility
        self.wind_speed = wind_speed

        # ==========================================
        # DADOS DA VIA / TRÂNSITO
        # ==========================================

        self.traffic = traffic
        self.road_type = road_type


    # ==========================================
    # REPRESENTAÇÃO
    # ==========================================

    def __repr__(self):

        return (
            f"Environment("
            f"rain={self.rain}, "
            f"visibility={self.visibility}, "
            f"wind_speed={self.wind_speed}, "
            f"traffic={self.traffic}, "
            f"road_type='{self.road_type}'"
            f")"
        )

    def update(
    self,
    rain=None,
    visibility=None,
    wind_speed=None,
    traffic=None,
    road_type=None
):

        if rain is not None:
            self.rain = rain

        if visibility is not None:
            self.visibility = visibility

        if wind_speed is not None:
            self.wind_speed = wind_speed

        if traffic is not None:
            self.traffic = traffic

        if road_type is not None:
            self.road_type = road_type