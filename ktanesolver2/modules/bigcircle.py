from ..edgework import edgework

class bigcircle(edgework):
    __collist = [
        ['red', 'yellow', 'blue'],
        ['orange', 'green', 'magenta'],
        ['blue', 'black', 'red'],
        ['magenta', 'white', 'orange'],
        ['orange', 'blue', 'black'],
        ['green', 'red', 'white'],
        ['magenta', 'yellow', 'black'],
        ['red', 'orange', 'yellow'],
        ['yellow', 'green', 'blue'],
        ['blue', 'magenta', 'red'],
        ['black', 'white', 'green'],
        ['white', 'yellow', 'blue']
    ]
    
    def __check(self, r, s):
        if not isinstance(r, int): raise TypeError("Rotation has an invalid type")
        elif not isinstance(s, int): raise TypeError("Solved has an invalid type")
        elif r != 0 and r != 1: raise ValueError("Rotation must either be 0 or 1")
        elif s < 0: raise ValueError("Solved cannot be below 0")
        else: return r, s
    
    def __init__(self, edgework: edgework, rotation: int, solved: int):
        '''
        Initialize a new bigcircle instance.

        Args:
            edgework (edgework): The edgework of the bomb
            rotation (int, 0 or 1): Rotation of the module, 0 represents clockwise and 1 represents counter-clockwise
            solved (int): Solved modules on the bomb
        '''
        super().__init__(edgework.batt, edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__rotation, self.__solved = self.__check(rotation, solved)
    
    def __iter(self, arr, p):
        temp = 0
        for a in arr:
            if a+'*' in self._litind: temp += p
            if a in self._unlitind: temp -= p
        return temp

    def __calculate(self):
        point = 0
        point = self.__iter(['BOB', 'CAR', 'CLR'], 1) + self.__iter(['FRK', 'FRQ', 'MSA', 'NSA'], 2) + self.__iter(['SIG', 'SND', 'TRN'], 3) + (3*self.__solved) + (4 if self.batt%2 == 1 else -4)
        for a in self.ports:
            if 'PARALLEL' in a: point += -4 if 'SERIAL' in a else 5
            if 'DVI-D' in a: point += 4 if 'RCA' in a else -5
        return point
        # not supporting custom indicators and ports

    def solve(self):
        '''
        Solve the Big Circle module

        Returns:
            (str, str, str): The order of color presses in a form of tuple, where index 0 is the first and 2 is the last in the sequence
        '''
        return tuple(self.__collist[int(self.__calculate()/3)]) if self.__rotation == 0 else tuple(self.__collist[int(self.__calculate()/3)][::-1])
