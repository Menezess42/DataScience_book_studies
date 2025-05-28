# Às vezes, as dimensões "reais" (ou úteis) dos dados não
# correspondem às dimensões que conhecemos. Por exemplo, veja o
# conjunto de dados indicado na Figura 10-6

### PCA:
### Principal Component Analysis ###
##### Extrair uma ou mais dimensões que concentram a maior variação
##### possível dos dados.
####> Na prática, NÃO É RECOMENDÁVEL usar essa técnica em um conjunto
####> de dados com tão poucas dimensões. A redução de dimensionalidade é
####> mais útil quando o conjunto de dados tem um grande núemro de dimensões
####> e queremos encontrar um pequeno subconjunto que capture a maior parte da
####> variação.

from typing import List

import tqdm

# First we translate the data to make sure that each dimension has mean 0.
from chap4_linear_algebra.linear_algebra import Vector, Vectors

vec = Vectors()


def de_mean(data: List[Vector]) -> List[Vector]:
    """Centraliza novamente os dados para que
    todas as dimensões tenham média zero."""
    vec = Vectors()
    mean = vec.vector_mean(data)
    return [vec.subtract(vector, mean) for vector in data]


# Para X com média definida, perguntamos qual é a direção que
# captura a maior variação nos dados.
def direction(w: Vector) -> Vector:
    vec = Vectors()
    mag = vec.magnitude(w)
    return [w_i / mag for w_i in w]


# Considerando um vetor w diferente de zero, calculamos a variação do
# conjunto de dados na direção determinada por w:
def directional_variance(data: List[Vector], w: Vector) -> float:
    """
    Retorna a variação de x na direção w
    """
    w_dir = direction(w)
    vec = Vectors()
    return sum(vec.dot(v, w_dir) ** 2 for v in data)


# Encontraremos a direção que maximiza essa variação. Para isso, usaremos
# o gradiente descendente assim que tivermos a função de gradiente
def directional_variance_gradient(data: List[Vector], w: Vector) -> Vector:
    """
    O gradiente da variação direcional em relação a w
    """
    w_dir = direction(w)
    vec = Vectors()
    return [sum(2 * vec.dot(v, w_dir) * v[i] for v in data) for i in range(len(w))]


# O primeiro componente importante que temos é a direção que maximiza a função
# directional_variance
def first_principal_component(
    data: List[Vecotr], n: int = 100, step_size: float = 0.1
) -> Vector:
    # Start with a random value
    guess = [1.0 for _ in data[0]]
    with tqdm.trange(n) as t:
        for _ in t:
            dv = directional_variance(data, guess)
            gradient = directional_variance_gradient(data, guess)
            t.set_description(f"dv: {dv:.3f}")

    return direction(guess)


# Depois de determinar a direção (primeiro componente importante), projetamos os
# dados nela para encontrar os valores desse componente:
def project(v: Vector, w: Vector) -> Vector:
    """retorna a projeção de v na direção w"""
    projection_length = vec.dot(v, w)
    return vec.scalar_multiply(projection_length, w)


# para encontrar mais componentes, primeiro temos que remover as projeções dos dados
def remove_projection_from_vector(v: Vector, w: Vector) -> Vector:
    """
    Projeta v em w e subtrai o resultado de v
    """
    return vec.subtract(v, project(v, w))


def remove_projection(data: List[Vector], w: Vector) -> List[Vector]:
    return [remove_projection_from_vector(v, w) for v in data]


# Livro: Como o conjunto de dados do exemplo é bidimensional, depois
# que removemos o primeiro componente, a estrutura restante será efetivamente
# unidimensional.
# Neste ponto para encontrar o próximo componente importante, repetimos
# o processo no resultado de remove_projection


# Em um conjunto de dados com muitas dimensões, podemos fazer iterações
# para encontrar qualquer número de componentes:
def pca(data: List[Vector], num_components: int) -> List[Vector]:
    components: List[Vector] = []
    for _ in range(num_components):
        component = first_principal_component(data)
        components.append(component)
        data = remove_projection(data, component)

    return components


# Depois transformamos os dados no espaço com menos dimensões criado pelos
# components:
def transform_vector(v: Vector, components: List[Vector]) -> Vector:
    return [vec.dot(v, w) for w in components]


def transform(data: List[Vector], components: List[Vector]) -> List[Vector]:
    return [transform_vector(v, components) for v in data]

# Importancia da técnica:
# 1. ajuda na limpeza dos dados, eliminando as dimensões de ruídos e consolidando
# as dimensões altamente correlacionadas.
# 2. Depois de extrair uma representação com poucas dimensões dos dados, é possível
# aplicar uma variedade de técnicas que não funcionam tão bem em dados com muitas
# dimensões.
