from ..edgework import edgework

class letterkeys(edgework):
    def __check(self, n):
        if not isinstance(n, int): raise TypeError("number must be int")
        elif n<0 or n>99: raise IndexError("number cannot be negative or above 99")
        return n

    def __init__(self, edgework:edgework, number:int):
        '''
        Initialize a new letterkeys instance

        Args:
            edgework (edgework): The edgework of the bomb
            number (int): The number that appears on the module            
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__number = self.__check(number)
    
    def __calculate(self):
        if self.__number==69: return 'D'
        elif self.__number%6==0: return 'A'
        elif self.batt>=2 and self.__number%3==0: return 'B'
        elif any([a in ['C','E','3'] for a in self.sn]) and self.__number in range(22,80): return 'B'
        elif any([a in ['C','E','3'] for a in self.sn]): return 'C'
        elif self.__number<46: return 'D'
        else: return 'A'

    def solve(self):
        '''
        Solve the Letter Keys module

        Returns:
            str: The correct letter to press
        '''
        return self.__calculate()