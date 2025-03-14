from typing import Tuple
import math
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from chap6_probability import probability

class Exemple:
    '''
    Testing the honesty of a coin.
    The probability p of landing heads.
    H0 = The coins is honest, in other words, p = 0.5.
    H1 = The coins is disonest, in other words, p != 0.5.
    the test consists of n coin tosses and the evaluation of X,
    the number of heads. Each coin toss is a Bernoulli trial,
    which means that X is a binomial random variable that, as
    we saw in Chapter 6, we can approximate using a normal
    distribution
    '''

    def normal_approximation_to_binomial(self, n: int, p: float) -> Tuple[float, float]:
        '''
        Returns mu and sigma correspondent binomial(n,p)
        '''
        mu = p*n
        sigma = math.sqrt(p*(1-p)*n)
        return mu, sigma

    # Whenever a random variable follows a normal distribution,
    # it is possiblie to apply normal_cdf to find
    # out the probability of its value being within a given range
    # or not.


    # The normal cdf is the probability that the variable is 
    # below a threshold   nd = Normal_distribution()
    nd = probability.Normal_distribution()
    normal_probability_below = nd.normal_cdf
    
    # It is above the limit if it is not below the limit
    def normal_probability_above(self, lo: float,
                                 mu: float=0,
                                 sigma: float = 1) -> float:
        '''
        The probability of a N(mu, sigma) be greater than lo.
        '''
        return 1-self.normal_probability_below(lo, mu, sigma)

    
    # It is between if is less then hi, but greater than lo
    def normal_probability_between(self,
                                   lo: float,
                                   hi: float,
                                   mu: float=0,
                                   sigma: float = 1) -> float:
        '''
        The probability of n(mu,sigma) be greater than lu
        '''
        return self.normal_probability_below(hi, mu, sigma) - self.normal_probability_below(lo,mu,sigma)

    # It is out if is between
    def normal_probability_outside(self,
                                   lo: float,
                                   hi: float,
                                   mu: float = 0,
                                   sigma: float = 1) -> float:
        '''
        The probability of N(mu, sigma) it is not between lo and hi.
        '''
        return 1 - self.normal_probability_between(lo,hi,mu,sigma) 

    
    # We also use the inverse. We can find the region outside the limit
    # or the symmetric interval around the mean witch a certain probability level.
    # For example, to find the center of the interval at the mean that has 60%
    # probability, we need to determine the lower and upper limits, each having
    # 20%

    def normal_upper_bound(self, probability: float,
                           mu: float=0,
                           sigma: float=1) -> float:
        '''
        Return the z for P(Z <= z) = probability
        '''
        return self.nd.inverse_normal_cdf(probability, mu, sigma)

    def normal_lower_bound(self, probability,mu=0,  sigma=1) -> float:
        ''' Return z for wich P(Z >= z) = probability '''
        return self.nd.inverse_normal_cdf(1 - probability,mu,sigma)

    def normal_two_sided_bounds(self,probability, mu=0, sigma=1):
        """returns the symmetric (about the mean) bounds 
        that contain the specified probability"""
        tail_probability = (1 - probability) / 2

        # upper bound should have tail_probability above it
        upper_bound = self.normal_lower_bound(tail_probability, mu, sigma)

        # lower bound should have tail_probability below it
        lower_bound = self.normal_upper_bound(tail_probability, mu, sigma)

        return lower_bound, upper_bound



    # Calculating test power for two-tailed. That means upper and lower limits
    # Like: | X |
    def verify_twoTailed_test_power(self, prob, percent, mu, sigma):
        '''
        We also want to determine the power of the test, the probability
        of not making a type 2 error, which happens when we fail to reject
        a false H0.
        (Knowing that p is not 0.5 does not provide much information about
        the distribution of X)
        So specific we want to verify what happen if p is 0.55; In this case
        the coin will be slightly biased twoards heads.
        '''
        # Limits of 95% based in p = 0.55(prob)
        lo, hi = self.normal_two_sided_bounds(prob, mu, sigma)

        # Real mu and sigma based in p=0.55(prob)
        mu_1, sigma_1 = self.normal_approximation_to_binomial(1000, percent)

        # A type 2 error occurs when we fail to reject the null hypothesis,
        # which occurs when X is still in the original range.
        type_2_probability = self.normal_probability_between(lo, hi, mu_1, sigma_1)
        power = 1- type_2_probability # 0.887
        print(f"lo: {lo} hi: {hi}\nmu_1: {mu_1} sigma_1: {sigma_1}")
        print(f"type 2 probability: {type_2_probability} power: {power}")


    # Calculating test power for upper-tailed. 
    # That means upper limits
    # Like: X |
    def verify_upperTailed_test_power(self, kargs):
        pass






if __name__ == '__main__':
    e = Exemple()
    mu_0, sigma_0 = e.normal_approximation_to_binomial(1000, 0.5)
    sigma_0 = math.trunc(sigma_0*10)/10
    print(f"mu0: {mu_0}\nsigma0: {sigma_0}")

    # We need to define significance -- determine how willing we
    # are to make a type 1 error ('false positive') and reject H0
    # even if it is true.
    # This is usually set at 5% or 1%. The 5% is the risk we are willing
    # to take of rejecting H0 and accepting H1 erroneously, i.e we accept
    # a 5% margin of error that an H0 will be interpreted as false.
    # (469, 531)
    lower_bound, upper_bound = e.normal_two_sided_bounds(0.95, mu_0, sigma_0)
    print(f"lower_bound: {lower_bound}\nupper_bound:  {upper_bound}")
    # The 0.95 indicates that we have only a probability of 5% that X is
    # outside this interval
    e.verify_test_power(0.95, 0.55, mu_0, sigma_0)

