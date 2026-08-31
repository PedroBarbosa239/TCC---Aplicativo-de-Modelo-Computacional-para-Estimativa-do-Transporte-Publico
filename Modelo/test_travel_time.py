from Agents.bus_stop_agent import BusStopAgent
from Agents.travel_time import TravelTimeCalculator


# ==========================================
# CRIA OS AGENTES
# ==========================================

p001 = BusStopAgent(
    stop_id="P001",
    latitude=-22.2231,
    longitude=-54.8120
)

p002 = BusStopAgent(
    stop_id="P002",
    latitude=-22.2240,
    longitude=-54.8130
)


# ==========================================
# CALCULA A DISTÂNCIA
# ==========================================

distance = TravelTimeCalculator.haversine_distance(
    p001.latitude,
    p001.longitude,
    p002.latitude,
    p002.longitude
)


print("================================")
print("TESTE DE TEMPO ENTRE AGENTES")
print("================================")

print(
    f"Distância P001 → P002: "
    f"{distance:.2f} metros"
)


# ==========================================
# DEFINE VELOCIDADE
# ==========================================

speed = 30.0  # km/h


# ==========================================
# CALCULA TEMPO
# ==========================================

travel_time = TravelTimeCalculator.calculate(
    distance,
    speed
)


print(
    f"Velocidade estimada: "
    f"{speed:.2f} km/h"
)

print(
    f"Tempo estimado: "
    f"{travel_time:.2f} segundos"
)