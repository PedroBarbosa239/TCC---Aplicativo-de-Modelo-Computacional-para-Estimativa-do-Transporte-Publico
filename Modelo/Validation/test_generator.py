import skfuzzy as fuzz


class TestGenerator:

    def __init__(self, fuzzy):

        self.fuzzy = fuzzy

        self.variables = {
            "Rain": self.fuzzy.rain,
            "Traffic": self.fuzzy.traffic,
            "Road": self.fuzzy.road,
            "Speed": self.fuzzy.speed
        }

    # ==========================================================
    # VALOR REPRESENTATIVO DE UM TERMO FUZZY
    # ==========================================================

    def get_representative_value(self, variable, term):

        membership = variable[term].mf

        max_membership = membership.max()

        indices = [
            i
            for i, value in enumerate(membership)
            if value == max_membership
        ]

        index = indices[len(indices) // 2]

        return float(variable.universe[index])

    # ==========================================================
    # GERAÇÃO DOS TESTES
    # ==========================================================

    def generate(self, rules):

        tests = []

        for rule in rules:

            context = {}

            # --------------------------------------------------
            # conditions é uma LISTA
            #
            # Exemplo:
            #
            # [
            #   {"variable": "Rain", "term": "none"},
            #   {"variable": "Traffic", "term": "low"},
            #   {"variable": "Road", "term": "excellent"}
            # ]
            # --------------------------------------------------

            for condition in rule["conditions"]:

                variable_name = condition["variable"]
                term = condition["term"]

                variable = self.variables[variable_name]

                context_key = {
                    "Rain": "rain",
                    "Traffic": "traffic",
                    "Road": "road_flow",
                    "Speed": "speed"
                }[variable_name]

                context[context_key] = (
                    self.get_representative_value(
                        variable,
                        term
                    )
                )

            # --------------------------------------------------
            # Completa variáveis que não aparecem na regra
            #
            # Isso é importante porque uma regra pode ter:
            #
            # Rain + Traffic
            #
            # mas o sistema possui também:
            #
            # Road + Speed
            #
            # --------------------------------------------------

            default_values = {

                "rain": 50.0,

                "traffic": 50.0,

                "road_flow": 50.0,

                "speed": 50.0

            }

            for key, value in default_values.items():

                if key not in context:

                    context[key] = value

            # --------------------------------------------------
            # TESTE
            # --------------------------------------------------

            tests.append({

                "id": f"T_{rule['id']}",

                "rule_id": rule["id"],

                "description":
                    f"Teste representativo da regra {rule['id']}",

                "context": context,

                "expected": rule["output"]

            })

        return tests