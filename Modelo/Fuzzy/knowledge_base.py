from skfuzzy import control as ctrl

from Knowledge.rule_loader import RuleLoader


class KnowledgeBase:

    def __init__(self, fuzzy):

        self.fuzzy = fuzzy

        self.loader = RuleLoader("rules.csv")
        self.rules = []
        self.variables = {

            "Rain": self.fuzzy.rain,

            "Traffic": self.fuzzy.traffic,

            "Road": self.fuzzy.road,

            "Speed": self.fuzzy.speed

        }

    def create_rules(self):
        self.rules.clear()
        rows = self.loader.load()

        rules = []

        for row in rows:

            if row["Implementada"].upper() != "TRUE":
                continue

            rules.append(
                self.build_rule(row)
            )

        return rules

    def build_rule(self, row):

        antecedent = None

        conditions = []

        for column, variable in self.variables.items():

            value = row[column].strip()

            if value == "":
                continue

            term = variable[value]

            conditions.append({
                "variable": column,
                "term": value
            })

            if antecedent is None:
                antecedent = term
            else:
                antecedent = antecedent & term

        consequent_name = row["Delay"].strip()

        consequent = self.fuzzy.delay[consequent_name]

        rule = ctrl.Rule(
            antecedent,
            consequent,
            label=row["ID"]
        )

        self.rules.append({

            "id": row["ID"],
            "group": row["Grupo"],
            "conditions": conditions,
            "output": consequent_name,
            "rule": rule

        })

        return rule