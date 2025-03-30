from ..edgework import edgework # type: ignore
from ..tools.colordict import _colorcheck # type: ignore

class button(edgework):
    __rule = {
        'abort': {'blue': 'HOLD', 'red': 'x', 'white':['x', 'HOLD'], 'yellow': 'x'},
        'detonate1': {'blue': 'HOLD', 'red': 'HOLD', 'white':['HOLD', 'HOLD'], 'yellow': 'HOLD'},
        'detonate2': {'blue': 'TAP', 'red': 'TAP', 'white':['TAP', 'TAP'], 'yellow': 'TAP'},
        'hold': {'blue': 'x', 'red': 'TAP', 'white':['x', 'HOLD'], 'yellow': 'x'},
        'press': {'blue': 'x', 'red': 'x', 'white':['x', 'HOLD'], 'yellow': 'x'}
        }

    def __init__(self, edgework, color: str, label: str):
        super().__init__(edgework.batt, edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__color, self.__label = self.__check(_colorcheck(color.lower()), label.lower())
    
    def __check(self, c, l):
        if not isinstance(c, str): raise TypeError("Color is not in the correct type")
        elif not isinstance(l, str): raise TypeError("Label is not in the correct type")
        return c, l

    def __calculate(self):
        if self.__label == 'detonate': self.__label = self.__label+'1' if self.batt <= 1 else self.__label+'2'
        if self.__color == 'white': idx = 0 if 'CAR' not in self.ind else 1
        else: idx = -1
        x = 't' if self.batt >= 3 and 'FRK' in self.litind else 'h'
        return idx, x

    def solve(self):
        idx, x = self.__calculate()
        ans = self.__rule[self.__label][self.__color]
        
        if isinstance(ans, list): ans = ans[idx]
        
        if ans == 'x':
            if x == 'HOLD': ans == 'HOLD'
            elif x == 'TAP': ans == 'TAP'
        
        return ans

    def holding(self ,color:str):
        color = _colorcheck(color.lower())

        if color == 'blue': return 4
        elif color == 'yellow': return 5
        else: return 1
