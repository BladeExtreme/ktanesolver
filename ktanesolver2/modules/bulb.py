import copy
from ..edgework import edgework
from ..tools.colordict import _colorcheck

class bulb(edgework):
    __table = [
        [['I','*','I','U','(O)','S'],['O','U','I','S','*','(O)'],['U','I','S','O','*','(O)'],['U','O','I','S','*','(O)']],
        [['I','U','O','[CLR]','S'],['O','U','O','S','*','(I)'],['U','I','I','~O~','S'],['U','O','O','~I~','S']],
        [['I','*','O','U','(O)','S'],['O','U','I','[FRQ]','S'],['U','I','O','S','*','(O)'],['U','O','S','O','*','(I)']],
        [['I','U','I','[SIG]','S'],['O','*','I','U','(O)','S'],['U','I','I','S','*','(I)'],['U','O','S','I','*','(O)']],
        [['I','U','O','S','*','(O)'],['O','U','O','[FRK]','S'],['U','I','O','~I~','S'],['U','O','O','S','*','(I)']],
        [['I','U','I','S','*','(I)'],['O','*','O','U','(I)','S'],['U','I','S','I','*','(I)'],['U','O','I','~O~','S']],
    ]
    
    def __check(self, c, l, o):
        if not isinstance(c, str): raise TypeError("color must be in str")
        elif not isinstance(l, bool): raise TypeError("light_on must be in bool")
        elif not isinstance(o, bool): raise TypeError("opaque must be bool")
        elif _colorcheck(c.lower()) not in ['red','blue','white','green','yellow','purple']: raise ValueError("color must be either 'red','blue','white','green','yellow', or 'purple'")
        return _colorcheck(c.lower()), l, o
    
    def __init__(self, edgework:edgework, color:str, opaque:bool, light_on:bool):
        '''
        Initialize a bulb instance

        Args:
            edgework (edgework): The edgework of the bomb
            color (str): The color of the bulb
            opqaue (bool): The state of the bulb if it's opaque or not. True represents the bulb is opaque, and False for see-through
            light (bool): The state of the bulb if it's on or not. True represents the bulb is lit and so does for the reverse
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__color, self.__light, self.__opaqueness = self.__check(color, light_on, opaque)
        self.__sequence = []
    
    def __checkSequence(self, new_light=None):
        for a in range(len(self.__sequence)):
            if self.__sequence[a]=='*':
                new_seq = self.__sequence[0:a]+[-1]
                self.__sequence.remove('*')
                return new_seq
            if '(' in self.__sequence[a] and ')' in self.__sequence[a]:
                if not new_light: self.__sequence[a] = 'OI'[('OI'.index(self.__sequence[a][1])+1)%2]
                else: self.__sequence[a] = self.__sequence[a][1]
            if '~' in self.__sequence[a]:
                if not self.__opaqueness: 'OI'[('OI'.index(self.__sequence[a][1])+1)%2]
                else: self.__sequence[a] = self.__sequence[a][1]
            if '[' in self.__sequence[a] and ']' in self.__sequence[a]:
                if self.__sequence[a][1:-1] in self._unlitind or self.__sequence[a][1:-1]+'*' in self._litind: self.__sequence[a] = 'I'
                else: self.__sequence[a] = 'O'
            if self.__sequence[a] == 'U': self.__sequence[a] = 'Unscrew'
            if self.__sequence[a] == 'S': self.__sequence[a] = 'Screw'
        return self.__sequence

    def __calculate(self):
        row = ['red','blue','white','green','yellow','purple'].index(self.__color)
        col = -1
        if self.__light and not self.__opaqueness: col = 0
        elif self.__light and self.__opaqueness: col = 1
        elif not self.__light and any([a in self._unlitind or a+'*' in self._litind for a in ['CAR','IND','MSA','SND']]): col = 2
        elif not self.__light and not any([a in self._unlitind or a+'*' in self._litind for a in ['CAR','IND','MSA','SND']]): col = 3
        self.__sequence = copy.deepcopy(self.__table[row][col])
        return self.__checkSequence()

    def solve(self, new_light:bool=None) -> tuple[str|int]:
        '''
        Solve the Bulb module

        Args:
            new_light: The state if the current bulb's light is on or not AFTER submitting the initial sequences. True represents the bulb is now lit and so does for the reverse

        Returns:
            tuple (str|int): The correct sequence to submit the bulb. If the last index has -1, it means the sequence is not completed and is asking for the current state of the bulb
        '''
        if not isinstance(new_light, bool) and new_light is not None: raise TypeError("new_light must be in bool or None")
        if new_light is not None:
            return tuple(self.__checkSequence(new_light))
        else: return tuple(self.__calculate())