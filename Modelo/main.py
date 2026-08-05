from Api.weather_api import get_weather
from Api.traffic_api import get_traffic
from Api.road_api import get_road_type

from Normalization.normalize import ContextNormalizer

from Fuzzy.delay_fuzzy import DelayFuzzySystem
from Fuzzy.inference_analyzer import InferenceAnalyzer

from Validation.validator import (
    FuzzyValidator,
    print_report
)



LAT = -22.2231
LON = -54.8120


# =====================================================
# OBTÉM CONTEXTO
# =====================================================

context = {}

context.update(get_weather(LAT, LON))
context.update(get_traffic(LAT, LON))
context.update(get_road_type(LAT, LON))

context["previous_delay"] = 2
context["previous_confidence"] = 90


# =====================================================
# NORMALIZAÇÃO
# =====================================================

normalizer = ContextNormalizer()

normalized = normalizer.normalize(context)

print("Contexto normalizado original:")
print(normalized)


# =====================================================
# TESTE MANUAL
# =====================================================

test_context = normalized["normalized"].copy()

test_context["rain"] = 0
test_context["traffic"] = 0
test_context["speed"] = 15
test_context["road_flow"] = 10

print("\nContexto utilizado no fuzzy:")
print(test_context)


# =====================================================
# MOTOR FUZZY
# =====================================================

fuzzy = DelayFuzzySystem()

delay = fuzzy.compute(test_context)


# =====================================================
# REGRAS CARREGADAS
# =====================================================

print("\n" + "=" * 60)
print("BASE DE CONHECIMENTO")
print("=" * 60)

for rule in fuzzy.knowledge.rules:

    print(
        f'{rule["id"]} '
        f'[{rule["group"]}] '
        f'-> {rule["output"]}'
    )


# =====================================================
# ANÁLISE DA INFERÊNCIA
# =====================================================

analyzer = InferenceAnalyzer(fuzzy)

analysis = analyzer.analyze(test_context)

print("\n" + "=" * 60)
print("REGRAS ATIVADAS")
print("=" * 60)

for rule in analysis:

    # mostra apenas regras relevantes
    if rule["activation"] < 0.10:
        continue

    print()

    print(f'ID...........: {rule["id"]}')
    print(f'Grupo........: {rule["group"]}')
    print(f'Ativação.....: {rule["activation"]:.3f}')
    print(f'Conclusão....: {rule["output"]}')

    print("Condições:")

    for cond in rule["conditions"]:

        print(
            f'   {cond["variable"]:8}'
            f' -> {cond["term"]:12}'
            f' μ={cond["membership"]:.3f}'
        )

    print("-" * 60)


# =====================================================
# RESULTADO FINAL
# =====================================================

print("\n" + "=" * 60)
print("RESULTADO FUZZY")
print("=" * 60)

print(f"Delay estimado: {delay:.2f}")

validator = FuzzyValidator(fuzzy)

results = validator.run()

print_report(results)
