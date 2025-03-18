# Gradient Descent
from typing import Callable
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from chap4_linear_algebra.linear_algebra import Vector, Matrix, Vectors, Matrixs


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
    def derivation(self, x: float) -> float:
        return 2*x

    # This is eazy to verify. Simply compute the quotient of the
    # differences and check the limit.


