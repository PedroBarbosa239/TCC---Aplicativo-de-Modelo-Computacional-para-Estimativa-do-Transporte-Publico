class ContextNormalizer:

    ROAD_FLOW = {

        "motorway": 0,
        "trunk": 10,
        "primary": 20,
        "secondary": 35,
        "tertiary": 50,
        "residential": 75,
        "service": 85,
        "living_street": 90,
        "track": 100,
        "path": 100,
        "unclassified": 60,
        "unknown": 50

    }

 
    def normalize(self, context):

        return {
            "raw": context,
            "normalized": {
                "rain":
                    self.normalize_rain(
                        context["rain"]
                    ),

                "visibility":
                    self.normalize_visibility(
                        context["visibility"]
                    ),

                "wind":
                    self.normalize_wind(
                        context["wind_speed"]
                    ),

                "traffic":
                    self.normalize_congestion(
                        context["congestion"]
                    ),

                "speed":
                    self.normalize_speed(
                        context["current_speed"]
                    ),

                "road_flow":
                    self.normalize_road(
                        context["road_type"]
                    ),

                "previous_delay":
                    self.normalize_delay(
                        context["previous_delay"]
                    ),

                "previous_confidence":
                    self.normalize_confidence(
                        context["previous_confidence"]
                    )

            }

        }

#funções para normalizar

    def normalize_rain(self, rain):
        rain = max(0, min(rain, 20))
        return (rain / 20) * 100

    def normalize_visibility(self, visibility):
        visibility = max(0, min(visibility, 10000))
        return 100 - ((visibility / 10000) * 100)

    def normalize_wind(self, wind):
        wind = max(0, min(wind, 80))
        return (wind / 80) * 100

    def normalize_congestion(self, congestion):
        return max(0, min(congestion, 100))

    def normalize_speed(self, speed):
        speed = max(0, min(speed, 110))
        return 100 - ((speed / 110) * 100)

    def normalize_road(self, road):
        return self.ROAD_FLOW.get(
            road,
            self.ROAD_FLOW["unknown"]
        )

    def normalize_delay(self, delay):
        delay = max(-15, min(delay, 15))
        return ((delay + 15) / 30) * 100

    def normalize_confidence(self, confidence):
        return max(0, min(confidence, 100))