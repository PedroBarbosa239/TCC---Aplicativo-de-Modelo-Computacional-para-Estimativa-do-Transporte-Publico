from Data.stop_loader import StopLoader
from Agents.agent_network import AgentNetwork

loader = StopLoader(
    "Data/stops.csv"
)

stops = loader.load()
agents = loader.create_agents()

print()
print("================================")
print("AGENTES CRIADOS")
print("================================")

print(
    "Quantidade de agentes:",
    len(agents)
)

for agent in agents:

    print(agent)

print()
print("================================")
print("TESTE DO STOP LOADER")
print("================================")

print(
    "Quantidade de pontos:",
    loader.size()
)

print()

for stop in stops:

    print(
        f"ID: {stop['stop_id']}"
    )

    print(
        f"Latitude: {stop['latitude']}"
    )

    print(
        f"Longitude: {stop['longitude']}"
    )

    print(
        f"Linhas: {stop['lines']}"
    )

    network = AgentNetwork()

network.add_agents(agents)

print()
print("================================")
print("REDE CRIADA A PARTIR DO CSV")
print("================================")

print(
    "Quantidade de agentes:",
    network.size()
)

for agent_id, agent in network.agents.items():

    print(
        agent_id,
        "→",
        agent
    )