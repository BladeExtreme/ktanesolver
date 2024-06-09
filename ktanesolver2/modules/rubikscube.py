from ..edgework import edgework
from ..tools.colordict import _colorcheck

class rubikscube(edgework):
    def __check(self, c):
        if not isinstance(c, dict): raise TypeError("colorlist must be in dict")
        elif len(c) != 5: raise IndexError("Length of colorlist must be 5")
        elif not all([isinstance(a, str) for a in c.keys()]): raise TypeError("Keys of colorllist must be in str")
        elif not all([a in ['d','l','f','u','r'] for a in c]): raise KeyError("Keys must be: u,l,f,d,r only")
        elif not all([isinstance(a, str) for a in c.values()]): raise TypeError("Values of colorllist must be in str")
        temp = {}
        for a,b in zip(c.keys(), c.values()): temp[a] = _colorcheck(b)
        return temp
        
    
    def __init__(self, edgework:edgework, color:dict):
        '''
        Initialize a new rubikscube instance

        Args:
            edgework (edgework): The edgework of the bomb
            color (dict {'u': str, 'l': str, ...}): The color of the middle piece in the cube. Keys of color must be only 'u', 'l', 'f', 'd', 'r' for their respective sides.
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__color = self.__check(color)
    
    def __calculate(self):
        col2num = {
            'yellow': 1, 'blue': 2,
            'red': 3, 'green': 4,
            'orange': 5, 'white': 6
        }
        movelist = [
            ["L'","F'"],["D'","U'"],["U","B'"],["F","B"],["L","D"],["R'","U"],["U'","F"],["B'","L'"],["B","R"],["D","L"],["R","D'"],["F'","R'"]
        ]
        invalid = col2num[self.__color['d']]-1; skips = [col2num[a] for a in [self.__color['u'], self.__color['l'], self.__color['f']]]
        validsn = [int(self.sn[a]) if self.sn[a].isnumeric() else int(ord(self.sn[a])-55) for a in range(len(self.sn)) if a != invalid]
        ans = []
        if self.__color['r'] in ['red', 'green', 'blue']:
            for a in validsn: ans.append(movelist[(int((a-(a%3))/3)+skips[a%3])%12])
        else:
            ans1 = []
            for a in validsn:
                ans.append(movelist[(int((a-(a%3))/3)+skips[a%3])%12])[0]
                ans1.append(movelist[(int((a-(a%3))/3)+skips[a%3])%12])[1]
            ans.append(ans1)
        ans = [a for b in ans for a in b]
        if self.__color['r'] in ['red', 'yellow', 'green']:
            for a in range(5):
                if "'" in ans[a]: ans[a].replace("'", "")
                else: ans[a] += "'"
        if self.__color['r'] in ['green', 'white']: ans = ans[::-1]
        
        return tuple(ans)


    def solve(self):
        '''
        Solve the Rubik's Cube module

        Returns:
            tuple (str, ...): The solution to solve the rubik's cube
        '''
        ans = self.__calculate()
        return ans
