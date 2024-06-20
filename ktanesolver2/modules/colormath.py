from ..edgework import edgework
from ..tools.colordict import _colorcheck

class colormath(edgework):
    def __check(self, c, o):
        if not isinstance(c, dict): raise TypeError("color must be in dict")
        elif not isinstance(o, dict): raise TypeError("operations must be in dict")
        elif not all([a in ['left','right'] for a in c]): raise KeyError("Key of color must consist of: 'left' and 'right'")
        elif not all([isinstance(a, list) for a in c.values()]): raise TypeError("Value of color must be in list")
        elif not all([len(a)==4 for a in c.values()]): raise IndexError("Length of color's value lists must be 4")
        elif not all([all([isinstance(b, str) for b in a]) for a in c.values()]): raise TypeError("Each element of color's value lists must be in str")
        elif not all([a in ['letter', 'color'] for a in o]): raise KeyError("Key of operation must consist of: 'letter' and 'color'")
        elif not all([isinstance(a, str) for a in o.values()]): raise TypeError("Value of operation must be in str")
        return {'left': [_colorcheck(a.lower()) for a in c['left']], 'right': [_colorcheck(a.lower()) for a in c['right']]}, {'letter': o['letter'].lower(), 'color': _colorcheck(o['color'].lower())}

    def __init__(self, edgework:edgework, color:dict[str,list[str]], operation:dict[str,str]):
        '''
        Initialize a new colormath instance

        Args:
            edgework (edgework): The edgework of the bomb
            color (dict [str, list[str]]): The color of each circles from top to bottom on both sides. Key of color must consist of: 'left' and 'right' representing left side and right side. In list, index 0 represents the topmost circle and index 3 represents the bottommost circle
            operation (dict [str,str]): The letter and the color of the operator in the middle. Key of operation must consist of: 'letter' and 'color' representing the letter and the color of the operator in the middle.
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__color, self.__operator = self.__check(color, operation)

    def __calculate(self):
        operator = {
            'a': lambda x,y: (x+y)%10000,
            'm': lambda x,y: (x*y)%10000,
            's': lambda x,y: (abs(x-y))%10000,
            'd': lambda x,y: (int(x/y))%10000
        }
        conversiontable = {0: ['gray', 'blue', 'magenta', 'gray'], 1: ['green', 'green', 'yellow', 'blue'], 2: ['orange', 'black', 'blue', 'purple'], 3: ['white', 'purple', 'gray', 'red'], 4: ['purple', 'magenta', 'red', 'yellow'], 5: ['blue', 'red', 'black', 'magenta'], 6: ['magenta', 'gray', 'green', 'black'], 7: ['black', 'yellow', 'purple', 'orange'], 8: ['yellow', 'orange', 'orange', 'green'], 9: ['red', 'white', 'white', 'white']}
        leftside = {'blue': [6, 8, 4, 6],'green': [1, 1, 1, 8],'purple': [2, 9, 9, 7],'yellow': [4, 4, 7, 5],'white': [9, 3, 0, 4],'magenta': [0, 6, 2, 9],'red': [8, 0, 5, 1],'orange': [5, 5, 3, 3],'gray': [3, 7, 8, 0],'black': [7, 2, 6, 2]}
        rightside = {'blue': [0, 2, 5, 5],'green': [6, 9, 0, 4],'purple': [5, 8, 6, 2],'yellow': [4, 0, 4, 9],'white': [3, 5, 2, 8],'magenta': [7, 3, 7, 6],'red': [9, 4, 9, 7],'orange': [8, 7, 3, 1],'gray': [1, 1, 8, 3],'black': [2, 6, 1, 0]}
        asmd = [
            [int(self._sndigit[0]), len(self._unlitind), 9, [a for b in self.ports for a in b].count('RJ-45')],
            [0, [a for b in self.ports for a in b].count('PS/2'), len(self._snletter), int(self._sndigit[-1])],
            [len([a for a in self._snletter if a in 'AIUEO']), self.hold, [a for b in self.ports for a in b].count('SERIAL'), 4],
            [[a for b in self.ports for a in b].count('DVI-D'), 5, len([a for a in self._snletter if a not in 'AIUEO']), len(self._litind)]
        ]
        leftnumber = int("".join([str(leftside[a][b]) for a,b in zip(self.__color['left'], range(4))])); func = operator
        if self.__operator['color']=='red':
            func = operator[self.__operator['letter']]
            ans = [int(a) for a in str(func(leftnumber, int("".join(str(x) for x in asmd[0 if self.batt in range(0,2) else 1 if self.batt in range(2,4) else 2 if self.batt in range(4,6) else 3])))).zfill(4)]
        elif self.__operator['color']=='green':
            rightnumber = int("".join([str(rightside[a][b]) for a,b in zip(self.__color['right'], range(4))])); func = operator[self.__operator['letter']]
            ans = [int(a) for a in str(func(leftnumber,rightnumber)).zfill(4)]
        for a in range(len(ans)):
            ans[a] = conversiontable[ans[a]][a]
        return tuple(ans)

    def solve(self):
        '''
        Solve the Color Math module

        Returns:
            tuple [str]: The list of colors that should be inputted to the right side of the module. Index 0 represents the topmost circle and index 3 represents the bottommost circle
        '''
        return self.__calculate()