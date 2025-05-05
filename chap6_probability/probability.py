import enum, random 
import math
import matplotlib.pyplot as plt
from collections import Counter
# In this book, think of probability as a way to qauntify uncertainty
# associated with selected events from a universe of events.

class Kid(enum.Enum):
    boy = 0
    girl = 1

class Conditional_Probability:
    '''
    p(e,f) = p(e)p(f)
    p(e|f) = p(e,f)/p(f)
    p(e,f) = p(e|f)p(f)
    p(e|f) = p(e)
    '''
    # The two children family problem
    def random_Kid(self) -> Kid:
        return random.choice([Kid.boy, Kid.girl])

    def two_Kids_problem(self):
        both_girls = 0
        older_girl = 0
        either_girl = 0

        random.seed(0)
        for _ in range(10000):
            younger = self.random_Kid()

            older = self.random_Kid()

            if older == Kid.girl:
                older_girl += 1

            if older == Kid.girl and younger == Kid.girl:
                both_girls += 1

            if older == Kid.girl or younger == Kid.girl:
                either_girl += 1

        print(f"P(both | older): {both_girls/older_girl}")
        print(f"P(both | either): {both_girls/either_girl}")

class Continuous_distributions:
    '''
    pdf
    cdf
    '''
    def uniform_pdf(self,x: float)-> float:
        return 1 if 0 <=x<1 else 0

    def uniform_cdf(self, x: float) -> float:
        '''
        Returns the probability of a given uniform random variable be <=x
        '''
        if x<0: return 0
        elif x<1: return x
        else: return 1

class Normal_distribution:
    '''
    Curve in bell shape.
    Is determined by its mean (mi) and its standard deviation(sigma).
    '''
    def __init__(self):
        self.SQRT_TWO_PI = math.sqrt(2*math.pi)

    def normal_pdf(self, x: float, mu: float=0, sigma: float = 1)-> float:
        return (math.exp(-(x-mu)**2/2/sigma**2)/(self.SQRT_TWO_PI * sigma))

    def norm_dist_plot(self):
        xs = [x / 10.0 for x in range(-50, 50)]
        plt.plot(xs, [self.normal_pdf(x, sigma=1) for x in xs], '-', label='mu=0, sigma=1')
        plt.plot(xs,[self.normal_pdf(x, sigma=2) for x in xs], '--', label='mu=0, sigma=2')
        plt.plot(xs,[self.normal_pdf(x, sigma=0.5) for x in xs], ':', label='mu=0, sigma=0.5')
        plt.plot(xs,[self.normal_pdf(x, mu=-1) for x in xs], '-.', label='mu=-1, sigma=1')
        plt.legend()
        plt.title('Various Normal pdfs')
        plt.savefig('./various_normal_pdfs.png')
        plt.show()
        # > The standard normal distribution occurs when mi=0 and sigma=1.
        # > If Z it is a standard random normal variable then:
        # > X = mi(Z) + sigma
        # > In another way if X it is a random normal variable with mean mi and
        # > standard deviation sigma, then:
        # > Z = (X-mi)/sigma
        # > This is a standard normal variable.

    def normal_cdf(self, x: float, mu: float=0, sigma: float = 1) -> float:
        '''
        The CDF for a normal distribution can't be coded in a 'simple'
        way, but we can write it using the error function math.erf from
        Python
        '''
        return (1+math.erf((x-mu)/math.sqrt(2)/sigma)) / 2

    def normal_cdf_plot(self):
        xs = [x/10.0 for x in range(-50,50)]
        plt.plot(xs, [self.normal_cdf(x, sigma=1) for x in xs], '-', label='mu=0, sigma=1')
        plt.plot(xs,[self.normal_cdf(x, sigma=2) for x in xs], '--', label='mu=0, sigma=2')
        plt.plot(xs,[self.normal_cdf(x, sigma=0.5) for x in xs], ':', label='mu=0, sigma=0.5')
        plt.plot(xs,[self.normal_cdf(x, mu=-1) for x in xs], '-.', label='mu=-1, sigma=1')
        plt.legend(loc=4) # in the right conor 
        plt.title('Various Normal cdfs')
        plt.savefig('./various_normal_cdfs.png')
        plt.show()

    def inverse_normal_cdf(self,
                           p: float,
                           mu: float=0,
                           sigma: float=1,
                           tolerance: float = 0.00001) -> float:
        '''
        Sometimes we invert the normal CDF to obtain the value
        corresponding to a specific probability. There is no simple
        way to compute this inversion, but since the normal CDF
        is continuously increasing, we can use binary search
        '''
        # If not the standard, compute the standard and resize
        if mu != 0 or sigma !=1:
            return mu + sigma * self.inverse_normal_cdf(p, mu=0, sigma=1, tolerance=tolerance)
        low_z = -10.0 # normal_cdf(-10) it is (very close to) 0
        hi_z = 10.0 # normal_cdf(10) it is (very close to) 1
        while hi_z - low_z > tolerance:
            mid_z = (low_z + hi_z) / 2 # consider the midpoint
            mid_p = self.normal_cdf(mid_z) # and the valu of CDF
            if mid_p < p:
                low_z = mid_z # the midpoint is to low, find one higher
            else:
                hi_z=mid_z # the midpoint is to high, find one lower
        return mid_z
        # > This function divides the two intervals in two several times
        # > until it reaches a Z sufficiently close to the desired probability

class Center_limit:
    def bernouli_trial(self, p: float) -> float:
        '''
        Returns 1 with probability p and 0 with probability 1-p
        '''
        return 1 if random.random() < p else 0
    
    def binomial(self, n: int, p: float) -> int:
        '''
        Returns the sum of n bernouli_trials(p)
        '''
        return sum(self.bernouli_trial(p) for _ in range(n))

    # > The mean of a bernoulli(p) variable is p and its standard deviaiton
    # > is root(p(1-p)). According to the central limit theorem, as n increases,
    # > the binomial(n,p) variable becomes approximately a normal random variable
    # > with mean mi=np and standard deviaiton sigma=root(np(1-p)).

    def binomial_histogram(self, p: float, n: int, num_points: int) -> None:
        '''
        Select points of a binomial(n,p) and plots its histogram
        '''
        data = [self.binomial(n,p) for _ in range(num_points)]

        # Use a bar graph to indicate samples of binomials
        histogram = Counter(data)
        plt.bar([x - 0.4 for x in histogram.keys()],
                [v/num_points for v in histogram.values()],
                0.8, # ????
                color='0.75')

        mu = p*n
        sigma = math.sqrt(n*p*(1-p)) # square root

        # Uses a line graph to inidicate the normal aproximation
        xs = range(min(data), max(data)+1)
        nd = Normal_distribution()
        ys = [nd.normal_cdf(i+0.5, mu, sigma) - nd.normal_cdf(i-0.5,mu,sigma) 
              for i in xs]
        plt.plot(xs, ys)
        plt.title("binomial distribution vs. Normal Aproximation")
        plt.savefig("./binomial_distribution_vs._Normal_Aproximation.png")
        plt.show()

class a:
    def __init__(self):
        ...
    def test(a,b):
        return a+b

if __name__=='__main__':
    cp = Conditional_Probability()
    # cp.two_Kids_problem()
    nd = Normal_distribution()
    #nd.norm_dist_plot()
    # nd.normal_cdf_plot()
    cl = Center_limit()
    cl.binomial_histogram(0.75, 100, 10000)



