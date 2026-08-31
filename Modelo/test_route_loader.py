from Data.route_loader import RouteLoader


loader = RouteLoader(
    "Data/routes.csv"
)

loader.load()


print()
print("================================")
print("TESTE DO ROUTE LOADER")
print("================================")

print(
    "Linhas encontradas:",
    loader.get_route_ids()
)


for route_id in loader.get_route_ids():

    route = loader.get_route(
        route_id
    )

    print()
    print(
        f"Linha {route_id}:"
    )

    for stop in route:

        print(
            f"  {stop['stop_order']} "
            f"→ {stop['stop_id']}"
        )