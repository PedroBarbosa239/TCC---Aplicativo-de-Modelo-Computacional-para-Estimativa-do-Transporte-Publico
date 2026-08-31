import csv


class RouteLoader:

    def __init__(self, file_path):

        self.file_path = file_path
        self.routes = []


    # ==========================================
    # CARREGA AS ROTAS
    # ==========================================

    def load(self):

        self.routes = []

        with open(
            self.file_path,
            "r",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                route = {
                    "route_id": row["route_id"],
                    "stop_id": row["stop_id"],
                    "stop_order": int(
                        row["stop_order"]
                    )
                }

                self.routes.append(route)

        return self.routes


    # ==========================================
    # BUSCA UMA LINHA
    # ==========================================

    def get_route(self, route_id):

        route = [

            item

            for item in self.routes

            if item["route_id"] == route_id

        ]

        return sorted(
            route,
            key=lambda item: item["stop_order"]
        )


    # ==========================================
    # LISTA AS LINHAS EXISTENTES
    # ==========================================

    def get_route_ids(self):

        return sorted(
            set(
                item["route_id"]
                for item in self.routes
            )
        )