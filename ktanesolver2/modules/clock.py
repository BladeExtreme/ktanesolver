from ..edgework import edgework
from ..tools.colordict import _colorcheck

class clock(edgework):
    def __check(self, c,m):
        if not isinstance(c, dict): raise TypeError("clock must be in dict")
        elif not isinstance(m, bool): raise TypeError("morethanhalf must be in bool")
        elif not all([a in ['casecolor','handcolor','tickcolor','ampmcolor','numeraltype','handshape','seconds'] for a in c.keys()]): raise KeyError("Key must consist of: 'casecolor', 'handcolor', 'tickcolor', 'ampmcolor', 'numeraltype', 'handshape', 'seconds'")
        elif not all([isinstance(b, str) if a.lower() in ['casecolor','handcolor','tickcolor','ampmcolor','numeraltype','handshape'] else isinstance(b, bool) for a,b in c.items()]): raise TypeError("Value of 'casecolor', 'handcolor', 'tickcolor', 'ampmcolor', 'numeraltype', 'handshape' must be in str. Value of 'seconds' must be in bool")
        elif not all([c['numeraltype'].lower() in ['roman','arabic','none'] and c['handshape'].lower() in ['lines','spades','arrows']]): raise ValueError("'numeraltype' value must be either: ['roman','arabic','none'] and 'handshape' value must be either: ['lines', 'arrows' or 'spades']")
        return {'numeraltype': c['numeraltype'].lower(), 'casecolor': _colorcheck(c['casecolor'].lower()), 'match': _colorcheck(c['handcolor'].lower())==_colorcheck(c['tickcolor'].lower()), 'handshape': c['handshape'].lower(), 'tickcolor': _colorcheck(c['tickcolor'].lower()), 'ampm': _colorcheck(c['ampmcolor'].lower()), 'seconds': c['seconds']}, m
    
    def __init__(self, edgework:edgework, clock:dict[str,str|bool], morethanhalf:bool):
        '''
        Initialize a new clock instance

        Args:
            edgework (edgework): The edgework of the bomb
            clock (dict [str,str|bool]): The information of the clock in the module. Key must consist of: 'casecolor', 'handcolor', 'tickcolor', 'ampmcolor', 'numeraltype', 'handshape', 'seconds'. Value of 'casecolor', 'handcolor', 'tickcolor', 'ampmcolor' must be in str and represent color. Value of 'numeraltype', 'handshape' must be in str. 'numeraltype' value must be either: ['roman','arabic','none'] and 'handshape' value must be either: ['lines', 'arrows' or 'spades']. 'seconds' must be in bool
            morethanhalf (bool): The state if the bomb's timer pasts its halftime
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__clock, self.__morethanhalf = self.__check(clock,morethanhalf)
    
    def __calculate(self):
        hours = range(12)[sum([(['roman','none','arabic'].index(self.__clock['numeraltype']))*4, ['silver','gold'].index(self.__clock['casecolor'])*2, int(not self.__clock['match'])])-1]
        minutes = range(1,61)[sum([(['lines','spades','arrows'].index(self.__clock['handshape']))*20, ['red','green','blue','gold','black'].index(self.__clock['tickcolor'])*4, ['black','white'].index(self.__clock['ampm'])*2, int(not self.__clock['seconds'])])-10]
        if minutes==0: hours+=1
        return {'hour': hours, 'minute': minutes, 'mode': 'add' if self.__morethanhalf else 'subtract'}

    def solve(self):
        '''
        Solve the Clock module

        Returns:
            dict (str, str): The amount of time needed to be added/subtracted. Keys of dicts are: 'hour', 'minute' and 'mode'. 'hour' represents the amount of hour, 'minute' represents the amount of minute, and 'mode' represents to subtract or add from the base minute
        '''
        return self.__calculate()