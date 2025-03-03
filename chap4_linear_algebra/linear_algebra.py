# Linear algebra is fundamental to a large number of data science concepts and techniques
from typing import List, Tuple, Callable
import math

Vector = List[float]
Matrix = List[List[float]]


class Vectors:
    '''
    For us, vectors are points in a space of finite dimensions.
    A good way to represent numerical data.
    '''
    height_weight_age = [70,170,40]
    grades = [95, 80, 75, 62]

    def add(self, v: Vector, w: Vector) -> Vector:
        '''Adds the correspondent elements.
           Can't add vectors of diferent dimentions
        '''
        assert len(v) == len(w), "Vectors must be the same length"
        return [v_i + w_i for v_i, w_i in zip(v,w)]


    def subtract(self, v: Vector, w: Vector) -> Vector:
        """Subtract the correspondent element.
           Can't subtract vectors of diferent dimentions
        """
        assert len(v) == len(w), "Vectors must be the same length"
        return [v_i - w_i for v_i, w_i in zip(v,w)]

    def vector_sum(self, vectors: List[Vector]) -> Vector:
        '''
        Adds all the correspondent elements
        '''
        assert vectors, "no vectors provided!"

        # Verify if all the vectors are the same size(dimentions)
        num_elements = len(vectors[0])
        assert all(len(v) == num_elements for v in vectors), "Different sizes!"

        return [sum(vector[i] for vector in vectors)
                for i in range(num_elements)]

    def scalar_multiply(self, c: float, v: Vector) -> Vector:
        '''
        Multiplies every v element for c
        '''
        return [c*v_i for v_i in v]

    def vector_mean(self, vectors: List[Vector]) -> Vector:
        '''
        Computates the mean of elements
        '''
        n = len(vectors)
        return self.scalar_multiply(1/n, self.vector_sum(vectors)) 


    # Another tool that is less knowing is the scalar product (or dot product).
    # The dot product of two vectors is the sum of the products per component
    def dot(self, v: Vector, w: Vector) -> float:
        '''
        Computes v_1*w_1+...+v_n*w_n.
        Vectors have to be the same size.
        '''
        assert len(v) == len(w), "Vectors must be same len(dimentions)"

        return sum(v_i*w_i for v_i, w_i in zip(v,w))


    
    # When W has magnitude=1, this is just it length, the dot product mesure the
    # extension of vector v in w direction (if we project a light behaind v, tthe shadow 
    # projected onto w will make w the same size as v, like w_length+shadow=v)

    # In this way is easy to computate the sum of sqaures of a vector
    def sum_of_sqaures(self, v: Vector) -> float:
        '''
        Returns v_1*v_1+....+v_n*v_n
        '''
        return self.dot(v,v)

    # We can use this value to computate the magnitude (length)
    def magnitude(self,v: Vector) -> float:
        '''
        return the magnitude of v
        '''
        return math.sqrt(self.sum_of_sqaures(v))
    
    
    # Now we have every thing we need to compute the distance between two vectors
    # distance_betwen_2vectors = root((v1-w1)² - ... - (vn-wn)²)

    def squared_distance(self, v: Vector, w: Vector) -> float:
        '''
        Computates (v_1-w_1)**2 +...+ (v_n-w_n)**2
        '''
        return self.sum_of_sqaures(self.subtract(v,w))

    def distance(self, v: Vector, w: Vector) -> float:
        '''
        Computates the distance between v and w
        '''
        return math.sqrt(self.squared_distance(v,w))

    # Maybe is more clear in this way 
    def distance2(self, v: Vector, w: Vector) -> float:
        return self.magnitude(self.subtract(v,w))

class Matrixs:
    '''
    It is a bidimentional colection of numbers. [Line][Column].
    '''

    def shape(self, A: Matrix) -> Tuple[int, int]:
        '''
        Returns (the number of lines of A, number of columns of B)
        '''
        num_rows = len(A)
        num_cols = len(A[0]) if A else 0 # number of elements of the first line
        return num_rows, num_cols

    def get_row(self, A: Matrix, i: int) -> Vector:
        '''
        returns the i line of A (as a vecotr)
        '''
        return A[i]

    def get_column(self, A: Matrix, j: int) -> Vector:
        '''
        Returns the i column of A (as a vector) 
        '''
        return [A_i[j] 
                for A_i in A]

    # We also will create matrix of a given size
    def make_matrix(self, num_rows: int, num_cols: int, entry_fn: Callable[[int, int], float]) -> Matrix:
        '''
        Returns a matrix num_rows X num_cols that the entry is (i,j)
        '''
        return [[entry_fn(i,j)                  # with i, make a list
                 for j in range(num_cols)]      # [entry_fn(i,0), .....]
                for i in range(num_rows)]       # make a list for each i

    
    # With this matrix you can create the identity matrix
    def identity_matrix(self, n: int) -> Matrix:
        '''
        Returns a matrix of identity nxn
        '''
        return self.make_matrix(n,n, lambda i, j: 1 if i == j else 0)

    # Matrix can be see as 'machines' that transforms a vector of a space in a vector of
    # another space
if __name__ == "__main__":
    # ------- VECOTRS --------
    vector = Vectors()
    assert vector.add([1, 2, 3],  [4, 5, 6]) == [5, 7, 9]
    assert vector.subtract([5, 7, 9],  [4, 5, 6]) == [1, 2, 3]
    assert vector.vector_sum([[1, 2],  [3, 4],  [5, 6],  [7, 8]]) == [16, 20]
    assert vector.scalar_multiply(2,  [1, 2, 3]) == [2, 4, 6]
    assert vector.vector_mean([[1, 2], [3, 4],  [5, 6]]) == [3, 4]
    assert vector.dot([1, 2, 3], [4, 5, 6]) == 32
    assert vector.sum_of_sqaures([1, 2, 3]) == 14 
    assert vector.magnitude([3, 4]) == 5
    #-----------------------------

    # -------- MATRIXS --------- 
    matrix = Matrixs()
    assert matrix.shape([[1,2,3],[4,5,6]])==(2,3)
    # assert matrix.identity_matrix(5)
    print(matrix.identity_matrix(5))
