from collections import Counter
import matplotlib.pyplot as plt
from typing import List, Tuple, Callable
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from chap4_linear_algebra.linear_algebra import Vectors

num_friends = [100,49,41,40,25,21,21,19,19,18,18,16,15,15,15,15,14,14,13,13,13,13,12,12,11,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,8,8,8,8,8,8,8,8,8,8,8,8,8,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

class Statisc:
    '''
    Statistics englobes all the mathematical
    concepts and techniques that we apply for 
    understand the data.
    '''

    num_friends = [100,49,41,40,25,21,21,19,19,18,18,16,15,15,15,15,14,14,13,13,13,13,12,12,11,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,8,8,8,8,8,8,8,8,8,8,8,8,8,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

    def ploting_num_friends(self):
        '''
        This graph is to complex for a presentation.
        So we gona do some statiscs.
        '''
        friends_counts = Counter(self.num_friends)
        xs = range(101) # the greatest value is 100
        ys = [friends_counts[x] for x in xs] # The hight indicates the number of friends
        plt.bar(xs,ys)
        plt.axis([0,101,0,25]) # [0,101,0,25] is [xmin, xmax, ymin, ymax]
        plt.xlabel("# of friends")
        plt.ylabel("# of people")
        plt.savefig('./ugly_plot.png')
        plt.show()

        # Number of data points
        num_points = len(self.num_friends)

        # Min and Max values
        largest_value = max(self.num_friends)
        smallest_value = min(self.num_friends)

        sorted_values = sorted(self.num_friends)
        smallest_value = sorted_values[0]
        second_smallest_value = sorted_values[1]
        second_largest_value = sorted_values[-2]
        print(f"Num Points: {num_points}\nLargest Value: {largest_value}")
        print(f"Smallets Value: {smallest_value}\nSecond Smallest Value: {second_smallest_value}")
        print(f"Second largest Value: {second_largest_value}")

class Central_tendencies:
    # In general we want to have some notion about the central points of the data.
    # For this we use the mean.
    # But if we have outliers, the mean can show a "wrong" value.
    # When we have a data (e) and it increase a little, the mean increases by
    # (e)/n | n=len(data)
    # That's why mean is comument applied in calculation tricks
    def mean(self, xs: List[float]) -> float:
        return sum(xs) / len(xs)


    # To know the exact value from the central point in the data we use the 
    # meadian. If the data is len odd it select the middle value. If len is even
    # the median takes the mean of the two middle values

    # private functions is indicated in this way _private
    def _median_odd(self, xs: List[float]) -> float:
        '''If len(xs) is odd, the median will be the middle value'''
        return sorted(xs)[len(xs)//2]


    def _median_even(self, xs: List[float]) -> float:
        '''If len(xs) is even, the median will take the mean of the 2 middle values'''
        sorted_xs = sorted(xs)
        hi_midpoint=len(xs)//2
        return (sorted_xs[hi_midpoint -1] + sorted_xs[hi_midpoint])/2

    # Using the example above about (e), if we increase (e) just a little bit,
    # we might increase the median by (e), decrease it by a smaller amount than (e),
    # or by nothing at all, depending on the other parts of the data.
    def median(self, v: list[float]) -> float:
        '''Find the middle value in v'''
        return self._median_even(v) if len(v)%2==0 else self._median_odd(v)

    # A generalization of median is the quantile, a value that separates an
    # determined percent of the data (the median separates 50% of the datas)
    def quantile(self, xs: List[float], p: float) -> float:
        '''
        Returns the value pth-percentile in x
        '''
        p_index = int(p*len(xs))
        return sorted(xs)[p_index]

    # The most frequent values (mode)
    def mode(self, x: List[float]) -> List[float]:
        '''
        Returns a list, because can have 1 or more values
        '''
        counts = Counter(x)
        max_count = max(counts.values())
        return [x_i for x_i, count in counts.items()
                if count == max_count]


class Dispersion:
    '''
    Express the distribution of the data.
    Here, in general, the values closest to zero
    indicates that the data is not scattered,
    and bigger values indicates more scatter.
    '''

    # Exemple, a simple measurement about that is the
    # amplitude, the difference between 
    # the biggest and smallest element
    def data_range(self, xs: List[float]) -> float:
        '''Don't depends on the data as all, just the max and mean values'''
        return max(xs) - min(xs)


    # A more complex measurement is the variance, computated in this way:
    def de_mean(self, xs: List[float])-> List[float]:
        '''
        Translate xs by subtracting their mean
        (so that the result has mean 0)
        '''
        ct = Central_tendencies()
        x_bar = ct.mean(xs=xs)
        return [x - x_bar for x in xs]

    def variance(self, xs: List[float]) -> float:
        '''
        Near root mean square deviation from the mean
        '''
        assert len(xs) >= 2, 'Variance requires at least two elements'
        n = len(xs)
        deviation = self.de_mean(xs)
        v = Vectors()
        x = v.sum_of_sqaures(v=deviation)
        return  x / (n-1)
    # > This is almost the root mean squared deviation from the mean (population variance)
    # > but we are dividing by n-1 (Bessel's correction) insted of n.
    # > In fact, in a largeer population sample, x_bar is just an estimate of the
    # > true mean, i.e. at mean (x_i - x_bar)², there is an underestimate of the
    # > squared deviation from the mean of _xi, so we divide by n-1 instead of n.

if __name__ == '__main__':
    s = Statisc()
    #s.ploting_num_friends()
    # mean_ = s.mean(xs=num_friends)
    # print(f"mean: {mean_}")

    s = Central_tendencies()
    assert s.median([1,10,2,9,5]) == 5
    assert s.median([1,9,2,10]) == (2+9)/2

    # Now we can computate the median for the number of friends
    # print(s.median(num_friends)) # 6
    assert s.quantile(num_friends, 0.1) == 1
    assert s.quantile(num_friends, 0.25) == 3
    assert s.quantile(num_friends, 0.75) == 9
    assert s.quantile(num_friends, 0.90) == 13

    assert set(s.mode(num_friends)) == {1,6}

    d = Dispersion()
    assert d.data_range(num_friends) == 99
    assert d.variance(num_friends) < 81.55



