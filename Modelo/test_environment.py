from Agents.environment import Environment
from Agents.bus_stop_agent import BusStopAgent


# ==========================================
# AMBIENTES
# ==========================================

environment_1 = Environment(
    rain=0.0,
    visibility=10000,
    wind_speed=5,
    traffic=20,
    road_type="avenida"
)

environment_2 = Environment(
    rain=5.0,
    visibility=7000,
    wind_speed=12,
    traffic=65,
    road_type="rua"
)

environment_3 = Environment(
    rain=10.0,
    visibility=4000,
    wind_speed=20,
    traffic=90,
    road_type="avenida"
)


# ==========================================
# AGENTES
# ==========================================

agent_1 = BusStopAgent(
    stop_id="P001",
    latitude=-22.2231,
    longitude=-54.8120,
    lines=["101"],
    environment=environment_1
)

agent_2 = BusStopAgent(
    stop_id="P002",
    latitude=-22.2240,
    longitude=-54.8130,
    lines=["101"],
    environment=environment_2
)

agent_3 = BusStopAgent(
    stop_id="P003",
    latitude=-22.2250,
    longitude=-54.8140,
    lines=["101"],
    environment=environment_3
)

agent_1.environment.update(
    rain=5.0,
    traffic=70.0
)
# ==========================================
# TESTE
# ==========================================

print()
print("================================")
print("AMBIENTE DOS AGENTES")
print("================================")

print()
print(agent_1.stop_id)
print(agent_1.environment)

print()
print(agent_2.stop_id)
print(agent_2.environment)

print()
print(agent_3.stop_id)
print(agent_3.environment)