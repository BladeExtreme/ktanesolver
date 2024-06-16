from ..edgework import edgework
from ..tools.colordict import _colorcheck

class fizzbuzz(edgework):
    def __check(self, c):
        if not isinstance(c, list): raise TypeError("colnum must be in list")
        elif len(c)!=3: raise IndexError("Length of colnum must be 3")
        elif not all([isinstance(a, dict) for a in c]): raise TypeError("Element of colnum must be dict")
        elif not all([all([b in ['color', 'number'] for b in a] for a in c)]): raise KeyError("Keys of colnum must be consist only the following: 'color', 'number'")
        elif not all([all(len(a['number'])==7 for a in c)]): raise KeyError("Length of key number must be 7")
        elif not all([isinstance(a['color'], str) and isinstance(a['number'], str) for a in c]): raise TypeError("Type of 'color' and 'number' value must be in str")
        elif not all([all([b.isnumeric() for b in a['number']]) for a in c]): raise ValueError("Number must consists of numbers only")
        return [{'color': _colorcheck(a['color'].lower()), 'number': a['number']} for a in c]
    def __check2(self, c, n):
        if not isinstance(c, list): raise TypeError("colors must be in list")
        elif not isinstance(n, list): raise TypeError("numbers must be in list")
        elif not len(c)==len(n)==3: raise IndexError("Length of colors and numbers must be 3")
        elif not all([isinstance(a, str) for a in c]): raise TypeError("Element of colors must be in str")
        elif not all([isinstance(a, str) for a in n]): raise TypeError("Element of numbers must be in str")
        elif not all([len(a)==7 for a in n]): raise IndexError("Length of each numbers must be 7")
        elif not all([all([b.isnumeric() for b in a]) for a in n]): raise ValueError("Number must consists of numbers only")
        return [{'color': _colorcheck(c[a].lower()), 'number': n[a]} for a in range(len(c))]
    
    def __init__(self, edgework:edgework, colors:list|None=None, numbers:list|None=None, colnum:list|None=None):
        '''
        Initialize a new fizzbuzz instance

        Args:
            edgework (edgework): The edgework of the bomb
            colors (list (str)): The color of the numbers that appears on the module. CAUTION: colors must be in sync with numbers
            numbers (list (str)): The numbers that appears on the module. CAUTION: numbers must be in sync with colors
            colnum (list (dict)): The numbers and colors in the form of a dict. The wires consists of the following keys only: 'color', 'number'. Both color and number must be in str
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        if colnum is not None:
            self.__colnum = self.__check(colnum)
        elif numbers is not None and colors is not None:
            self.__colnum = self.__check2(colors, numbers)
        else:
            raise TypeError("fizzbuzz.__init__() missing 1 to 2 required positional argument: 'colors', 'numbers' | 'colnum'")
    
    def __calculate(self):
        table = {
            'red': [7, 3, 4, 2, 6, 1, 3],
            'green': [3, 4, 5, 3, 6, 2, 1],
            'blue': [2, 9, 8, 7, 1, 2, 8],
            'yellow': [4, 2, 8, 9, 2, 5, 3],
            'white': [5, 8, 2, 1, 8, 3, 4],
        }
        coltouse = []
        if self.hold>=3: coltouse.append(0)
        if 'SERIAL' in self._uniqueports and 'PARALLEL' in self._uniqueports: coltouse.append(1)
        if len(self._snletter)==len(self._sndigit)==3: coltouse.append(2)
        if 'DVI-D' in self._uniqueports and 'STEREO RCA' in self._uniqueports: coltouse.append(3)
        if self.strikes>=2: coltouse.append(4)
        if self.batt>=5: coltouse.append(5)
        if len(coltouse)==0: coltouse.append(6)
        ans = []
        for a in self.__colnum:
            adder = sum([table[a['color']][b] for b in coltouse])
            newnum = []
            for b in a['number']:
                newnum.append(str((int(b)+adder)%10))
            ans.append('fizzbuzz' if int("".join(newnum))%3==0 and int("".join(newnum))%5==0 else 'fizz' if int("".join(newnum))%3==0 else 'buzz' if int("".join(newnum))%5==0 else a['number'])
        return ans

    def solve(self):
        '''
        Solve the FizzBuzz module

        Returns:
            tuple(str, str, str): The state of the number to solve the module. Index 0 represents the top row number, and index 2 represents the bottom row number.
        '''
        return tuple(self.__calculate())