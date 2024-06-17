from ..edgework import edgework
from ..tools.colordict import _colorcheck

class neutralization(edgework):
    __acidtable = {
        'red': {'formula': 'HBr', 'symbol': 'Br', 'number': 35},
        'yellow': {'formula': 'HF', 'symbol': 'F', 'number': 9},
        'green': {'formula': 'HCl', 'symbol': 'Cl', 'number': 17},
        'blue': {'formula': 'HI', 'symbol': 'I', 'number': 53}
    }
    __basetable = {
        'ammonia': {'formula': 'NH3', 'symbol': 'H', 'number': 1},
        'lithium': {'formula': 'LiOH', 'symbol': 'Li', 'number': 3},
        'sodium': {'formula': 'NaOH', 'symbol': 'Na', 'number': 11},
        'potassium': {'formula': 'KOH', 'symbol': 'K', 'number': 19}
    }
    __solubletable = {
        'HBr': {'NH3': False, 'KOH': True, 'LiOH': True, 'NaOH': False},
        'HF': {'NH3': True, 'KOH': False, 'LiOH': True, 'NaOH': False},
        'HCl': {'NH3': True, 'KOH': True, 'LiOH': False, 'NaOH': True},
        'HI': {'NH3': False, 'KOH': False, 'LiOH': False, 'NaOH': True}
    }

    def __check(self, c, v):
        if not isinstance(c, str): raise TypeError("chemcolor must be in str")
        elif not isinstance(v, int): raise TypeError("volume must be in int")
        elif v<0: raise ValueError("volume cannot be negative")
        return _colorcheck(c.lower()), v

    def __init__(self, edgework:edgework, chemcolor:str, volume:int):
        '''
        Initialize a new neutralization instance

        Args:
            edgework (edgework): The edgework of the bomb
            chemcolor (str): The color of the chemical inside the tube
            volume (int): The volume of the chemical
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__chemcolor, self.__volume = self.__check(chemcolor, volume)
    
    def __calculate(self):
        acid = self.__acidtable[self.__chemcolor].copy()
        if ('NSA' in self.ind or 'NSA*' in self.ind) and self.batt==3: base = self.__basetable['ammonia'].copy()
        elif any([a in ['CAR*','FRQ*','IND*'] for a in self._litind]): base = self.__basetable['potassium'].copy()
        elif len(self._uniqueports)==0 and any([a in ['A','I','U','E','O'] for a in self._snletter]): base = self.__basetable['lithium'].copy()
        elif any([any([a.upper() in b for b in self.ind]) for a in acid['formula']]): base = self.__basetable['potassium'].copy()
        elif self.batt-((self.batt-self.hold)*2)>(self.batt-self.hold)*2: base = self.__basetable['ammonia'].copy()
        elif acid['number']<20: base = self.__basetable['sodium'].copy()
        else: base = self.__basetable['lithium'].copy()

        concA = acid['number']-base['number']
        if any([any([b in ['A','I','U','E','O'] for b in a]) for a in acid['symbol']]) or any([any([b in ['A','I','U','E','O'] for b in a]) for a in base['symbol']]): concA-=4
        if len(acid['symbol'])==len(base['symbol']): concA*=3
        concA = concA%10 if concA%10!=0 else int((self.__volume*2)/5); concA /= 10

        if (acid['formula']=='HI' and base['formula']=='KOH') or (acid['formula']=='HCl' and base['formula']=='NH3'): concB=20
        elif self.hold>len(self._uniqueports) and self.hold>len(self.ind): concB = 5
        elif len(self._uniqueports)>self.hold and len(self._uniqueports)>len(self.ind): concB = 10
        elif len(self.ind)>len(self._uniqueports) and len(self.ind)>self.hold: concB = 20
        else:
            temp = base['number']; comparison = [abs(5-temp), abs(10-temp), abs(20-temp)]
            tempidx = comparison.index(min(comparison))
            if tempidx==0: concB=5
            elif tempidx==1: concB=10
            else: concB=20
        
        drop = int((20/concB)*self.__volume*concA)
        soluble = 'ON' if self.__solubletable[acid['formula']][base['formula']] else 'OFF'
        return tuple([base['formula'], drop, soluble])

    def solve(self):
        '''
        Solve the Neutralization module

        Returns:
            tuple (str, int, str): The answer to submit neutralization. Index 0 is the required formula to use, index 1 is the amount of drop count to submit and index 2 is the state to use filter or not. Index 2 only outputs: 'OFF' or 'ON'
        '''
        return self.__calculate()