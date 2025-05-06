# The first step is to compute some summary statiscs, such as the
# number of data poins, the smalles, the largest, the mean, and
# the standard deviation.

# But this don't necessary gives a good comprehension. A good idea
# is to create a histogram to grup the data in discrit buckets
# and count how many points get in each of then:
from typing import List, Dict
from collections import Counter
import math
import matplotlib.pyplot as plt
import random
from chap6_probability.probability import Normal_distribution


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


def main():
    inverse_normal_cdf = Normal_distribution()
    inverse_normal_cdf = inverse_normal_cdf.inverse_normal_cdf

    random.seed(0)

    # Uniform between -100 and 100
    uniform = [200*random.random()-100 for _ in range(10000)]

    # normal distribution with mean 0 and standard-deviation 57
    normal = [57*inverse_normal_cdf(random.random()) for _ in range(10000)]

    plot_histogram(uniform, 10, "Uniform Histogram")
    plot_histogram(normal, 10, "normal Histogram")
    # In this case both have very different maximum and minimum points
    # but define this is not sufficient to explain the different

if __name__ == '__main__':
    main()
