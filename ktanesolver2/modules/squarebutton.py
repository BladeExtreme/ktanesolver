from ..edgework import edgework
from ..tools.colordict import _colorcheck

class squarebutton(edgework):
    def __check(self, c,l):
        if not isinstance(c, str): raise TypeError("color must be in str")
        elif not isinstance(l, str): raise TypeError("label must be in str")
        return _colorcheck(c.lower()), l.lower().replace(" ","")
    
    def __init__(self, edgework:edgework, color:str, label:str):
        '''
        Initialize a new squarebutton instance

        Args:
            edgework (edgework): The edgework of the bomb
            color (str): The color of the square button
            label (str): The lalbel of the square button
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__color, self.__label = self.__check(color, label)
    
    def __calculate(self):
        colorlabel = ['red','blue','green','yellow','orange','white','black','cyan','magenta','gray','purple','pink','jade','indigo','maroon']

        if self.__color=='blue' and (self.batt-self.hold)*2 > self.batt-((self.batt-self.hold)*2): return 'HOLD'
        elif self.__color in ['yellow', 'blue'] and int(max(self._sndigit))==len(self.__label): return 'PRESS'
        elif self.__color in ['yellow', 'blue'] and self.__label in colorlabel: return 'HOLD'
        elif self.__label == "": return tuple(['PRESS', tuple(['00','11','22','33','44','55'])])
        elif self.__color!='dark gray' and len(self.__label)>len(self._litind): return 'PRESS'
        elif len(self._unlitind)>=2 and any([a in 'AIUEO' for a in self._snletter]): return 'PRESS'
        else: return 'HOLD'
    
    def solve(self):
        '''
        Solve the Square Button module

        Returns:
            str|tuple [str, tuple[str]]: State to press or hold the button any time or in a specific time. If it's a tuple, index 1 represent which seconds should be released
        '''
        return self.__calculate()
    
    def holding(self, color:str, minutes:int, flickering:bool|None=False):
        '''
        Find when the correct time to release the held button

        Args:
            color (str): The color of the LED
            minutes (int): The minute when the button is desired to be released (for flickering cyan rule)
            flickering (bool|None): Stateif the color of the led is flickering or not. By default is False
        Returns:
            tuple: The list of seconds where the button can be released
        '''
        if not isinstance(color, str): raise TypeError("color must be in str")
        elif not isinstance(flickering, bool): raise TypeError("flickering must be in bool")
        elif not isinstance(minutes, int): raise TypeError("minutes must be in int")
        self.__colorled = _colorcheck(color.lower())
        if not flickering:
            if self.__colorled=='cyan': return tuple([a for a in range(60) if sum([int(x) for x in str(a)])==7])
            elif self.__colorled=='orange': return tuple([a for a in range(60) if sum([int(x) for x in str(a)])==3 or sum([int(x) for x in str(a)])==13])
            else: return tuple([a for a in range(60) if sum([int(x) for x in str(a)])==5])
        else:
            if self.__colorled=='cyan': return tuple([a for a in range(60) if (a+minutes)%7==0])
            elif self.__colorled=='orange': return tuple([a for a in range(60) if a in [0,2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59]])
            else: return tuple([a-1 for a in range(1,60) if sum([int(x) for x in str(a)])%4==0])