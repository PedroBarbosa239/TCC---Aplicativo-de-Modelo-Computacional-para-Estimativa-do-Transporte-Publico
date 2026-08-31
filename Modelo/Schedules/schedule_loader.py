import csv
from datetime import datetime


class ScheduleLoader:

    def __init__(self, file_path):

        self.file_path = file_path
        self.schedules = []

    # ==========================================
    # CARREGA OS HORÁRIOS
    # ==========================================

    def load(self):

        self.schedules = []

        with open(
            self.file_path,
            "r",
            encoding="utf-8",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                schedule = {
                    "route_id": row["route_id"].strip(),
                    "direction": row["direction"].strip(),
                    "start_time": row["start_time"].strip()
                }

                self.schedules.append(schedule)

        return self.schedules

    # ==========================================
    # QUANTIDADE DE HORÁRIOS
    # ==========================================

    def size(self):

        return len(self.schedules)

    # ==========================================
    # LISTA HORÁRIOS DE UMA LINHA
    # ==========================================

    def get_route_schedules(self, route_id, direction=None):

        schedules = [
            item
            for item in self.schedules
            if item["route_id"] == str(route_id)
        ]

        if direction is not None:
            schedules = [
                item
                for item in schedules
                if item["direction"] == direction
            ]

        return sorted(
            schedules,
            key=lambda item: self._to_minutes(item["start_time"])
        )

    # ==========================================
    # PRÓXIMA SAÍDA
    # ==========================================

    def get_next_departure(self, route_id, current_time, direction=None):

        schedules = self.get_route_schedules(
            route_id=route_id,
            direction=direction
        )

        if not schedules:
            return None

        current_minutes = self._to_minutes(current_time)

        for schedule in schedules:

            departure_minutes = self._to_minutes(schedule["start_time"])

            if departure_minutes >= current_minutes:
                return schedule

        return schedules[0]

    # ==========================================
    # CONVERTE HH:MM PARA MINUTOS
    # ==========================================

    @staticmethod
    def _to_minutes(value):

        if value is None:
            return 0

        if isinstance(value, (int, float)):
            return int(value)

        try:
            parsed = datetime.strptime(str(value), "%H:%M")
            return parsed.hour * 60 + parsed.minute
        except ValueError:
            return 0
