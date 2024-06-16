from ..edgework import edgework
from ..tools.colordict import _colorcheck

class wireplacement(edgework):
    __table = {
        "yellow": {'black': ['d2', 'd3', 'd1'], 'blue': ['d1', 'c3', 'a1'], 'red': ['d2', 'a2', 'b2'], 'white': ['a2', 'a4', 'b4'], 'yellow': ['d1', 'a3', 'a4']},
        "blue": {'black': ['a2','c3'], 'blue': ['c4','c2'], 'red': ['a1','c1'], 'white': ['c4','d3'], 'yellow': ['d4','b1']},
        "white": {'black': ['d3','b2'], 'blue': ['d2','c1'], 'red': ['d4','b4'], 'white': ['b3','a1'], 'yellow': ['b2','c1']},
        "red": {'black': ['a1','c4'], 'blue': ['c3','d3'], 'red': ['c4','b1'], 'white': ['b2','c1'], 'yellow': ['b3','c2']},
        "black": {'black': ['b1'], 'blue': ['d4'], 'red': ['a4'], 'white': ['d2'], 'yellow': ['b4']}
    }
    
    def __check(self, w):
        if not isinstance(w, list): raise TypeError("wires must be in list")
        elif not all([isinstance(a, dict) for a in w]): raise TypeError("Element of wires must be in str")
        elif not all([all([b in ['color', 'coords'] for b in a]) for a in w]): raise KeyError("Key must consists only of the following: 'color' and 'coords'")
        elif not all([isinstance(a['color'], str) and isinstance(a['coords'], list) for a in w]): raise TypeError("Value of color must be in str, and value of coords must be in list")
        elif not all([all([len(b)==2 for b in a['coords']]) for a in w]): raise IndexError("Length of coords key must be 2")
        elif not all([all([isinstance(b, str) for b in a['coords']]) for a in w]): raise TypeError("Value for coords' elements must be in str")
        elif not all([all([b[0] in ['a','b','c','d'] and int(b[-1]) in range(1,5) for b in a['coords']]) for a in w]): raise TypeError("coords must be in range of a-d and 1-4")
        return [{'color': _colorcheck(a['color'].lower()), 'coords': list(map(lambda x: x.lower(), a['coords']))} for a in w]

    def __check2(self, c, o):
        if not isinstance(c, list): raise TypeError("color must be in list")
        elif not isinstance(o, list): raise TypeError("coords must be in list")
        elif not all([isinstance(a, str) for a in c]): raise TypeError("Element of color must be in str")
        elif not all([isinstance(a, list) for a in o]): raise TypeError("Element of coords must be in str")
        elif not all([isinstance(a, str) for b in o for a in b]): raise TypeError("Each element of coords must be in str")
        elif not all([int(a[-1]) in range(1,5) and a[0].lower() in ['a','b','c','d'] for b in o for a in b]): raise TypeError("coords must be in range of a-d and 1-4")
        arr = []
        for a in range(len(c)):
            temp = {'color': _colorcheck(c[a].lower()), 'coords': [x.lower() for x in o[a]]}
            arr.append(temp)
        return arr

    def __init__(self, edgework:edgework, color:list|None=None, coords:list|None=None, wires:list|None=None):
        '''
        Initialize a new wireplacement instance

        Args:
            edgework (edgework): The edgework of the bomb
            color (list (str)): The color of the wires that appears on the module. CAUTION: color must be in sync with coords
            coords (list (list (str))): The coordinates of each wire in the module. CAUTION: coords must be in sync with color
            wires (list (dict)): The wires in the form of a dict. The wires consists of the following keys only: 'color', 'coords'. Color must be in str, while coords must be in list (str)
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        if wires is not None:
            self.__wires = self.__check(wires)
        elif color is not None and coords is not None:
            self.__wires = self.__check2(color, coords)
        else:
            raise TypeError("wireplacement.__init__() missing 1 to 2 required positional argument: 'color', 'coords' | 'wires'")
    
    def __calculate(self):
        cut = []; c3wire = [a['color'] for a in self.__wires if 'c3' in a['coords']][0]
        for a in self.__wires:
            if any([b in self.__table[a['color']][c3wire] for b in a['coords']]):
                cut.append(tuple([a['color'], tuple(a['coords'])]))
        return cut
    
    def solve(self):
        '''
        Solve the Wire Placement module

        Returns:
            tuple (tuple (str), tuple (str)): The wires that needed to be cut in any particular order. Each element's index 0 are the color of the wire, while index 1 are the coordinates that is connected to and from
        '''
        return self.__calculate()