from Agents.bus_stop_agent import BusStopAgent
from Agents.agent_network import AgentNetwork
from Agents.agent_message import AgentMessage


# ==========================================
# CRIA A REDE
# ==========================================

network = AgentNetwork()


# ==========================================
# CRIA OS AGENTES
# ==========================================

p001 = BusStopAgent(
    stop_id="P001",
    latitude=-22.2231,
    longitude=-54.8120,
    lines=["101", "103"]
)

p002 = BusStopAgent(
    stop_id="P002",
    latitude=-22.2240,
    longitude=-54.8130,
    lines=["101", "103"]
)

p003 = BusStopAgent(
    stop_id="P003",
    latitude=-22.2250,
    longitude=-54.8140,
    lines=["101"]
)

p004 = BusStopAgent(
    stop_id="P004",
    latitude=-22.2260,
    longitude=-54.8150,
    lines=["103"]
)


# ==========================================
# ADICIONA À REDE
# ==========================================

network.add_agents([
    p001,
    p002,
    p003,
    p004
])


# ==========================================
# CONEXÕES DA LINHA 101
# ==========================================

network.connect_agents(
    "P001",
    "P002",
    route_id="101"
)

network.connect_agents(
    "P002",
    "P003",
    route_id="101"
)


# ==========================================
# CONEXÕES DA LINHA 103
# ==========================================

network.connect_agents(
    "P001",
    "P002",
    route_id="103"
)

network.connect_agents(
    "P002",
    "P004",
    route_id="103"
)


# ==========================================
# CONTEXTO DO PONTO
# ==========================================

context = {

    "raw": {

        "rain": 0.0,
        "visibility": 10000.0,
        "wind_speed": 23.8,

        # Dados utilizados pelo agente
        "current_speed": 30.0,
        "free_speed": 50.0,

        "congestion": 0.0,
        "road_type": "unknown",

        "previous_delay": 0,
        "previous_confidence": 100
    },

    "normalized": {

        "rain": 0.0,
        "visibility": 0.0,
        "wind": 29.75,
        "traffic": 0,
        "speed": 72.727,
        "road_flow": 50,
        "previous_delay": 50,
        "previous_confidence": 100
    }
}


# ==========================================
# TESTE DA VELOCIDADE
# ==========================================

estimated_speed = p002.estimate_speed(
    current_speed=context["raw"]["current_speed"],
    free_speed=context["raw"]["free_speed"]
)


print()
print("================================")
print("VELOCIDADE ESTIMADA")
print("================================")

print(
    f"Velocidade atual: "
    f"{context['raw']['current_speed']:.2f} km/h"
)

print(
    f"Velocidade livre: "
    f"{context['raw']['free_speed']:.2f} km/h"
)

print(
    f"Velocidade utilizada: "
    f"{estimated_speed:.2f} km/h"
)


# ==========================================
# MENSAGEM INICIAL
# ==========================================

message = AgentMessage(
    source_agent="P001",
    route_id="101",
    departure_time="05:00:00",
    arrival_time="05:00:00",
    estimated_delay=0.0,
    confidence=1.0
)


# ==========================================
# P001 → P002
# ==========================================

p002.receive_message(message)

result_p002 = p002.process_trip(
    message,
    context
)


print()
print("================================")
print("VIAGEM P001 → P002")
print("================================")

print(
    f"Linha: {result_p002['route_id']}"
)

print(
    f"Saída: {result_p002['departure_time']}"
)

print(
    f"Agente anterior: "
    f"{result_p002['stop_id'] if False else 'P001'}"
)

print(
    f"Velocidade: "
    f"{result_p002['speed_kmh']:.2f} km/h"
)

print(
    f"Distância: "
    f"{result_p002['distance_meters']:.2f} m"
)

print(
    f"Tempo do trecho: "
    f"{result_p002['travel_time_seconds']:.2f} s"
)

print(
    f"Chegada P002: "
    f"{result_p002['arrival_time']}"
)


# ==========================================
# P002 → P003
# ==========================================

message_p002 = AgentMessage(
    source_agent="P002",
    route_id=result_p002["route_id"],
    departure_time=result_p002["departure_time"],
    arrival_time=result_p002["arrival_time"],
    estimated_delay=result_p002["estimated_delay"],
    confidence=result_p002["confidence"]
)


p003.receive_message(message_p002)

result_p003 = p003.process_trip(
    message_p002,
    context
)


print()
print("================================")
print("VIAGEM P002 → P003")
print("================================")

print(
    f"Linha: {result_p003['route_id']}"
)

print(
    f"Saída da viagem: "
    f"{result_p003['departure_time']}"
)

print(
    f"Chegada anterior: "
    f"{message_p002.arrival_time}"
)

print(
    f"Velocidade: "
    f"{result_p003['speed_kmh']:.2f} km/h"
)

print(
    f"Distância: "
    f"{result_p003['distance_meters']:.2f} m"
)

print(
    f"Tempo do trecho: "
    f"{result_p003['travel_time_seconds']:.2f} s"
)

print(
    f"Chegada P003: "
    f"{result_p003['arrival_time']}"
)


# ==========================================
# TEMPO TOTAL
# ==========================================

total_time = (
    result_p002["travel_time_seconds"]
    +
    result_p003["travel_time_seconds"]
)


print()
print("================================")
print("TEMPO TOTAL DA VIAGEM")
print("================================")

print(
    f"P001 → P002 → P003"
)

print(
    f"Tempo total: "
    f"{total_time:.2f} s"
)

print(
    f"Tempo total: "
    f"{total_time / 60:.2f} minutos"
)


# ==========================================
# MENSAGENS
# ==========================================

print()
print("================================")
print("MENSAGENS DOS AGENTES")
print("================================")

print()
print("P002 recebeu:")

print(
    p002.received_messages
)

print()
print("P003 recebeu:")

print(
    p003.received_messages
)


# ==========================================
# TESTE FINAL
# ==========================================

print()
print("================================")
print("TESTE FINALIZADO")
print("================================")