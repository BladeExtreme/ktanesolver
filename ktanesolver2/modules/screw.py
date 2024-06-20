from ..edgework import edgework
from ..tools.colordict import _colorcheck

class screw(edgework):
    def __check2(self, c,b):
        if not isinstance(c, str): raise TypeError("colorhole must be in str")
        elif not isinstance(b, list): raise TypeError("buttons must be in list")
        elif len(b)!=4: raise IndexError("Length of buttons must be 4")
        elif not all([isinstance(a,str) for a in b]): raise TypeError("Element of buttons must be in str")
        elif not all([len(a)==1 for a in b]): raise IndexError("Length of each letter must only be 1")
        return _colorcheck(c.lower()), [a.upper() for a in b]
    
    def __check(self, i,c):
        if not isinstance(c, list): raise TypeError("colorhole must be in list")
        elif not isinstance(i, str): raise TypeError("initial must be in list")
        elif len(c)!=6: raise IndexError("Length of colorhole must be 6")
        elif not all([isinstance(a, str) for a in c]): raise TypeError("Element of colorhole must be in str")
        return [_colorcheck(a.lower()) for a in c], _colorcheck(i.lower())
    
    def __init__(self, edgework:edgework, initialcolor: str, colorhole:list[str]):
        '''
        Initialize a new screw instance

        Args:
            edgework (edgework): The edgework of the bomb
            colorhole (list [str]): The list of the holes' outline colors
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__color, self.__initial = self.__check(initialcolor, colorhole)
    
    def __calculate1(self):
        if self.__colorhole in ['red','yellow','green']:
            if self.__color.index(self.__colorhole)<3:
                row = self.__color[0:3]
                if row.index(self.__colorhole)==self.hold-1: return self.__buttons[3]
                elif self.__buttons.index('A') in [0,2]: return 'C'
                elif any([a in ['CLR','FRK','TRN','CLR*','FRK*','TRN*'] for a in self.ind]): return self.__buttons[2]
                elif self.__buttons.index('blue')<3: return self.__buttons[0]
                else: return 'B'
            else:
                row = self.__color[3:]
                if row.index(self.__colorhole)==len(self._uniqueports)-1: return self.__buttons[1]
                elif row.index(self.__colorhole)==self.batt-1: return 'D'
                elif self.__color[self.__color.index(self.__colorhole)+3]!='white': 'A'
                elif (row[row.index(self.__colorhole)+1]=='magenta' if row.index(self.__colorhole)<2 else False) or (row[row.index(self.__colorhole)-1]=='magenta' if row.index(self.__colorhole)>0 else False): return 'C'
                else: return self.__buttons[0]
        else:
            if self.__color.index(self.__colorhole)<3:
                row = self.__color[0:3]
                if row.index(self.__colorhole)==len(self._uniqueports)-1: return 'D'
                elif self.__buttons.index('C') in [1,3]: return 'B'
                elif any([a in ['CAR','FRQ','SND','CAR*','FRQ*','SND*'] for a in self.ind]): return self.__buttons[3]
                elif self.__color.index('red')<3: return self.__buttons[1]
                else: return 'A'
            else:
                row = self.__color[3:]
                if row.index(self.__colorhole)==len(self.ports)-1: return self.__buttons[1]
                elif row.index(self.__colorhole)==len(self.ind)-1: return 'A'
                elif (row[row.index(self.__colorhole)+1]=='yellow' if row.index(self.__colorhole)<2 else False) or (row[row.index(self.__colorhole)-1]=='yellow' if row.index(self.__colorhole)>0 else False): return 'C'
                elif self.__color.index('green')==self.__color.index(self.__colorhole)-3: return self.__buttons[3]
                else: return 'D'

    def __calculate(self):
        ans = [self.__color.index(self.__initial), ((self.batt+len(self._unlitind))%6)-1 if self.batt+len(self._unlitind)!=0 else 0, ((int(self._sndigit[-1])+len(self._litind))%6)-1 if int(self._sndigit[-1])+len(self._litind)!=0 else 0, ((len([a for b in self.ports for a in b])+self.hold)%6)-1 if len([a for b in self.ports for a in b])+self.hold!=0 else 0]
        for a in range(1, len(ans)):
            if len(set(ans[a-1:a+1]))!=2:
                for b in range(1,6):
                    ans[a] = (ans[a]+1)%6
                    if len(set(ans[a-1:a+1]))==2: break
        return tuple([self.__color[a] for a in ans[1:]])

    def solve(self, colorhole:str|None=None, buttons:list[str]|None=None):
        '''
        Solve the Screw module

        Args:
            colorhole (str|None): The current color of the screw's hole
            buttons (list [str]|None): The button list from left to right
        Returns:
            str: The letter button to press
        '''
        if colorhole is not None and buttons is not None:
            self.__colorhole, self.__buttons = self.__check2(colorhole,buttons)
            return self.__calculate1()
        elif (colorhole is None)^(buttons is None): raise TypeError("screw.solve() missing 0 or 2 required positional argument: 'colorhole' and 'buttons'")
        return self.__calculate()