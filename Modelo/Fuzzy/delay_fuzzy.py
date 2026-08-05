import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

from .knowledge_base import KnowledgeBase
from .database import Database


class DelayFuzzySystem:

    def __init__(self):

        # ==========================
        # UNIVERSO DAS VARIÁVEIS
        # ==========================

        self.database = Database()

        self.rain = self.database.rain
        self.traffic = self.database.traffic
        self.speed = self.database.speed
        self.road = self.database.road
        self.previous_delay = self.database.previous_delay
        self.delay = self.database.delay

        self.knowledge = KnowledgeBase(self)
        self.build_system()

        
    # ==========================================================
    # VISUALIZAÇÃO
    # ==========================================================

    def show_memberships(self):

        self.rain.view()
        self.traffic.view()
        self.speed.view()
        self.road.view()
        self.previous_delay.view()
        self.delay.view()


    def create_rules(self):
        return self.knowledge.create_rules()

    def build_system(self):

        rules = self.create_rules()

        print(f"{len(rules)} regras carregadas.")
        self.control_system = ctrl.ControlSystem(rules)
        self.simulation = ctrl.ControlSystemSimulation(
            self.control_system
        )

    def compute(self, context):

        self.simulation.input["rain"] = context["rain"]
        self.simulation.input["traffic"] = context["traffic"]
        self.simulation.input["speed"] = context["speed"]
        self.simulation.input["road"] = context["road_flow"]

        self.simulation.compute()

        print("\nSaída da simulação:")
        print(self.simulation.output)

        return self.simulation.output["delay"]

if __name__ == "__main__":

    print("Criando sistema...")

    fuzzy = DelayFuzzySystem()

    tests = [

        {
            "name": "Condições ideais",
            "context": {
                "rain": 0,
                "traffic": 0,
                "speed": 0,
                "road_flow": 0
            }
        },

        {
            "name": "Condições médias",
            "context": {
                "rain": 50,
                "traffic": 50,
                "speed": 50,
                "road_flow": 50
            }
        },

        {
            "name": "Condições ruins",
            "context": {
                "rain": 80,
                "traffic": 90,
                "speed": 85,
                "road_flow": 50
            }
        },

        {
            "name": "Trânsito intenso",
            "context": {
                "rain": 10,
                "traffic": 95,
                "speed": 80,
                "road_flow": 70
            }
        }

    ]

    for test in tests:

        result = fuzzy.compute(test["context"])

        print(f'{test["name"]}: {result:.2f}')

   # print("Abrindo gráficos...")
   # fuzzy.show_memberships()
   # print("Fim.")
   # input("Pressione ENTER para sair...")