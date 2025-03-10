import enum, random 
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

if __name__=='__main__':
    cp = Conditional_Probability()
    cp.two_Kids_problem()



