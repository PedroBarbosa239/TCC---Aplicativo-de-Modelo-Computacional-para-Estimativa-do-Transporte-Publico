import skfuzzy as fuzz


class InferenceAnalyzer:

    def __init__(self, fuzzy):

        self.fuzzy = fuzzy

    def analyze(self, context):

        activated_rules = []

        for rule in self.fuzzy.knowledge.rules:

            activations = []

            for condition in rule["conditions"]:

                variable_name = condition["variable"]
                term_name = condition["term"]

                variable = self.get_variable(variable_name)

                value = self.get_context_value(
                    variable_name,
                    context
                )

                membership = fuzz.interp_membership(
                    variable.universe,
                    variable[term_name].mf,
                    value
                )

                activations.append(
                    {
                        "variable": variable_name,
                        "term": term_name,
                        "value": value,
                        "membership": membership
                    }
                )

            activation = min(
                item["membership"]
                for item in activations
            )

            if activation > 0:

                activated_rules.append(
                    {
                        "id": rule["id"],
                        "group": rule["group"],
                        "activation": activation,
                        "output": rule["output"],
                        "conditions": activations
                    }
                )

        activated_rules.sort(
            key=lambda r: r["activation"],
            reverse=True
        )

        return activated_rules

    def get_variable(self, name):

        mapping = {

            "Rain": self.fuzzy.rain,

            "Traffic": self.fuzzy.traffic,

            "Road": self.fuzzy.road,

            "Speed": self.fuzzy.speed

        }

        return mapping[name]

    def get_context_value(self, name, context):

        mapping = {

            "Rain": context["rain"],

            "Traffic": context["traffic"],

            "Road": context["road_flow"],

            "Speed": context["speed"]

        }

        return mapping[name]