from typing import Tuple, List
import math
import sys
import os
import random
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
    def verify_upperTailed_test_power(self, probability, mu_0, sigma_0):
        '''
        Now, imagine that the null hypothesis states that
        the coin is not biased towards heads, i.e., that p<=0.5
        In this case, we want a one-sided test to reject the null
        hypothesis when X is much greater than 50, but not when X is less.
        Therefore, the 5% significance test should apply normal_probability_below
        to find the threshold that lies above the 95% probability
        '''
        hi = self.normal_upper_bound(probability, mu_0, sigma_0) # probability=.95
        print(f'hi: {hi}')
        mu_1, sigma_1 = self.normal_approximation_to_binomial(1000,0.55)
        # é 526 (<531, since we need more probability at the top end)
        type_2_probability = self.normal_probability_below(hi, mu_1, sigma_1)
        power = 1 - type_2_probability # 0.936
        print(f'type_2_probability: {type_2_probability}\nPower: {power}')
        


    # p-values
    # The p-value measures how surprised we should be by a result if H0=True
    # If the p-value is very small, the surprise is large -> Maybe H0!=True
    # p-value high means that H0 is probably True
    # p-value very low means that H0 is probably False
    def two_sided_p_value(self, x: float, mu: float = 0, sigma: float=-1) -> float:
        '''
        What is the probability of observing a value at
        least as extreme as x (in either direction) if
        the values come from a range of N(mu, sigma)
        '''
        if x >= mu:
            # x é maior do que a média, então a coroa é qualquer
            # valor maior que x
            return 2 * self.normal_probability_above(x,mu,sigma)

        # x is less than the mean, between the crown is any value
        # less than x
        return 2*self.normal_probability_below(x, mu, sigma)

    # confidence interval
    # Is a range of values where we believe the
    # true population parameter (in this case, the true
    # probability of getting heads) is located. It is
    # calculated from a sample and has an associated
    # confidence level (e.g. 95%)
    # Therefore, the confidence interval does not
    # prove H0, but it gives us a criterion to check
    # whether or not we have enough evidence to reject
    # it.
    def confidence_interval(self, n, success, confiance=0.95):
        '''
        To find the confidence interval
        we use tree simple steps:
        1. Sampling Proportion (estimated mean)
        2. estimated standard deviation of the sampling distribution
        3. Determine the limits of the confidence interval
        '''
        # 1.
        p_hat = success/n
        mu = p_hat

        # 2.
        sigma = math.sqrt(p_hat * (1-p_hat)/n)

        # 3.
        lower, upper = self.normal_two_sided_bounds(confiance, mu, sigma)
        return lower, upper

    # P-HACKING
    # P-hacking, it's running a statistical test so many
    # times that at some point it becomes significant
    # (a p-value that falls below 0.05)
    def run_experiment(self) -> List[bool]:
        '''
        Flip a fair coin multiple times, True = Heads
        False = tails
        '''
        return [random.random() < 0.5 for _ in range(1000)]
    def reject_fairness(self, experiment: List[bool]) -> bool:
        '''
        P-hacking demonstration.
        Using 5% significance levels
        '''
        num_heads = len([flip for flip in experiment if flip])
        return num_heads < 469 or num_heads > 531

    # A/B Testing
    # Is a statisc way to compare two or more versions
    # and not only see with version performs better, but
    # to see if the the difference between A and B is
    # statiscally differente
    def estimated_parameters(self, N: int, n: int) -> Tupe[float, float]:
        p = n/N
        sigma = math.sqrt(p*(1-p)/N)
        return p, sigma

    def a_b_test_statistic(self, N_A: int, n_A: int, N_B: int, n_B: int) -> float:
        p_A, sigma_A = self.estimated_parameters(N_A, n_A)
        p_B, sigma_B = self.estimated_parameters(N_B, n_B)
        return (p_B - p_A)/math.sqrt(sigma_A**2 + sigma_B**2)
    # This value will be aproximate a standard normal

    # Bayesian Infererence
    def B(self, alpha: float, beta: float) -> float:
        '''
        A normalizing constant for which the total probability
        is 1
        '''
        return math.gamma(alpha) * math.gamma(beta) / math.gama(alpha+beta)

    def beta_pdf(self, x: float, alpha: float, beta: float) -> float:
        if x <= 0 or x >= 1:
            return 0
        return x ** (alpha-1) * (1-x)**(beta-1)/self.B(alpha, beta)


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
    e.verify_twoTailed_test_power(0.95, 0.55, mu_0, sigma_0)
    e.verify_upperTailed_test_power(0.95, mu_0, sigma_0)

    # We computed the observation of 530 heads as follows
    response = e.two_sided_p_value(529.5, mu_0, sigma_0)
    print(response) # 0.062
    # Why 529.5 instead of 530 ? 
    # This is a continuity correction. Since we're approximating
    # a discrete binomial distribution with a continuous normal
    # distribution, we adjust by 0.5 to better estimate the probability.
    # Instead of P(X = 530), we compute P(529. 5 <= X < 530.5) to improve accuracy.

    # To make the sensitivity of this estimate clear, let's do a simulation:
    extreme_value_count = 0
    for _ in range(1000):
        num_heads = sum(1 if random.random() < 0.5 else 0 # count the n⁰ of heads
                        for _ in range(1000)) # in a thousend tosses,
        if num_heads >= 530 or num_heads <= 470: # and cont the qtde of times that
            extreme_value_count += 1 # the n⁰ is 'extreme'

    # The p-value is 0.062 => ~62 values extrems in 1000
    # assert 59 < extreme_value_count < 65, f"{extreme_value_count}"

    # Since the p-value is greater than the 5% fail to reject the null
    # hypothesis. If we observe 532 heads, then the p-value is:
    print(e.two_sided_p_value(531.5, mu_0, sigma_0)) # 0.0463

    # Since this value is less than the 5% significance level, we reject
    # the null hypothesis here, even though the test is still exactly the
    # same. This is just another way of approaching the statistics.
    # Similarly, we have:
    # upper_p_value = normal_probability_above
    # lower_p_value = normal_probability_below
    # When we observe 525 heads, we compute the one-sided
    # test as follows:
    # upper_p_value(524.5, mu_0, sigma_0) # 0.061
    # here, we fail to reject the null hypothesis.
    # For 527 heads, the computation is:
    # upper_p_value(526.5, mu_0, sigma_0) # 0.047
    # here, we reject the null hypothesis.
    
    # Confidence Interval
    lower, upper = e.confidence_interval(1000, 525)
    print(f"Confidence Interval: {lower} <-> {upper}")

    lower, upper = e.confidence_interval(1000, 540)
    print(f"Confidence Interval: {lower} <-> {upper}")


    # P-hacking, it's running a statistical test so many
    # times that at some point it becomes significant
    # (a p-value that falls below 0.05)
    random.seed(0)
    experiments = [e.run_experiment() for _ in range(1000)]
    num_rejections = len([experiment for experiment in experiments if e.reject_fairness(experiment=experiment)])
    print(num_rejections)
    # A/B Testing - Exemple
    # H0 - A and B are equal
    # if A recives 200 cliks in 1000 visualization
    # and B recives 180 in 1000 visualization, the statisc is:
    z = e.a_b_test_statistic(1000, 200, 1000, 180)
    print(f"z: {z}") # -1.14
    # The probability of observe this greater difference it will
    # be:
    r = e.two_sided_p_value(z)
    print(f"r: {r}") # 0.254
    # This value will be so big that we can't define if has difference
    # But if B recives 150 in a 1000 we have:
    z = e.a_b_test_statistic(1000, 200,1000, 150)
    print(f"z: {z}") # -2.94
    r = e.two_sided_p_value(z) # 0.003
    # This indicatsee that there is only a 0.003 chance of observing
    # this large difference if the ads are equally effective
    # A/B Testing Exemple - Conclusion
    # The z-value and p-value indicate whether the difference between A and B
    # is statiscally significant or not. In the first case (180 clicks), we
    # were unable to prove that A is better. But in the second case(150 clicks)
    # the statistics indicate that A performs significantly better than B.
    
