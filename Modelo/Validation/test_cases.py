TEST_CASES = [

    {
        "id": "T001",
        "description": "Condições ideais",

        "context": {
            "rain": 0,
            "traffic": 0,
            "road_flow": 0,
            "speed": 0
        },

        "expected": "very_early"
    },

    {
        "id": "T002",
        "description": "Trânsito extremo",

        "context": {
            "rain": 0,
            "traffic": 100,
            "road_flow": 100,
            "speed": 100
        },

        "expected": "very_late"
    },

    {
        "id": "T003",
        "description": "Condições médias",

        "context": {
            "rain": 50,
            "traffic": 50,
            "road_flow": 50,
            "speed": 50
        },

        "expected": "on_time"
    },

    {
        "id": "T004",
        "description": "Chuva intensa",

        "context": {
            "rain": 90,
            "traffic": 70,
            "road_flow": 70,
            "speed": 85
        },

        "expected": "very_late"
    },

]