from ..edgework import edgework
from ..tools.colordict import _colorcheck

class complicatedwires(edgework):
    __table = [
        ['c','c','d','b'],
        ['s','c','b','b'],
        ['s','d','p','p'],
        ['s','p','s','d']
    ]
    
    def __check2(self, c,l,s):
        colorlist = ['b','r','w','blue','red','white']
        if not isinstance(c, list): raise TypeError("color must be in list")
        elif not isinstance(l, list): raise TypeError("light must be in list")
        elif not isinstance(s, list): raise TypeError("star must be in list")
        elif not len(c)==len(l)==len(s): raise IndexError("Length of color, list and star must be same")
        elif not all([isinstance(a,str) if isinstance(a,str) and a.lower() in colorlist else False or isinstance(a,list) if isinstance(a,list) and len(a)>1 and all([isinstance(b, str) for b in a]) else False for a in c]): raise TypeError("color must be in str for singular color, or list for multiple colors")
        elif not all([isinstance(a, bool) for a in l]): raise TypeError("element of light must be in bool")
        elif not all([isinstance(a, bool) for a in s]): raise TypeError("element of star must be in bool")
        wires = []
        for x,y,z in zip(c,l,s):
            temp = {'color': [], 'light': [], 'star': []}
            temp['color'] = _colorcheck(x.lower()) if isinstance(x, str) else [_colorcheck(a.lower()) for a in x]
            temp['light'] = y; temp['star'] = z
            wires.append(temp)
        return wires
    
    def __check(self, w):
        if not isinstance(w, list): raise TypeError("wires must be in list")
        elif not all([isinstance(a, dict) for a in w]): raise TypeError("Element of wires must be in dict")
        elif not all([all([b in ['color','light','star'] for b in a]) for a in w]): raise KeyError("Keys of each wires must consist only of: 'color', 'light', and 'star'")
        elif not all([all([isinstance(a['color'], str) or (isinstance(a['color'], list) if isinstance(a['color'], list) and len(a)>1 and all([isinstance(b, str) for b in a['color']]) else False) for a in w]), all([isinstance(a['light'], bool) and isinstance(a['star'], bool) for a in w])]): raise TypeError("Value of each wires must be str for 'color' key (list if multiple colored wire) and bool for 'color' and 'light' keys")
        return w
    
    def __init__(self, edgework:edgework, color:list|None=None, light:list|None=None, star:list|None=None, wires:list|None=None):
        '''
        Initialize a new complicatedwires instance

        Args:
            edgework (edgework): The edgework of the bomb
            color (list [str|list]): Color of the wires in the module in list. Multiple colored wire must be in list. CAUTION: color list must be in sync with light and star
            light (list [str]): State of the wires if star exist or not in the module in list. CAUTION: light list must be in sync with color and star
            star (list [str]): State of the wires if star exist or not in the module in list. CAUTION: star list must be in sync with light and color
            wires (list (dict)]): The wires that appears on the bomb, each wire must be in dict where it contain the following key: 'color', 'light', 'star'. Values for color must be in str, while light and star must be in boolean.
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        if wires is not None:
            self.__wires = self.__check(wires)
        elif color is not None and light is not None and star is not None:
            self.__wires = self.__check2(color,light,star)
        else:
            raise TypeError("complicatedwires.__init__() missing 1 or 3 required positional arguments: 'color', 'light', and 'star' | 'wires'")
    
    def __calculate(self):
        ans = []
        for a in range(len(self.__wires)):
            row=0; col=(1 if self.__wires[a]['star'] else 0)+(2 if self.__wires[a]['light'] else 0)
            if 'blue' in self.__wires[a]['color'] and 'red' in self.__wires[a]['color']: row=3
            elif 'red' in self.__wires[a]['color']: row=1
            elif 'blue' in self.__wires[a]['color']: row=2
            elif 'white' in self.__wires[a]['color']: row=0

            temp = self.__table[row][col]
            if (temp=='c')or(temp=='b' and self.batt>=2)or(temp=='s' and int(self._sndigit[-1])%2==0)or(temp=='p' and 'PARALLEL' in self._uniqueports): ans.append(a)
        return ans

    def solve(self):
        '''
        Solve the Complicated Wires module

        Returns:
            tuple (int, ...): The index of wire that should be cut
        '''
        return tuple(self.__calculate())