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

    # ==========================================================
    # ANÁLISE DA BASE DE REGRAS
    # ==========================================================

    def analyze_rules(self):

        rows = self.loader.load()

        rules = []

        for row in rows:

            if row["Implementada"].upper() != "TRUE":
                continue

            conditions = {}

            for column in self.variables:

                value = row[column].strip()

                if value != "":
                    conditions[column] = value

            rules.append({

                "id": row["ID"],
                "group": row["Grupo"],
                "conditions": conditions,
                "output": row["Delay"].strip()

            })

        print("\n" + "=" * 70)
        print("ANÁLISE DA BASE DE REGRAS")
        print("=" * 70)

        print(f"\nTotal de regras analisadas: {len(rules)}")

        self._find_exact_conflicts(rules)
        self._find_exact_duplicates(rules)
        self._find_overlaps(rules)

    # ==========================================================
    # CONFLITOS EXATOS
    # ==========================================================

    def _find_exact_conflicts(self, rules):

        groups = {}

        for rule in rules:

            key = tuple(
                sorted(rule["conditions"].items())
            )

            groups.setdefault(key, []).append(rule)

        conflicts = []

        for key, group in groups.items():

            outputs = set(
                rule["output"]
                for rule in group
            )

            if len(outputs) > 1:
                conflicts.append((key, group))

        print("\n" + "-" * 70)
        print("1. CONFLITOS EXATOS")
        print("-" * 70)

        if not conflicts:

            print("Nenhum conflito exato encontrado.")

            return

        for key, group in conflicts:

            ids = ", ".join(
                rule["id"]
                for rule in group
            )

            outputs = ", ".join(
                sorted(
                    set(
                        rule["output"]
                        for rule in group
                    )
                )
            )

            print(f"\nRegras: {ids}")

            print("Condições:")

            for variable, term in key:
                print(f"  {variable} = {term}")

            print(f"Consequentes: {outputs}")

    # ==========================================================
    # DUPLICATAS
    # ==========================================================

    def _find_exact_duplicates(self, rules):

        groups = {}

        for rule in rules:

            key = (
                tuple(sorted(rule["conditions"].items())),
                rule["output"]
            )

            groups.setdefault(key, []).append(rule)

        duplicates = []

        for key, group in groups.items():

            if len(group) > 1:
                duplicates.append((key, group))

        print("\n" + "-" * 70)
        print("2. REGRAS DUPLICADAS")
        print("-" * 70)

        if not duplicates:

            print("Nenhuma regra duplicada encontrada.")

            return

        for key, group in duplicates:

            ids = ", ".join(
                rule["id"]
                for rule in group
            )

            print(f"\nRegras: {ids}")

            print("Condições:")

            for variable, term in key[0]:
                print(f"  {variable} = {term}")

            print(f"Consequente: {key[1]}")

    # ==========================================================
    # SOBREPOSIÇÕES
    # ==========================================================

    def _find_overlaps(self, rules):

        overlaps = []

        for rule_a in rules:

            for rule_b in rules:

                if rule_a["id"] == rule_b["id"]:
                    continue

                conditions_a = rule_a["conditions"]
                conditions_b = rule_b["conditions"]

                # A precisa ser uma regra mais específica que B
                if not self._is_subset(
                    conditions_b,
                    conditions_a
                ):
                    continue

                if len(conditions_a) <= len(conditions_b):
                    continue

                overlaps.append(
                    (rule_b, rule_a)
                )

        # Evita duplicar A -> B e B -> A
        unique = []

        seen = set()

        for general, specific in overlaps:

            key = (
                general["id"],
                specific["id"]
            )

            if key in seen:
                continue

            seen.add(key)

            unique.append(
                (general, specific)
            )

        print("\n" + "-" * 70)
        print("3. SOBREPOSIÇÕES")
        print("-" * 70)

        if not unique:

            print("Nenhuma sobreposição encontrada.")

            return

        for general, specific in unique:

            print(
                f"\n{general['id']} "
                f"({general['output']})"
                f"  ⊃  "
                f"{specific['id']} "
                f"({specific['output']})"
            )

            print("  Regra geral:")

            for variable, term in general["conditions"].items():

                print(
                    f"    {variable} = {term}"
                )

            print("  Regra específica:")

            for variable, term in specific["conditions"].items():

                print(
                    f"    {variable} = {term}"
                )

    # ==========================================================
    # TESTE DE SUBCONJUNTO
    # ==========================================================

    @staticmethod
    def _is_subset(general, specific):

        for variable, term in general.items():

            if specific.get(variable) != term:
                return False

        return True