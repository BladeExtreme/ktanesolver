from ..edgework import edgework

class astrology(edgework):
    __elemword = ['fire', 'water', 'earth', 'air']
    __planword = ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto']
    __zodiword = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']
    __table = [
        [
            [0, 0, 1, -1, 0, 1, -2, 2, 0, -1],
            [-2, 0, -1, 0, 2, 0, -2, 2, 0, 1],
            [-1, -1, 0, -1, 1, 2, 0, 2, 1, -2],
            [-1, 2, -1, 0, -2, -1, 0, 2, -2, 2]
        ],[
            [1, 0, -1, 0, 0, 2, 2, 0, 1, 0, 1, 0],
            [2, 2, -1, 2, -1, -1, -2, 1, 2, 0, 0, 2],
            [-2, -1, 0, 0, 1, 0, 1, 2, -1, -2, 1, 1],
            [1, 1, -2, -2, 2, 0, -1, 1, 0, 0, -1, -1]
        ],[
            [-1, -1, 2, 0, -1, 0, -1, 1, 0, 0, -2, -2],
            [-2, 0, 1, 0, 2, 0, -1, 1, 2, 0, 1, 0],
            [-2, -2, -1, -1, 1, -1, 0, -2, 0, 0, -1, 1],
            [-2, 2, -2, 0, 0, 1, -1, 0, 2, -2, -1, 1],
            [-2, 0, -1, -2, -2, -2, -1, 1, 1, 1, 0, -1],
            [-1, -2, 1, -1, 0, 0, 0, 1, 0, -1, 2, 0],
            [-1, -1, 0, 0, 1, 1, 0, 0, 0, 0, -1, -1],
            [-1, 2, 0, 0, 1, -2, 1, 0, 2, -1, 1, 0],
            [1, 0, 2, 1, -1, 1, 1, 1, 0, -2, 2, 0],
            [-1, 0, 0, -1, -2, 1, 2, 1, 1, 0, 0, -1]
      ]
    ]
    
    def __check(self, e,p,z):
        if not isinstance(e, str): raise TypeError("element must be in str")
        elif e.lower() not in self.__elemword: raise ValueError("This element cannot be found in list. Use showNames('element')")
        elif not isinstance(p, str): raise TypeError("planet must be in str")
        elif p.lower() not in self.__planword: raise ValueError("This planet cannot be found in list. Use showNames('planet')")
        elif not isinstance(z, str): raise TypeError("zodiac must be in str")
        elif z.lower() not in self.__zodiword: raise ValueError("This zodiac cannot be found in list. Use showNames('zodiac')")
        return [e.lower(), p.lower(), z.lower()]
    
    def __init__(self, edgework:edgework, element:str, planet:str, zodiac: str):
        '''
        Initialize a new astrolog instance

        Args:
            edgework (edgework): The edgework of the bomb
            element (str): The element/most left symbol name
            planet (str): The planet/middle symbol name
            zodiac (str): The zodiac/most right symbol name
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__symbol = self.__check(element, planet, zodiac)
    
    def __calculate(self):
        omen = 0
        omen += self.__table[self.__elemword.index(self.__symbol[0])][self.__planword.index(self.__symbol[1])]
        omen += self.__table[self.__elemword.index(self.__symbol[0])][self.__zodiword.index(self.__symbol[2])]
        omen += self.__table[self.__planword.index(self.__symbol[1])][self.__zodiword.index(self.__symbol[2])]
        for a in self.__symbol:
            if any([b.upper() in self._snletter for b in a]): omen+=2
        return tuple(['GOOD', omen]) if omen>0 else tuple(['BAD', omen]) if omen<0 else tuple(['NO', '-'])

    def solve(self):
        '''
        Solve the Astrology module

        Returns:
            tuple (str, int|str): Press either 'GOOD', 'BAD' or 'NO' omen according to index 0 of tuple when the timer has the digit mentioned in index 1 in any timer
        '''
        return self.__calculate()