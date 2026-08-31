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
# CONECTA AUTOMATICAMENTE
# ==========================================

network.connect_routes_from_loader(
    route_loader
)


# ==========================================
# TESTE
# ==========================================

print()
print("================================")
print("REDE GERADA AUTOMATICAMENTE")
print("================================")

print(
    "Quantidade de agentes:",
    network.size()
)


for route_id in route_loader.get_route_ids():

    route = route_loader.get_route(
        route_id
    )

    print()
    print(
        f"Linha {route_id}:"
    )

    for stop in route:

        agent = network.get_agent(
            stop["stop_id"]
        )

        print(
            f"{agent.stop_id}",
            end=""
        )

        next_agent = agent.next_agents.get(
            route_id
        )

        if next_agent is not None:

            print(
                f" → {next_agent.stop_id}",
                end=""
            )

        print()