from ..edgework import edgework
from ..tools.colordict import _colorcheck

class ledencryption(edgework):
    __multillist = {
        'red': 2, 'green': 3,
        'blue': 4, 'yellow': 5,
        'purlpe': 6, 'orange': 7
    }
    
    def __check(self, m):
        if not isinstance(m, list): raise TypeError("multiplier must be in list")
        elif not all([isinstance(a, str) for a in m]): raise TypeError("Element of multiplier must be in str")
        return [_colorcheck(a.lower()) for a in m]
    
    def __init__(self, edgework:edgework, multiplier:list):
        '''
        Initialize a new ledencryption instance

        Args:
            edgework (edgework): The edgework of the bomb
            multiplier (list [str, ...]): The color list that appears on the top of the module
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__multiplier = self.__check(multiplier)
    
    def __calculate(self, l, m):
        for a in range(len(l)):
            if (int(ord(l[a])-65)*self.__multillist[m])%26 == int(ord(l[-1-a]))-65: return l[a], a

    def solve(self, letters):
        '''
        Solve the LED Encryption module

        Args:
            letters (list [str, ...]): The letters that appears on the module
        Returns:
            str: The correct letter to press
            int: The index of the correct letter to press from the given list
        '''
        if not isinstance(letters, list): raise TypeError("Letters must be in list")
        elif len(letters) != 4: raise IndexError("Length of letters must be 4")
        elif not all([isinstance(a, str) for a in letters]): raise TypeError("Element of letters must be in str")
        elif not all([len(a)==1 for a in letters]): raise IndexError("Length of letters' elements must be 1")
        
        currmulti = self.__multiplier.pop(0)
        ans, idx = self.__calculate([a.upper() for a in letters], currmulti)
        return tuple([ans, idx])