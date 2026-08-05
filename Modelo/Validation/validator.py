from Validation import coverage
from Validation.test_cases import TEST_CASES
from Validation.classifier import DelayClassifier

from Validation.coverage import CoverageAnalyzer
from Fuzzy.inference_analyzer import InferenceAnalyzer


class FuzzyValidator:

    def __init__(self, fuzzy):

        self.fuzzy = fuzzy


    def run(self):

        results = []

        coverage = CoverageAnalyzer(
            self.fuzzy.knowledge
        )

        analyzer = InferenceAnalyzer(
            self.fuzzy
        )

        for test in TEST_CASES:

            delay = self.fuzzy.compute(
                test["context"]
            )

            activated = analyzer.analyze(
            test["context"]
            )

            coverage.register(
            activated
            )

            predicted = DelayClassifier.classify(delay)

            results.append({

                "id": test["id"],

                "description": test["description"],

                "expected": test["expected"],

                "predicted": predicted,

                "delay": delay,

                "passed": predicted == test["expected"]

            })
        coverage.report()
        return results

def print_report(results):

        print()
        print("=" * 60)
        print("FUZZY VALIDATION REPORT")
        print("=" * 60)

        passed = 0

        for result in results:

            status = "PASS" if result["passed"] else "FAIL"

            if result["passed"]:
                passed += 1

            print(
                f'{result["id"]} | '
                f'{status:<5} | '
                f'{result["predicted"]:<12} | '
                f'{result["delay"]:.2f}'
            )

        print()
        print(f"Passed : {passed}")
        print(f"Failed : {len(results)-passed}")
        print(f"Accuracy: {passed/len(results)*100:.2f}%")
        print("=" * 60)
    