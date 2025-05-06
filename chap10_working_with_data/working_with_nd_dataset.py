from typing import List, Dict
from collections import Counter
import math
import matplotlib.pyplot as plt
import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from chap6_probability.probability import Normal_distribution
from chap5_statisc.statisc import Correlation
from chap4_linear_algebra.linear_algebra import Matrix, Vector, Matrixs, Vectors

correlation = Correlation()
matrixs = Matrixs()
vectors = Vectors()

# Working with N dimensions you have to determine the relation between then.
# A simple approach it sto analyse the correlation matrix. 
# in which the entry in line i and column j is the correlation between the
# dimension i and j of the data

def random_normal()->float:
    '''
    returns a random point of a standart normal distribution
    '''
    nd = Normal_distribution()
    return nd.inverse_normal_cdf(random.random())

def random_row() -> List[float]:
   row = [0.0, 0, 0, 0]
   row[0] = random_normal()
   row[1] = -5 * row[0] + random_normal()
   row[2] = row[0] + row[1] + 5 * random_normal()
   row[3] = 6 if row[2] > -2 else 0
   return row

random.seed(0)
num_points = 100
# each row has 4 points, but really we want the columns
corr_rows = [random_row() for _ in range(num_points)]

corr_data = [list(col) for col in zip(*corr_rows)]

def correlation_matrix(data: List[Vector]) -> Matrix:
    '''
    returns the matrix len(data) x len(data), in which the entry
    (i,j) is the correlation between data[i] and data[j]
    '''
    def correlation_ij(i: int, j: int) -> float:
        return correlation.correlation(data[i], data[j])
    return matrixs.make_matrix(len(data), len(data), correlation_ij)


# A more visual approach (when there are not many dimensions) is to create
# a scatterplot matrix to indicate all the pairs of points in the scatterplot.
# Here we are using plt.subplot to create subplots from the reference plot.
# When we indicate the number of rows and columns, it returns an object figure
# (we will not use it) and a two-dimensional array of objects axes (which we
# will use to create the plot)
def main():
    num_vectors = len(corr_data)
    fig, ax = plt.subplots(num_vectors, num_vectors)

    for i in range(num_vectors):
        for j in range(num_vectors):
            if i != j:
                ax[i][j].scatter(corr_data[j], corr_data[i])
            else:
                ax[i][j].annotate("series" + str(i), (0.5, 0.5),
                                  xycoords='axes fraction',
                                  ha='center', va='center')

            # Correção da visibilidade dos eixos:
            if i != num_vectors - 1:
                ax[i][j].xaxis.set_visible(False)  # Oculta eixo X, exceto última linha
            if j != 0:
                ax[i][j].yaxis.set_visible(False)  # Oculta eixo Y, exceto primeira coluna

    # Ajuste de limites nas diagonais (opcional)
    ax[-1][-1].set_xlim(ax[0][-1].get_xlim())
    ax[0][0].set_ylim(ax[0][1].get_ylim())
    plt.savefig('./scatterplot_matrix.png')
    plt.show()

    # When analyzing the scatter plot, note that series 1 is very negatively correlated
    # with series 0, series 2 is positively correlated with series 1 and series 3 only
    # accepts the values 0 and 6, with 0 corresponding to the small values of series 2;
    # and 6, to the large values.
    
    ## REMEMBERING ##
    # positively Corelated:
    # - When one gos up, the other also tends to go up.

    # negatively Corelated:
    # - When one gos up, the other tends to go down.

if __name__ == '__main__':
    main()
