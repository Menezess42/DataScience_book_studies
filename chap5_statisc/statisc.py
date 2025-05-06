from collections import Counter
import matplotlib.pyplot as plt
from typing import List, Tuple, Callable
import math
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from chap4_linear_algebra.linear_algebra import Vectors

num_friends = [100,49,41,40,25,21,21,19,19,18,18,16,15,15,15,15,14,14,13,13,13,13,12,12,11,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,8,8,8,8,8,8,8,8,8,8,8,8,8,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

num_friends = list(map(float, num_friends)) # => [1,2,3]
daily_minutes = [1,68.77,51.25,52.08,38.36,44.54,57.13,51.4,41.42,31.22,34.76,54.01,38.79,47.59,49.1,27.66,41.03,36.73,48.65,28.12,46.62,35.57,32.98,35,26.07,23.77,39.73,40.57,31.65,31.21,36.32,20.45,21.93,26.02,27.34,23.49,46.94,30.5,33.8,24.23,21.4,27.94,32.24,40.57,25.07,19.42,22.39,18.42,46.96,23.72,26.41,26.97,36.76,40.32,35.02,29.47,30.2,31,38.11,38.18,36.31,21.03,30.86,36.07,28.66,29.08,37.28,15.28,24.17,22.31,30.17,25.53,19.85,35.37,44.6,17.23,13.47,26.33,35.02,32.09,24.81,19.33,28.77,24.26,31.98,25.73,24.86,16.28,34.51,15.23,39.72,40.8,26.06,35.76,34.76,16.13,44.04,18.03,19.65,32.62,35.59,39.43,14.18,35.24,40.13,41.82,35.45,36.07,43.67,24.61,20.9,21.9,18.79,27.61,27.21,26.61,29.77,20.59,27.53,13.82,33.2,25,33.1,36.65,18.63,14.87,22.2,36.81,25.53,24.62,26.25,18.21,28.08,19.42,29.79,32.8,35.99,28.32,27.79,35.88,29.06,36.28,14.1,36.63,37.49,26.9,18.58,38.48,24.48,18.95,33.55,14.24,29.04,32.51,25.63,22.22,19,32.73,15.16,13.9,27.2,32.01,29.27,33,13.74,20.42,27.32,18.23,35.35,28.48,9.08,24.62,20.12,35.26,19.92,31.02,16.49,12.16,30.7,31.22,34.65,13.13,27.51,33.2,31.57,14.1,33.42,17.44,10.12,24.42,9.82,23.39,30.93,15.03,21.67,31.09,33.29,22.61,26.89,23.48,8.38,27.81,32.35,23.84]

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
        ys = [friends_counts[x] for x in xs] # The high indicates the number of friends
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
    # > squared deviation from the mean of x_i, so we divide by n-1 instead of n.

    # Standard Deviation
    def standard_deviation(self, xs: List[float])-> float:
        '''
        The standard-deviation is the square root of the variance
        '''
        return math.sqrt(self.variance(xs))
    # The problem of outliers also strikes here and affects the amplitude.
    # Using the same example of the mean, if the most popular user has 200 friends, 
    # the standard deviation will be 14.89 -- more than 60% higher.


    # A most eficient alternative computes the difference between the 75 and 25 
    # percentile.
    def interquartile_range(self, xs: List[float]) -> float:
        '''
        Returns the difference between the 75 and 25 percentile
        '''
        cs = Central_tendencies()
        return cs.quantile(xs, 0.75) - cs.quantile(xs, 0.25)


class Correlation:
    '''
    Show the correlation between two metrics
    '''
    def __init__(self):
        print('ok')
    # Covariance is a type of variance applied to tuples. If
    # variance measures the deviation of a variable from its mean,
    # Covariance measures the simultaneous variation between the variables
    # in relation to their mean
    def covariance(self, xs: List[float], ys: List[float]) -> float:
        assert len(xs) == len(ys), 'xs and ys must have the same len'
        v = Vectors()
        d = Dispersion()
        return v.dot(d.de_mean(xs), d.de_mean(ys))/(len(xs) - 1)
        # > Remember that the dot product sums the product of corresponding elements.
        # > When both X and y are above or below the mean, a positive value enters
        # > the sum. But if X or y is above while the other is below the mean, a 
        # > negative value enters the sum

    # > So a high positive covariance indicates that X tends to
    # > be high when Y is high. and lower when Y is lower.
    # > A high negative covariance indicates the opposite -- that
    # > X tends to be lower when Y is high and vice-versa.

    # But this can be hard to interpret. For two reasons:
    # 1. Its units are the product of the units of the inputs,
    # which may be difficult to undrestand.
    # 2. If each user had twice as many friends, the covariance would be
    # twice as large. However, in practice, the variables would be just
    # as interrelated as before. In other words, it is difficult to define a
    # 'high' covariance.

    # That's why it is more common to calculate the correlation, which dives
    # the standard-deviation of the two variables
    def correlation(self,xs: List[float], ys: List[float]) -> float:
        '''
        Measures the simultaneous variation of xs and ys
        from their means
        '''
        d = Dispersion()
        stdev_x = d.standard_deviation(xs)
        stdev_y = d.standard_deviation(ys)
        if stdev_x > 0 and stdev_y > 0:
            return self.covariance(xs, ys) / stdev_x/stdev_y
        else:
            return 0 # If there is no variance the correlation will be 0
        # > The correlation has no unit and always stays between 
        # > -1 (perfect anticorrelation) and 1 (perfect Correlation).
        # > The number 0.25 indicates a weak positive correlation

    def outlier_demo(self, xs: List[float], ys: List[float]):
        '''
        The person with 100 friends (thats pends just one minute per day)
        is an huge outlier and the correlation is sensitive to that.
        What happens if we ignore that ?
        '''
        plt.plot(xs, ys, 'ro')
        plt.title('Plot with outler')
        plt.xlabel('# minuts per day')
        plt.ylabel('# num of friends')
        plt.show()
        plt.savefig('./num_frinds_minutes_outlier_plot.png')
        outlier = xs.index(100)
        num_friends_good = [x for i, x in enumerate(xs) if i != outlier]
        daily_minutes_good = [x for i, x in enumerate(ys) if i != outlier]
        plt.plot(num_friends_good, daily_minutes_good, 'ro')
        plt.title('Plot without outler')
        plt.xlabel('# minuts per day')
        plt.ylabel('# num of friends')
        plt.show()
        plt.savefig('./num_frinds_minutes_plot.png')
        # daily_hours_good = [dm/60 for dm in daily_minutes_good]
        assert 0.57 < self.correlation(num_friends_good, daily_minutes_good) < 0.58






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
    assert 9.02 < d.standard_deviation(num_friends) < 9.04
    assert d.interquartile_range(num_friends) == 6

    c = Correlation()
    assert 22.42 < c.covariance(num_friends, daily_minutes) < 22.43
    assert 22.42/60 < c.covariance(num_friends, daily_minutes) < 22.43
    assert 0.24 < c.correlation(num_friends, daily_minutes) < 0.25
    c.outlier_demo(num_friends, daily_minutes)

