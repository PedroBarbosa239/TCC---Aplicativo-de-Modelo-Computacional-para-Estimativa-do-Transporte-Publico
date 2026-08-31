import math


class TravelTimeCalculator:

    @staticmethod
    def haversine_distance(
        latitude_1,
        longitude_1,
        latitude_2,
        longitude_2
    ):
        """
        Calcula a distância entre duas coordenadas
        geográficas utilizando a fórmula de Haversine.

        Retorno:
            distância em metros
        """

        earth_radius = 6371000  # metros

        lat1 = math.radians(latitude_1)
        lon1 = math.radians(longitude_1)

        lat2 = math.radians(latitude_2)
        lon2 = math.radians(longitude_2)

        delta_lat = lat2 - lat1
        delta_lon = lon2 - lon1

        a = (
            math.sin(delta_lat / 2) ** 2
            +
            math.cos(lat1)
            * math.cos(lat2)
            * math.sin(delta_lon / 2) ** 2
        )

        c = 2 * math.atan2(
            math.sqrt(a),
            math.sqrt(1 - a)
        )

        return earth_radius * c

    @staticmethod
    def calculate(
        distance_meters,
        speed_kmh
    ):
        """
        Calcula o tempo de deslocamento.

        Retorno:
            tempo em segundos
        """

        if speed_kmh <= 0:
            raise ValueError(
                "A velocidade deve ser maior que zero."
            )

        speed_mps = speed_kmh / 3.6

        return distance_meters / speed_mps