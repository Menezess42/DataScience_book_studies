# Imagine que escolhemos um número k = 3 ou 5.
# Para classificar novos pontos de dados, devemos encontrar os k
# pontos rotulados mais próximos e recebermos seus votos na nova
# saída.

from collections import Counter
from pathlib import Path

# Função que conta votos:
from typing import List

BASE_DIR = Path(__file__).parent


# subdir/utils.py
def get_resource_path(filename: str) -> Path:

    return BASE_DIR / filename


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


def knn_classify(k: int, labeled_points: List[LabelPoint], new_point: Vector) -> str:
    # Classifique os pontos rotulados do mais próximo par o mais
    # distante.
    by_distance = sorted(
        labeled_points, key=lambda lp: vec.distance2(lp.point, new_point)
    )

    # Encontre os rótulos dos k mais próximos
    k_nearest_labels = [lp.label for lp in by_distance[:k]]

    # E recebe seus votos
    return majority_vote(k_nearest_labels)


### Exemplo conjunto Iris
def run_one():
    import requests

    data = requests.get(
        "https://archive.ics.uci.edu/ml/machine-learning-database/iris/iris.data"
    )

    with open("./iris.dat", "w") as f:
        f.write(data.text)


import csv
from collections import defaultdict

# Vamos começar explorando os dados:
from typing import Dict


def parse_iris_row(row: List[str]) -> LabelPoint:
    """
    Sepal_length, sepal_width, petal_length, petal_width, class
    """
    measurements = [float(value) for value in row[:-1]]
    # A classe é nome composto "Iris-x" queremos só x
    label = row[-1].split("-")[-1]

    return LabelPoint(measurements, label)


iris_data = []
with get_resource_path("./iris.data").open() as f:
    reader = csv.reader(f)
    iris_data = [parse_iris_row(row) for row in reader if row]

# Também agrupamos apenas os pontos espécie/rótulo para plotá-los
points_by_species: Dict[str, List[Vector]] = defaultdict(list)
for iris in iris_data:
    points_by_species[iris.label].append(iris.point)


# Gráfico de dispersão
import matplotlib.pyplot as plt

metrics = ["sepal length", "sepal width", "petal length", "petal width"]
pairs = [(i, j) for i in range(4) for j in range(4) if i < j]
marks = ["+", ".", "x"]  # temos 3 clases, então 3 marcadores

fig, ax = plt.subplots(2, 3)

for row in range(2):
    for col in range(3):
        i, j = pairs[3 * row + col]
        ax[row][col].set_title(f"{metrics[i]} vs {metrics[j]}", fontsize=8)
        ax[row][col].set_xticks([])
        ax[row][col].set_yticks([])

        for mark, (species, points) in zip(marks, points_by_species.items()):
            xs = [point[i] for point in points]
            ys = [point[j] for point in points]
            ax[row][col].scatter(xs, ys, marker=mark, label=species)

ax[-1][-1].legend(loc="lower right", prop={"size": 6})
# plt.savefig(get_resource_path('./scatterPlot.png').as_posix())
# plt.show(get_resource_path("./scatterPlot.png"))

# Podemos observar que, nesses gráficos, parece que as medidas realmente
# estão agrupadas por espécie. Por exemplo, considerando apenas o comprimento
# da sépala e a largura da sépala, é difícil distinguir entre versicolor e
# virginica. Mas, quando adicionamos o comprimento e a largura da pétala, fica
# mais fácil prever as espécies com base nos vizinhos mais próximos.


