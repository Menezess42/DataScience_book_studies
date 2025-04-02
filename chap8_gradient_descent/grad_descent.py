# Gradient Descent
from typing import Callable
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from chap4_linear_algebra.linear_algebra import Vector, Matrix, Vectors, Matrixs
import matplotlib.pyplot as plt
import random
from typing import TypeVar, Iterator, List


class GradientDescent:
    # The central Idea of Gradient Descent
    '''
    Gradient:
        the vector of partial derivatives
    '''
    def sum_of_squares(self, v: Vector) -> float:
        '''
        Computes the sum of square elements in v
        '''
        vec = Vectors()
        return vec.dot(v, v)
    # Ofte, we will have to maxmize or minimize these functions, that is,
    # determine the input v that produces the largest (or smallest) possible
    # value. In functions like this, the gradient points the direction
    # of the input in which the function grows most rapidly.
    
    # Similarly, to maximize a function, you can select a RANDOM starting point,
    # compute the gradient, take a small step in the direction of that point (in
    # the direction the function grows the most), and repeat the procedure with
    # the new point. You can also minimize a function by taking small steps in
    # the opposite direction.

    # Estimating the Gradient
    # if F is a function with one variable, it derivation in point x 
    # is indicated by f(x) changes when we alter x just a little bit.
    # The derivative is defined as the limit of the quotient of the differences

    def difference_quotient(self, f: Callable[[float], float],
                            x: float,
                            h: float) -> float:
        return (f(x+h) - f(x))/h

    # This occurs as h approaches zero.

    # The derivative is the slope of the tangent line at (x,f(x)),
    # and the quotient of the differences is the slope of the secant
    # line through (x+h, f(x+h)). As h decreases, the secant line
    # approaches the tangent line.

    # In many functions, it is eazy to calculate the derivations
    # with accuracy. Exemple, in the square function:
    def sqaure(self, x: float) -> float:
        return x*x

    # The derivation is:
    def derivative(self, x: float) -> float:
        return 2*x

    # This is eazy to verify. Simply compute the quotient of the
    # differences and check the limit.
    
    # If you can't determine the gradient ?
    # Although it is not possible to set limits in python,
    # we can estimate derivatives by analyzing the quotient of the
    # differences for a small value e.

    def ploting_exemple(self):
        xs = range(-10,11)
        actuals = [self.derivative(x) for x in xs]
        estimates = [self.difference_quotient(self.sqaure, x, h=0.001) for x in xs]

        # plot to indicate that they are esssentialy the same
        plt.title('Actual Derivatives vs. Estimates')
        plt.plot(xs, actuals, 'rx', label='Actual') # red x
        plt.plot(xs, estimates, 'b+', label='Estimate') # blue +
        plt.legend(loc=9)
        plt.savefig('Actual_derivatives_vs_Estimates.png')
        plt.show()

    # If F is a function with multiple variables. 
    # Then it has multiple parcial derivatives.
    # Each derivative indicates how F changes when we
    # make little alterations in one of the input variables.
    # To calculate the parcial derivative i, we to treate as
    # a function of the variable i and considered all the other
    # variables as fixed

    def partial_difference_quotient(self,
                                    f: Callable[[Vector], float],
                                    v: Vector,
                                    i: int,
                                    h: float
                                    ) -> float:
        '''
        Returns the parcial quotient of the differences i of f in v
        '''
        w = [v_j + (h if j==i else 0) # add h just to the i ement of v
             for j, v_j in enumerate(v)]
        return (f(w) - f(v))/h

    # After the function above, we estimate the gradient like this
    def estimate_gradient(self, f: Callable[[Vector], float],
                          v: Vector,
                          h: float = 0.0001):
        return [self.partial_difference_quotient(f, v, i, h)
                for i in range(len(v))]

        # Note: The biggest disadvantage of this
        # 'estimate with the difference quotient'
        # approach is its high computational cost.
        # If v has length n, estimate_gradient must
        # evaluate f on 2n inputs. In this scheme,
        # estimating a series of gradients is a lot of
        # work.
        # Therefore, we will always perform mathematical
        # operations to calculate the gradient functions

    # Using The Gradient
    # We will use gradients to find the minimum between
    # threedimensional vectors.
    def gradient_step(self, v: Vector, gradient: Vector, step_size: float) -> Vector:
        '''
        Move 'step_size' in the direction of gradient from v
        '''
        assert len(v) == len(gradient), 'len of v has to be the same as len of gradient'
        vecs = Vectors()
        step = vecs.scalar_multiply(step_size, gradient)
        return vecs.add(v, step)

    def sum_of_sqaures_gradient(self, v: Vector) -> Vector:
        return [2 * v_i for v_i in v]


    # Using Descent Gradient to ajust models

    # We'll use gradient descent to find the slope and intercept that minimize the
    # mean sqared error. We start with a function that determines the gradient based
    # on the erro of just one point:
    # JUST ONE POINT
    def linear_gradient(self, x: float, y: float, theta: Vector) -> Vector:
        slope, intercept = theta
        predicted = slope*x+intercept # The model predction.
        error = (predicted - y) # the error is (predicted - real)
        squared_error = error**2 # Let's minimize the square error
        grad = [2*error*x, 2*error] # using it gradient.
        return grad
    # Let's analyze:
    # Imagine that for X, the prediction is to high.
    # In this case, the error is positive.
    # The second variable is term of the gradient, 2*error,
    # is positive, indicating that little alterations in the
    # intercepto will increase the prediction (that is already big),
    # that is, increasing alot the sqared error for THIS X
    # The first term, 2*error*xx, has the same signal that x.
    # So if X is positive, little increases in inclination
    # will icrease the prediction and the error. But if X,
    # is negative, little increases in inclination will
    # decrease the prediction and the error.


    # Minibatch and estocastic Gradient Descent
    # minibatch = Amostra
    # Extracted from the dataset
    T = TypeVar('T') # this allows the insertion of generic functions
    
    def minibatchs(self, dataset: List[T], 
                   batch_size: int,
                   shuffle: bool=True) -> Iterator[List[T]]:
        '''
        Creates minibatchs with batch_size from the dataset
        '''
        # iniciate the indices 0, batch_size, 2*batch_size, ....
        batch_starts = [start for start in range(0, len(dataset), batch_size)]
        if shuffle: random.shuffle(batch_starts) # randomic classify the batches
        for start in batch_starts:
            end = start+batch_size
            yield dataset[start:end]

if __name__ == '__main__':
    gd = GradientDescent()
    # gd.ploting_exemple()

    # Select a random start point
    v = [random.uniform(-10, 10) for i in range(3)]
    for epoch in range(1000):
        grad = gd.sum_of_sqaures_gradient(v) # computes the gradient in v
        v = gd.gradient_step(v, grad, -0.01) # take a negative step ffor the gradient
        print(epoch, v)

    vecs = Vectors()
    assert vecs.distance(v, [0,0,0]) < 0.001 # should be close to zero
    # print(vecs.distance(v, [0,0,0]))

    # Using Descent Gradient to ajust models

    # X goes from -50 through 49, y is always 20*x+5
    inputs = [(x,20*x+5) for x in range(-50,50)]

    # After many epochs (each pass through the dataset), we determine some things
    # like the correct parameters.
    theta = [random.uniform(-1, 1), random.uniform(-1,1)]
    learning_rate = 0.001
    for epoch in range(5000):
        # computes gradients mean
        v = Vectors()
        grad = v.vector_mean([gd.linear_gradient(x, y, theta) for x, y in inputs])
        # Gives one step in that direction
        theta = gd.gradient_step(theta, grad, -learning_rate)
        print(epoch, theta)
    slope, intercept = theta
    print(f"slope: {slope}")
    print(f"intercept: {intercept}")
    assert 19.9 < slope < 20.1, 'slope should be about 20'
    assert 4.9 < intercept < 5.1, 'slope should be about 20'

    # Minibatch and estocastic Gradient Descent
    # minibatch = Amostra
    # Extracted from the dataset

    # Now we can solve the quest again, but this time using minibatchs

    theta = [random.uniform(-1, 1), random.uniform(-1,1)]
    for epoch in range(1000):
        for batch in gd.minibatchs(inputs, batch_size=20):
            v = Vectors()
            grad = v.vector_mean([gd.linear_gradient(x, y, theta) for x, y in batch])
            theta = gd.gradient_step(theta, grad, -learning_rate)
        # print(epoch, theta)

    slope, intercept = theta
    print(f"slope: {slope}")
    print(f"intercept: {intercept}")
    assert 19.9 < slope < 20.1, 'slope should be about 20'
    assert 4.9 < intercept < 5.1, 'slope should be about 20'

    # Stocastic Gradient
    theta = [random.uniform(-1, 1), random.uniform(-1,1)]
    for epoch in range(1000):
        for x, y in inputs:
            grad = gd.linear_gradient(x, y, theta)
            theta = gd.gradient_step(theta, grad, -learning_rate)
        print(epoch, theta)

    slope, intercept = theta
    print(f"slope: {slope}")
    print(f"intercept: {intercept}")
    assert 19.9 < slope < 20.1, 'slope should be about 20'
    assert 4.9 < intercept < 5.1, 'slope should be about 20'












