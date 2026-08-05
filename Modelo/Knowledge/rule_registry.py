class RuleRegistry:

    def __init__(self):
        self.rules = []

    def register(self, rule_info):
        self.rules.append(rule_info)

    def all(self):
        return self.rules

    def clear(self):
        self.rules.clear()