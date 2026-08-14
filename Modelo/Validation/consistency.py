from collections import defaultdict


class ConsistencyAnalyzer:

    def __init__(self, knowledge):
        self.knowledge = knowledge

    def analyze(self):

        groups = defaultdict(list)

        # Agrupa regras pelas condições
        for rule in self.knowledge.rules:

            conditions = []

            for condition in rule["conditions"]:

                conditions.append(
                    (
                        condition["variable"],
                        condition["term"]
                    )
                )

            # Ordena para garantir que a ordem
            # das condições não altere a comparação
            conditions = tuple(sorted(conditions))

            groups[conditions].append(rule)

        conflicts = []

        # Procura grupos com saídas diferentes
        for conditions, rules in groups.items():

            outputs = set(
                rule["output"]
                for rule in rules
            )

            if len(outputs) > 1:

                conflicts.append(
                    {
                        "conditions": conditions,
                        "rules": rules,
                        "outputs": outputs
                    }
                )

        return conflicts

    def report(self):

        conflicts = self.analyze()

        print()
        print("=" * 70)
        print("ANÁLISE DE CONSISTÊNCIA DAS REGRAS")
        print("=" * 70)

        print(
            f"\nTotal de regras      : "
            f"{len(self.knowledge.rules)}"
        )

        print(
            f"Conflitos encontrados: "
            f"{len(conflicts)}"
        )

        if not conflicts:

            print()
            print("Nenhum conflito encontrado.")
            print("=" * 70)

            return conflicts

        for index, conflict in enumerate(
            conflicts,
            start=1
        ):

            print()
            print("-" * 70)
            print(
                f"CONFLITO {index}"
            )
            print("-" * 70)

            print()
            print("Condições:")

            for variable, term in conflict["conditions"]:

                print(
                    f"  {variable:<10} -> {term}"
                )

            print()
            print("Regras:")

            for rule in conflict["rules"]:

                print(
                    f"  {rule['id']:<6} "
                    f"-> {rule['output']}"
                )

            print()
            print(
                "Resultado: "
                "CONFLITO ENTRE SAÍDAS"
            )

        print()
        print("=" * 70)

        return conflicts