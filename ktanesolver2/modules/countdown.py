import copy
from ..edgework import edgework

class countdown(edgework):
    def __check(self, t, o):
        if not isinstance(t, int): raise TypeError("target must be int")
        elif not isinstance(o, list): raise TypeError("options must be in list")
        elif not all([isinstance(a, int) for a in o]): raise TypeError("Element of options must be int")
        elif len(o)!=6: raise IndexError("Length of options must be 6")
        return t,o
    
    def __init__(self, edgework:edgework, target:int, options:list[int]):
        '''
        Initialize a new countdown instance

        Args:
            edgework (edgework): The edgework of the bomb
            target (int): The target number to achieve
            options (list [int]): List of all numbers to be used in an operation'
        '''
        super().__init__(edgework.batt, edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__target, self.__options = self.__check(target, options)
    
    def __calculate(self):
        queue = [[a, [], [z for z in self.__options if z!=a], abs(self.__target-a)] for a in self.__options]
        queue.sort(key=lambda x: x[-1])

        while queue:
            n, path, options, score = queue.pop(0)
            if n==self.__target: return path
            if len(options)==1: continue
            for a in options:
                if a==n: continue
                operation = [lambda x,y: x+y, lambda x,y: x-y, lambda x,y: x*y, lambda x,y: x//y]
                for b in range(4):
                    if (a==0 or (n%a!=0)) and b==3: continue
                    new_n = operation[b](n, a); new_options = copy.deepcopy(options)
                    if new_n<=0 or new_n>9999: continue
                    new_options.remove(a)
                    new_path = copy.deepcopy(path); new_path.append(f"{n} {'+-*/'[b]} {a} = {new_n}")
                    new_score = abs(self.__target-new_n)
                    queue.append([new_n, new_path, new_options, new_score])
                    queue.sort(key=lambda x: x[-1])
        return None
    
    def solve(self):
        '''
        Solve the Countdown module

        Returns:
            tuple (str, ...): The solution to solve the module. Use the numbers and the operation stated on each index.
        '''
        return tuple(self.__calculate())