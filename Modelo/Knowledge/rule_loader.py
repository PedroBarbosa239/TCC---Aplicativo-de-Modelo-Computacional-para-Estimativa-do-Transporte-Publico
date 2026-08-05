import csv
from pathlib import Path


class RuleLoader:

    def __init__(self, filename):

        # Pasta onde está este arquivo (Knowledge/)
        base_path = Path(__file__).parent

        # Caminho completo do CSV
        self.filename = base_path / filename

    def load(self):

        rules = []

        with open(
            self.filename,
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                rules.append(row)

        return rules