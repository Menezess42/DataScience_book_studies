# Imagine que escolhemos um número k = 3 ou 5.
# Para classificar novos pontos de dados, devemos encontrar os k
# pontos rotulados mais próximos e recebermos seus votos na nova
# saída.

from collections import Counter

# Função que conta votos:
from typing import List


def raw_majority_vote(labels: List[str]) -> str:
    votes = Counter(labels)
    winner, _ = votes.most_common(1)[0]
    return winner


assert raw_majority_vote(["a", "b", "c", "b"]) == "b"


# Mas essa abordagem não lida bem com empates como por exemplo se
# tivessemos ["a", "b", "c", "b", "a"]

# Neste caso, temos várias opções:
# - Escolher aleatoriamente um dos vencedores;
# - Ponderar os votos com base na distância e escolher o vencedor ponderado;
# - Reduzir k até encontrar um só vencedor;


def majority_vote(labels: List[str]) -> str:
    """
    Supõe que os rótulos estão classificados do mais próximo para o mais
    distante.
    """
    vote_counts = Counter(labels)
    winner, winner_count = vote_counts.most_common(1)[0]
    num_winners = len(
        [count for count in vote_counts.values() if count == winner_count]
    )

    if num_winners == 1:
        return winner  # Vencedor úncio, então retorna isso
    else:
        return majority_vote(labels[:-1])  # Tente novamente sem o mais distante


# Empate, então primeiro analisa 4, depois 'b'
assert majority_vote(["a", "b", "c", "b", "a"]) == "b"


# Com essa função é fácil criar um classificador
from typing import NamedTuple

from chap4_linear_algebra.linear_algebra import Vector, Vectors

vec = Vectors()

class LabelPoint(NamedTuple):
    point: Vector
    label: str


def knn_classify(k: int,
                 labeled_points: List[LabelPoint],
                 new_point: Vector) -> str:
    # Classifique os pontos rotulados do mais próximo par o mais
    # distante.
    by_distance = sorted(labeled_points,
                         key=lambda lp: vec.distance2(lp.point, new_point))

    # Encontre os rótulos dos k mais próximos
    k_nearest_labels = [lp.label for lp in by_distance[:k]]

    # E recebe seus votos
    return majority_vote(k_nearest_labels)



### Exemplo conjunto Iris
import requests

data = requests.get("https://archive.ics.uci.edu/ml/machine-learning-database/iris/iris.data")

with open('iris.dat', 'w') as f:
    f.write(data.text)


