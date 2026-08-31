from Agents.agent_network import AgentNetwork
from Data.stop_loader import StopLoader
from Data.route_loader import RouteLoader


# ==========================================
# CARREGA OS PONTOS
# ==========================================

stop_loader = StopLoader(
    "Data/stops.csv"
)

stop_loader.load()

agents = stop_loader.create_agents()


# ==========================================
# CRIA A REDE
# ==========================================

network = AgentNetwork()

network.add_agents(agents)


# ==========================================
# CARREGA AS ROTAS
# ==========================================

route_loader = RouteLoader(
    "Data/routes.csv"
)

route_loader.load()


# ==========================================
# CONECTA AS ROTAS
# ==========================================

network.connect_routes_from_loader(
    route_loader
)


# ==========================================
# PEGA O AGENTE P002
# ==========================================

p002 = network.get_agent("P002")


# ==========================================
# CALCULA O TRECHO
# ==========================================

result = p002.calculate_previous_segment_time(
    route_id="101",
    speed_kmh=30
)


# ==========================================
# RESULTADO
# ==========================================

print()
print("================================")
print("TRECHO CALCULADO PELO AGENTE")
print("================================")

print(
    f"Linha: {result['route_id']}"
)

print(
    f"Agente anterior: "
    f"{result['previous_agent']}"
)

print(
    f"Agente atual: "
    f"{result['current_agent']}"
)

print(
    f"Distância: "
    f"{result['distance_meters']:.2f} m"
)

print(
    f"Velocidade: "
    f"{result['speed_kmh']:.2f} km/h"
)

print(
    f"Tempo: "
    f"{result['travel_time_seconds']:.2f} s"
)


# ==========================================
# ESTADO DO AGENTE
# ==========================================

print()
print("================================")
print("ESTADO DO P002")
print("================================")

print(
    "Tempo desde o agente anterior:",
    f"{p002.travel_time_from_previous:.2f} s"
)