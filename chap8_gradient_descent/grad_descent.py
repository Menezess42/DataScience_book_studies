# Gradient Descent
from typing import Callable
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from chap4_linear_algebra.linear_algebra import Vector, Matrix, Vectors, Matrixs
import matplotlib.pyplot as plt


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

if __name__ == '__main__':
    gd = GradientDescent()
    gd.ploting_exemple()

