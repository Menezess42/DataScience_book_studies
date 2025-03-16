from typing import List

def reverse(s: List[float]) -> List[float]:
    '''reverse a given list'''
    s = s[::-1]
    return s

if __name__ == '__main__':
    s = reverse([-3, -2, -1, 0, 1, 2, 3])
    print(s)

