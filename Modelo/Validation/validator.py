from Validation.coverage import CoverageAnalyzer
from Validation.classifier import DelayClassifier
from Validation.test_generator import TestGenerator

from Fuzzy.inference_analyzer import InferenceAnalyzer
from Validation.consistency import ConsistencyAnalyzer
import io
from contextlib import redirect_stdout


class FuzzyValidator:

    def __init__(self, fuzzy):
        self.fuzzy = fuzzy

    def run(self):

        results = []

        coverage = CoverageAnalyzer(
            self.fuzzy.knowledge
        )
        consistency = ConsistencyAnalyzer(
    self.fuzzy.knowledge
)

        analyzer = InferenceAnalyzer(
            self.fuzzy
        )

        generator = TestGenerator(
            self.fuzzy
        )

        # Gera automaticamente os testes
        tests = generator.generate(
            self.fuzzy.knowledge.rules
        )

        print()
        print("=" * 60)
        print("INICIANDO VALIDAÇÃO")
        print("=" * 60)

        # ==================================================
    # ARQUIVO DE DIAGNÓSTICO
    # ==================================================

        report_file = open(
            "diagnostico_validacao.txt",
            "w",
            encoding="utf-8"
        )

        report_file.write("=" * 70 + "\n")
        report_file.write(
            "DIAGNÓSTICO COMPLETO DA VALIDAÇÃO FUZZY\n"
        )
        report_file.write("=" * 70 + "\n\n")

        # ==================================================
        # ANÁLISE DA BASE DE REGRAS
        # ==================================================

        captured_rules_analysis = io.StringIO()

        with redirect_stdout(captured_rules_analysis):

            self.fuzzy.knowledge.analyze_rules()

        report_file.write(
            captured_rules_analysis.getvalue()
        )

        report_file.write("\n\n")

        # ==================================================
        # EXECUÇÃO DOS TESTES
        # ==================================================

        for test in tests:

            try:

                # ------------------------------------------
                # EXECUTA O FUZZY
                # ------------------------------------------

                result = self.fuzzy.compute(
                    test["context"]
                )

                delay = result["delay"]
                fallback = result["fallback"]

            except Exception as error:

                report_file.write("\n")
                report_file.write("=" * 70 + "\n")
                report_file.write(
                    f"ERRO NO TESTE {test['id']}\n"
                )
                report_file.write("=" * 70 + "\n")

                report_file.write(
                    f"Contexto: {test['context']}\n"
                )

                report_file.write(
                    f"Erro: {error}\n"
                )

                raise

            # ------------------------------------------
            # ANALISA REGRAS ATIVADAS
            # ------------------------------------------

            activated = analyzer.analyze(
                test["context"]
            )

            coverage.register(
                activated
            )

            # ------------------------------------------
            # CLASSIFICA RESULTADO
            # ------------------------------------------

            predicted = DelayClassifier.classify(
                delay
            )

            passed = (
                predicted == test["expected"]
            )

            # ==================================================
            # DIAGNÓSTICO COMPLETO
            # ==================================================

            report_file.write("\n")
            report_file.write("=" * 70 + "\n")
            report_file.write(
                f"TESTE {test['id']}\n"
            )
            report_file.write("=" * 70 + "\n")

            report_file.write(
                f"Descrição : {test['description']}\n"
            )

            report_file.write(
                f"Esperado  : {test['expected']}\n"
            )

            report_file.write(
                f"Obtido    : {predicted}\n"
            )

            report_file.write(
                f"Delay     : {delay:.2f}\n"
            )

            report_file.write(
                f"Origem    : "
                f"{'FALLBACK' if fallback else 'FUZZY'}\n"
            )

            # ------------------------------------------
            # CONTEXTO
            # ------------------------------------------

            report_file.write("\n")
            report_file.write("Contexto utilizado:\n")

            for key, value in test["context"].items():

                report_file.write(
                    f"  {key:<18} = {value}\n"
                )

            # ------------------------------------------
            # REGRAS ATIVADAS
            # ------------------------------------------

            report_file.write("\n")
            report_file.write("Regras ativadas:\n")

            found = False

            for rule in activated:

                activation = rule["activation"]

                if activation < 0.01:
                    continue

                found = True

                report_file.write(
                    f"  {rule['id']:<6}"
                    f" -> {rule['output']:<12}"
                    f" μ={activation:.3f}\n"
                )

                # Mostra as condições da regra
                report_file.write(
                    "     Condições:\n"
                )

                for condition in rule["conditions"]:

                    report_file.write(
                        f"       "
                        f"{condition['variable']:<10}"
                        f" -> "
                        f"{condition['term']:<12}"
                        f" μ={condition['membership']:.3f}\n"
                    )

            if not found:

                report_file.write(
                    "  Nenhuma regra significativamente ativada.\n"
                )

            # ------------------------------------------
            # STATUS
            # ------------------------------------------

            report_file.write("\n")

            if passed:

                report_file.write(
                    "STATUS: PASS\n"
                )

            else:

                report_file.write(
                    "STATUS: FAIL\n"
                )

            report_file.write("-" * 70 + "\n")

            # ------------------------------------------
            # SALVA RESULTADO
            # ------------------------------------------

            results.append({

                "id": test["id"],

                "description":
                    test["description"],

                "expected":
                    test["expected"],

                "predicted":
                    predicted,

                "delay":
                    delay,

                "fallback":
                    fallback,

                "passed":
                    passed

            })

        # ==================================================
        # RELATÓRIO DE COBERTURA
        # ==================================================

        report_file.write("\n")
        report_file.write("=" * 70 + "\n")
        report_file.write("RELATÓRIO DE COBERTURA\n")
        report_file.write("=" * 70 + "\n")

        # CoverageAnalyzer atualmente imprime diretamente
        # no console. Capturamos essa saída e colocamos no TXT.

        captured_output = io.StringIO()

        with redirect_stdout(captured_output):

            coverage.report()

        coverage_text = captured_output.getvalue()

        report_file.write(
            coverage_text
        )

        # Fecha arquivo
        report_file.close()

        # ==================================================
        # MENSAGEM NO CONSOLE
        # ==================================================

        print()
        print(
            "Diagnóstico completo salvo em:"
        )

        print(
            "diagnostico_validacao.txt"
        )

        # ------------------------------------------
        # ANÁLISE DE CONSISTÊNCIA
        # ------------------------------------------

        consistency.report()
    #N AGUENTO MAIS
        return results


def print_report(results):

    print()
    print("=" * 70)
    print("FUZZY VALIDATION REPORT")
    print("=" * 70)

    passed = 0
    fallback_count = 0

    for result in results:

        if result["passed"]:

            status = "PASS"
            passed += 1
        #print( "passou for if 1.txt")
        else:

            status = "FAIL"

        if result["fallback"]:

            fallback_count += 1
            source = "FALLBACK"

        else:

            source = "FUZZY"

        print(
            f'{result["id"]:<7} | '
            f'{status:<5} | '
            f'{result["expected"]:<12} | '
            f'{result["predicted"]:<12} | '
            f'{result["delay"]:>6.2f} | '
            f'{source}'
        )

    total = len(results)

    print()
    print("-" * 70)

    print(f"Total   : {total}")
    print(f"Passed  : {passed}")
    print(f"Failed  : {total - passed}")

    if total > 0:

        print(
            f"Accuracy: "
            f"{passed / total * 100:.2f}%"
        )

        print(
            f"Fallbacks: "
            f"{fallback_count}"
        )

        print(
            f"Cobertura efetiva: "
            f"{(total - fallback_count) / total * 100:.2f}%"
        )

    print("=" * 70)