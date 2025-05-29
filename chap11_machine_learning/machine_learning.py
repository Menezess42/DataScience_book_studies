# Dividing data

import random
from typing import List, Tuple, TypeVar

X = TypeVar("X")  # Tipo genérico para representar um ponto de dados


def split_data(data: List[X], prob: float) -> Tuple[List[X], List[X]]:
    """
    Divida os dados em frações [prob, 1 - prob]
    """
    data = data[:]  # Faça uma cópia superficial
    random.shuffle(data)  # Porque o shuffle modifica a lista
    cut = int(len(data) * prob)  # Use prob encontrar um limiar
    return data[:cut], data[cut:]  # e dividir a lista aleatória nesse ponto


data = [n for n in range(1000)]
train, test = split_data(data, 0.75)
assert len(train) == 750
assert len(test) == 250

# E os dados originais devem ser preservados (em alguma ordem)
assert sorted(train + test) == data


# Dividing data with Output variables
Y = TypeVar("Y")  # tipo genérico para representar variáveis de saída


def train_test_split(
    xs: List[X], ys: List[Y], test_pct: float
) -> Tuple[List[X], List[X], List[Y], List[Y]]:
    # Gere e divida os indices
    idxs = [i for i in range(len(xs))]
    train_idxs, test_idxs = split_data(idxs, 1 - test_pct)

    return (
        [xs[i] for i in train_idxs],  # x_train
        [xs[i] for i in test_idxs],  # x_test
        [ys[i] for i in train_idxs],  # y_train
        [ys[i] for i in test_idxs],  # y_test
    )


xs = [x for x in range(1000)]  # xs são 1 .... 1000
ys = [2 * x for x in xs]  # cada y_i é o dobro de x_i
x_train, x_test, y_train, y_test = train_test_split(xs, ys, 0.25)
# Verifique se as proporções estão corretas
assert len(x_train) == len(y_train) == 750
assert len(x_test) == len(y_test) == 250

# Verifique se os pontos de dados correspondentes estão emparelhados corretamente
assert all(y == 2 * x for x, y in zip(x_train, y_train))
assert all(y == 2 * x for x, y in zip(x_test, y_test))


# After we do something like this (de function is not part of the code
# it is just so that this "code" is not called)
def something_like_this():
    model = SomeKindOfModel()
    x_train, x_test, y_train, y_test = train_test_split(xs, ys, 0.33)
    model.train(x_train, y_train)
    performance = model.test(x_test, y_test)


# If the model performs well in the test, we may be confident.
# But, that can be wrong in an set of ways.
# 1. There may be common patterns in the test and training data
# that do not generalize to a larger set.
# In this type of cases we can divide the data in 3 parts:
# Train for training the model;
# Validation to validate the model;
# Test to test the model;


# #### CORREÇÃO ########
# It's not safe to use the "precision" as a criteria to measure
# the quait of a model (binary classification).

# Dados de exemplo do livro
# |          | Leucemia  | Sem Leucemia  |   Total  |
# |----------|-----------|---------------|----------|
# |  "Luke"  |    70     |    4,930      |   5,000  |
# |Não "Luke"|  13,930   |   981,070     |  995,000 |
# |  Total   |  14,000   |   986,000     | 1,000,000|

# Vamos usar estes dados para computar várias estatísticas sobre
# o desempenho do modelo.


# A acurácia é definida como a fração de previsões corretas:
def accuracy(tp: int, fp: int, fn: int, tn: int) -> float:
    """
    tp: true postives  | Think that is X and it is X
    fp: false positive | Think is X but is Y
    fn: false negative | Think is Y but is X
    tn: true negative  | Think is Y and it is Y
    """
    correct = tp + tn
    total = tp + fp + fn + tn
    return correct / total


assert accuracy(70, 4930, 13930, 981070) == 0.98114


# Geralmente observamos a combinação de acurácia e sensibilidade.
# A precisão determina em que medida as previsões positivas são acuradas:
def precision(tp: int, fp: int, fn: int, tn: int) -> float:
    """
    tp: true postives  | Think that is X and it is X
    fp: false positive | Think is X but is Y
    fn: false negative | Think is Y but is X
    tn: true negative  | Think is Y and it is Y
    """
    return tp / (tp + fp)


assert precision(70, 4930, 13930, 981070) == 0.014


# Já a sensibilidade determina a fração dos positivos identificados pelo modelo:
def recall(tp: int, fp: int, fn: int, tn: int) -> float:
    """
    tp: true postives  | Think that is X and it is X
    fp: false positive | Think is X but is Y
    fn: false negative | Think is Y but is X
    tn: true negative  | Think is Y and it is Y
    """
    return tp / (tp + fn)


assert recall(70, 4930, 13930, 981070) == 0.005

# We can see that both numbers (precision and recall) are awful


# Precisiona and recall are combined in the F1 score
def f1_score(tp: int, fp: int, fn: int, tn: int) -> float:
    p = precision(tp, fp, fn, tn)
    r = recall(tp, fp, fn, tn)

    return 2 * p * r / (p + r)


# Essa é a média harmônica da precisão e da sensibilidade e, necessariamente,
# fica entre elas.


# #### O Dilema Viés-Variância #####
# OUtra forma de pernsar no problema do overfiting é com o dilema viés e a
# variância.

# Viés alto e Variância baixa geralmente indica subajuste (underfiting)
# Viés baixo e Variância alta geralmente indica sobreajuste (overfiting)

# Pensar nos probllemas do modelo dessa forma facilita a definição de soluções
# quando ele não funciona tão bem.

# Se o modelo tem um viés alto (indicando um desempenho ruim até com os dados
# de treinamento), uma opção é adicionar mais
# Recursos.

# Da mesma forma, se o modelo tem uma variância alta, é possível remover recursos.
# aqui, outra solução seria obter mais dados (se possível).


