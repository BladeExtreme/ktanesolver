from ..edgework import edgework # type: ignore
from ..tools.colordict import _colorcheck # type: ignore

class wires(edgework):
    __rule = {
        3: [1,1,2],
        4: ['r',0,0,3,1],
        5: [3,0,1,0],
        6: [2,3,5,3]
    }

    def __init__(self, edgework, color: str):
        super().__init__(edgework.batt, edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__color = _colorcheck(self.__check(color))
    
    def __check(self, c):
        if not isinstance(c, list): raise TypeError("Color is not in the correct type")
        elif len(c) < 3 or len(c) > 6: raise IndexError(f"Color's length is invalid, {len(c)}")
        elif not all([isinstance(a, str) for a in c]): raise TypeError("Color's list has an invalid type")
        return c
    
    def __calculate(self, color, length):
        if (length==3 and color == ['blue', 'blue', 'red']) or \
        (color.count('red') >= 2 and int(self._sndigit[-1]) % 2 == 1 and length==4) or \
        (length==5 and color[-1] == 'black' and int(self._sndigit[-1]) % 2 == 1) or \
        (length==6 and color.count('yellow') == 0 and int(self._sndigit[-1]) % 2 == 1):
            return 0
        elif (length==3 and color.count('red') == 0) or \
        (length==4 and color[-1] == 'yellow' and color.count('red') == 0) or \
        (length==5 and color.count('red') == 1 and color.count('yellow') >= 2) or \
        (length==6 and color.count('yellow') == 1 and color.count('white') >= 2):
            return 1
        elif (length==3) or (length==4 and color.count('blue') == 1) or \
        (length == 5 and color.count('black') == 0) or \
        (length == 6 and color.count('red') == 0):
            return 2
        elif (length==4 and color.count('yellow') >= 2) or length==5 or length==6:
            return 3
        else: return 4

    def solve(self):
        ans = self.__rule[len(self.__color)][self.__calculate(self.__color, len(self.__color))]
        if ans == 'r':
            for a in range(len(self.__color)):
                if self.__color[a] == 'red': ans = a
        return tuple([ans, str(ans+1)+('st' if ans+1==1 else 'nd' if ans+1==2 else 'rd' if ans+1==3 else 'th'), self.__color[ans]])
