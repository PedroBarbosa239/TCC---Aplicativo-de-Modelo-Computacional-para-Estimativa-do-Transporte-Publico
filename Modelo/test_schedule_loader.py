from Schedules.schedule_loader import ScheduleLoader


# ==========================================
# CARREGA HORÁRIOS
# ==========================================

loader = ScheduleLoader(
    "Data/schedules.csv"
)

schedules = loader.load()


# ==========================================
# TESTE DOS HORÁRIOS
# ==========================================

print()
print("================================")
print("HORÁRIOS CARREGADOS")
print("================================")

print(
    f"Quantidade de horários: "
    f"{loader.size()}"
)


# ==========================================
# HORÁRIOS DA LINHA 101
# ==========================================

route_101 = loader.get_route_schedules(
    "101"
)

print()
print("================================")
print("HORÁRIOS DA LINHA 101")
print("================================")

for schedule in route_101:

    print(
        f"Linha: {schedule['route_id']} | "
        f"Sentido: {schedule['direction']} | "
        f"Saída: {schedule['start_time']}"
    )


# ==========================================
# TESTE DA PRÓXIMA SAÍDA
# ==========================================

next_departure = loader.get_next_departure(
    route_id="101",
    current_time="04:35"
)

print()
print("================================")
print("PRÓXIMA SAÍDA")
print("================================")

if next_departure:

    print(
        f"Linha: {next_departure['route_id']}"
    )

    print(
        f"Sentido: {next_departure['direction']}"
    )

    print(
        f"Horário: {next_departure['start_time']}"
    )

else:

    print("Nenhuma saída encontrada.")