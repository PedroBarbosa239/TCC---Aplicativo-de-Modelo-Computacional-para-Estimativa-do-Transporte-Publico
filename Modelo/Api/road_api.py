import requests

OVERPASS = "https://overpass-api.de/api/interpreter"


def get_road_type(lat, lon):
    query = f"""
    [out:json];
    way(around:30,{lat},{lon})["highway"];
    out tags;
    """

    try:
        response = requests.post(
            OVERPASS,
            data=query,
            headers={
                "User-Agent": "TCC-Modelo/1.0",
                "Content-Type": "text/plain"
            },
            timeout=10
        )



        response.raise_for_status()

        data = response.json()

        if not data.get("elements"):
            return {"road_type": "unknown"}

        tags = data["elements"][0].get("tags", {})

        return {
            "road_type": tags.get("highway", "unknown")
        }

    except requests.exceptions.RequestException as e:
        print(f"Erro ao consultar Overpass API: {e}")
        return {"road_type": "unknown"}

    except ValueError:
        print("A resposta da API não é um JSON válido.")
        return {"road_type": "unknown"}