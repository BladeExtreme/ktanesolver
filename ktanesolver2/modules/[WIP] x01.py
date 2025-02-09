from ..edgework import edgework

class x01(edgework):
    def __check(self, n):
        if isinstance(n, list): raise TypeError("numbers must be in list")
        elif not all(isinstance(a, int) for a in n): raise TypeError("Element of numbers must be in int")
        elif len(n)!=10: raise IndexError("Length of numbers must be 10")
        elif not all(a>=0 for a in n): raise ValueError("Element of numbers cannot be negative")
        return n
    
    def __init__(self, numbers:list[int]):
        '''
        Initialize a new x01 instance

        Args:
            edgework (edgework): The edgework of the bomb
            numbers (list (int)): The score that appears on the module for each segments. NOTE: The list assumes that the first index is the topmost and its segment color is red
        '''
        self.__numbers = self.__check(numbers)
    
    def __calculate(self):
        pass

    def solve(self):
        self.__calculate()