from ..edgework import edgework
from ..morsedict import _translate

class morsecode(edgework):
    __bank = {
        "beats": '3.600',
        "bistro": '3.552',
        "bombs": '3.565',
        "boxes": '3.535',
        "break": '3.572',
        "brick": '3.575',
        "flick": '3.555',
        "halls": '3.515',
        "leaks": '3.542',
        "shell": '3.505',
        "slick": '3.522',
        "steak": '3.582',
        "sting": '3.592',
        "strobe": '3.545',
        "trick": '3.532',
        "vector": '3.595'
    }
    
    
    def __check(self, m):
        if not isinstance(m, list): raise TypeError("Morse has an invalid type")
        elif len(m)<1: raise IndexError("Morse must have at least 1 letter")
        elif any([True if not isinstance(a, str) else False for a in m]): raise TypeError("One of morse list has an invalid type")
        elif any([True if set(a)!={'-','.'} and set(a)!={'-'} and set(a)!={'.'} else False for a in m]): raise ValueError("Morse must be made out of dots ('.') and dashes ('-')")
        else: return m
    
    def __init__(self, edgework: edgework, morse: str):
        '''
        Initialize a new morsecode instance

        Args:
            edgework (edgework): The edgework of the bomb
            morse (List [str]): The morse code in the form of dots ('.') and dashes ('-')
        '''
        super().__init__(edgework.batt, edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.strikes)
        self.__morsecode = self.__check(morse)
    
    def solve(self):
        '''
        Solve the Morse Code module

        Returns:
            (tuple (str), tuple (str)): First tuple are all of the possible words with those sets of morse, Second tuple are the number code to be submitted

        '''
        ans = [a for a in self.__bank if ''.join(_translate(self.__morsecode)) == a[0:len(self.__morsecode)]]
        if ans == None:
            raise IndexError("Cannot find word with these set of morse code")
        return tuple(ans), tuple([self.__bank[a] for a in ans])