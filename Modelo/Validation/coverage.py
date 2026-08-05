class CoverageAnalyzer:

    def __init__(self, knowledge):

        self.knowledge = knowledge
        self.used_rules = set()

    def register(self, activated_rules):

        for rule in activated_rules:

            self.used_rules.add(rule["id"])

    def report(self):

        total = len(self.knowledge.rules)

        used = len(self.used_rules)

        unused = total - used

        print()
        print("=" * 60)
        print("RULE COVERAGE")
        print("=" * 60)

        print(f"Total rules : {total}")
        print(f"Used rules  : {used}")
        print(f"Unused      : {unused}")
        print(f"Coverage    : {used / total * 100:.2f}%")

        print()
        print("Unused rules")
        print("-" * 60)

        for rule in self.knowledge.rules:

            if rule["id"] not in self.used_rules:

                print(
                    f'{rule["id"]} [{rule["group"]}]'
                )