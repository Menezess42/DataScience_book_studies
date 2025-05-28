# Muitas técnicas são sensíveis à escala de dados.
# Alturas, e queremos identificar clusters de portes físicos

# Intuitivamente queremos que os clusters representem pontos próximos uns dos outros.

from chap4_linear_algebra.linear_algebra import Vector, Vectors

distance = Vectors()
distance = distance.distance2

# Se medirmos em polegadas o vizinho mais próximo de B é A

a_to_b = distance([63, 150], [67, 160])
print(a_to_b)
a_to_c = distance([63, 150], [70, 171])
print(a_to_c)
b_to_c = distance([67, 160], [70, 171])
print(b_to_c)

# But if we mesure in cm than B to C
a_to_b = distance([160, 150], [170.2, 160])
print(a_to_b)
a_to_c = distance([160, 150], [177.8, 171])
print(a_to_c)
b_to_c = distance([170.2, 160], [177.8, 171])
print(b_to_c)


# Por isso, quando as dimensões não são comparáveis entre si, às vezes redimensionamos
# os dados para que cada dimensão tenha média 0 e desvio-padrão 1. Isso efetivamente
# elimina as unidades.

# Para começar, computaremos a mean e o standard_deviation de cada posição:
from typing import List, Tuple

from chap5_statisc.statisc import Dispersion


def scale(data: List[Vector]) -> Tuple[Vector, Vector]:
    dim = len(data[0])
    n = len(data)

    vector_sum = Vectors()
    vector_sum = vector_sum.vector_sum
    sums = vector_sum(data)

    means = [s / n for s in sums]  # ← média verdadeira

    standard_deviation = Dispersion()
    standard_deviation = standard_deviation.standard_deviation

    stdevs = [standard_deviation([vector[i] for vector in data]) for i in range(dim)]

    return means, stdevs


vectors = [[-3, -1, 1], [-1, 0, 1], [1, 1, 1]]
means, stdenvs = scale(vectors)
print(f"means: {means}")
print(f"stdenvs: {stdenvs}")
assert means == [-1, 0, 1]
assert stdenvs == [2, 1, 0]


# Agora criamos um novo conjunto de dados:
def rescale(data: List[Vector]) -> List[Vector]:
    """
    Redimensiona os dados de entrada para que cada
    posição tenha média 0 e desvio-padrão 1. (deixa a posição
                                                  como está se o
                                                  desvio padrão for 0.)
    """
    dim = len(data[0])
    means, stdevs = scale(data)

    # Faça uma cópia de cada vetor
    rescaled = [v[:] for v in data]

    for v in rescaled:
        for i in range(dim):
            if stdevs[i] > 0:
                v[i] = (v[i] - means[i]) / stdevs[i]

    return rescaled

means, stdevs = scale(rescale(vectors))
assert means == [0, 0, 1]
assert stdevs == [1, 1, 0]

# Devemos usar o bom senso. Se filtrarmos apenas as pessoas com alturas entre 69.5
# e 70.5 polegadas em um enorme conjunto de dados sobre alturas e pesos, muito
# provavelmente (dependendo da pergunta em questão) a variação resultante será apenas
# ruído. Talvez não seja boa ideia colocar esse desvio-padrão em pé de igualdade com
# os desvios das outras dimensões.
