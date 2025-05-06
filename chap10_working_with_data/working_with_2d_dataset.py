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


def bucketize(point: float, bucket_size: float) -> float:
    """Floor the point to the next lower multiple of bucket_size"""
    return bucket_size * math.floor(point / bucket_size)


def make_histogram(points: List[float], bucket_size: float) -> Dict[float, int]:
    """Buckets the points and counts how many in each bucket"""
    return Counter(bucketize(point, bucket_size) for point in points)


def plot_histogram(points: List[float], bucket_size: float, title: str = ""):
    histogram = make_histogram(points, bucket_size)
    plt.bar(histogram.keys(), histogram.values(), width=bucket_size)
    plt.title(title)
    plt.show()


def random_normal()->float:
    '''
    returns a random point of a standart normal distribution
    '''
    nd = Normal_distribution()
    return nd.inverse_normal_cdf(random.random())


def main():
    c = Correlation()
    correlation = c.correlation
    xs = [random_normal() for _ in range(1000)]
    ys1 = [x+random_normal()/2 for x in xs]
    ys2 = [-x+random_normal()/2 for x in xs]

    plt.figure(figsize=(10, 6))
    plt.hist(ys1, bins=50, alpha=0.6, label='ys1', color='skyblue', density=True)
    plt.hist(ys2, bins=50, alpha=0.6, label='ys2', color='salmon', density=True)
    plt.title('Distribuições de ys1 e ys2')
    plt.xlabel('Valor')
    plt.ylabel('Densidade')
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.scatter(xs, ys1, marker='.', color='black', label='ys1')
    plt.scatter(xs, ys2, marker='.', color='gray', label='ys2')
    plt.xlabel('xs')
    plt.ylabel('ys')
    plt.legend(loc=9)
    plt.title('Very different join distribuition')
    plt.show()

    # This diference is also observed when we analisy the Correlation
    print(correlation(xs=xs, ys=ys1)) # 0.9 
    print(correlation(xs=xs, ys=ys2)) # 0.9 

if __name__ == '__main__':
    main()
