from ..edgework import edgework

class skewedslots(edgework):
    __prime = [2,3,5,7,11,13,17,19,23,29]
    __fibonacci = [1,1,2,3,5,8,13,21,34,55,89,144]
    
    def __check(self, i):
        if not isinstance(i, list): raise TypeError("Initial must be in list")
        elif any([True if not isinstance(a, int) else False for a in i]): raise TypeError("Initial numbers must be in int")
        elif any([True if a<0 or a>10 else False for a in i]): raise ValueError("Numbers must be in range of 0-10")
        return i
    
    def __init__(self, edgework: edgework, initial: list):
        '''
        Initialize a new skewedslots instance

        Args:
            edgework (edgework): The edgework of the bomb
            initial (list [int, int, int]): The numbers that appears on the bomb. Index 0 represents the leftmost column
        '''
        super().__init__(edgework.batt, edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__initial = self.__check(initial)
        self.__edit = self.__initial.copy()
    
    def __calculate(self):
        offset = len(self._litind)-len(self._unlitind)
        edit = [5-offset if x == 2 else 0-offset if x == 7 else x-offset for x in self.__edit]
        for a in range(len(edit)):
            if edit[a]%3==0: edit[a] += 4
            elif edit[a]>7: edit[a] *= 2
            elif edit[a]<3 and edit[a]%2==0: edit[a] /= 2
            elif 'STEREO RCA' not in self._uniqueports or 'PS/2' not in self._uniqueports: edit[a] = self.__initial[a]+self.batt
        return edit
    
    def __calculate1(self, n):
        if n>5 and n%2==0: n /= 2
        elif n in self.__prime: n += int(self._sndigit[-1])
        elif 'PARALLEL' in self._uniqueports: n *= -1
        elif self.__initial[1]%2==1: return n
        else: n -= 2
        return n
    def __calculate2(self, n):
        if 'BOB' in self._unlitind: return n
        elif n==0: n += self.__initial[0]
        elif n in self.__fibonacci: n += self.__fibonacci[self.__fibonacci.index(n)+1]
        elif n >= 7: n+=4
        else: n*=3
        return n
    def __calculate3(self, n):
        if 'SERIAL' in self._uniqueports: n += max([int(a) for a in self._sndigit])
        elif self.__initial.count(self.__initial[2]) > 1: return n
        elif n >= 5: n = bin(n)[2:].count('1')
        else: n+=1
        return n

    def solve(self):
        '''
        Solve the Skewed Slots module

        Returns:
            Tuple (int, int, int): The submit numbers. Index 0 represents leftmost column
        '''
        edit = [int(a) for a in self.__calculate()]
        modified = [int(self.__calculate1(edit[0]))%10, int(self.__calculate2(edit[1]))%10, int(self.__calculate3(edit[2]))%10]
        return tuple(modified)