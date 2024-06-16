from ..edgework import edgework
from ..tools.colordict import _colorcheck

class followtheleader(edgework):
    def __check(self, w):
        if not isinstance(w, list): raise TypeError("wires must be in list")
        elif not all([isinstance(a, dict) for a in w]): raise TypeError("Element of wires must be in str")
        elif not all([all([b in ['color', 'plug0', 'plug1'] for b in a]) for a in w]): raise KeyError("Key must consists only of the following: 'color' and 'coords'")
        elif not all([isinstance(a['color'], str) and isinstance(a['plug0'], int) and isinstance(a['plug1'], int) for a in w]): raise TypeError("Value of color must be in str, and value of plug0 and plug1 must be in int")
        elif not all([a['plug0'] in range(1,13) and a['plug1'] in range(1,13) for a in w]): raise IndexError("Value of plug0 and plug1 must be in range of 1-12")
        return [{'color': _colorcheck(a['color'].lower()), 'plug0': a['plug0'], 'plug1': a['plug1']} for a in w]
    
    def __check2(self, c, p):
        if not isinstance(c, list): raise TypeError("color must be in list")
        elif not isinstance(p, list): raise TypeError("plugs must be in list")
        elif not all([isinstance(a, str) for a in c]): raise TypeError("Element of color must be in str")
        elif not all([isinstance(a, list) for a in p]): raise TypeError("Element of plugs must be in list")
        elif not all([isinstance(a[0], int) and isinstance(a[1], int) for a in p]): raise TypeError("Each element of plugs must be in int")
        elif not all([a[0] in range(1,13) and a[1] in range(1,13) for a in p]): raise TypeError("plugs must be in range of 1-12")
        arr = []
        for a in range(len(c)):
            temp = {'color': _colorcheck(c[a].lower()), 'plug0': p[a][0], 'plug1': p[a][1]}
            arr.append(temp)
        return arr
    
    def __init__(self, edgework:edgework, color:list|None=None, plugs:list|None=None, wires:list|None=None):
        '''
        Initialize a new followtheleader instance

        Args:
            edgework (edgework): The edgework of the bomb
            color (list (str)): The color of the wires that appears on the bomb. CAUTION: color must be in sync with plugs
            plugs (list (list (int)): The origin and destination of the plug number of that wire. Each element of plugs must have 2 numbers, representing the origin plug's number in index 0 and destination's in index 1. CAUTION: plugs must be in sync with color
            wires (list (dict)): The wires in the form of a dict. The wires consists of the following keys only: 'color', 'plug0', 'plug1'. Color must be in str, while plug0 and plug1 must be in int. NOTE: Plug must have an index 1 counting. Meaning, there will be no such thing as plug with number 0
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        if wires is not None:
            self.__wires = self.__check(wires)
        elif color is not None and plugs is not None:
            self.__wires = self.__check2(color, plugs)
        else:
            raise TypeError("wireplacement.__init__() missing 1 to 2 required positional argument: 'color', 'plugs' | 'wires'")
        temp = self.__wires[0]['plug1']
        for a in range(1, len(self.__wires)):
            if self.__wires[a]['plug0']!=temp: raise ValueError("plugs are not connected with each other.")
            temp = self.__wires[a]['plug1']
        if self.__wires[0]['plug0']!=temp: raise ValueError("plugs are not connected with each other.")
    
    def __calculate(self):
        if 'CLR*' not in self._litind:
            if 'RJ-45' in self._uniqueports and len([a for a in self.__wires if a['plug0']==4 and a['plug1']==5])>0: startingwire = [a for a in self.__wires if a['plug0']==4 and a['plug1']==5][0]
            elif len([a for a in self.__wires if a['plug0']==self.batt])>0: startingwire = [a for a in self.__wires if a['plug0']==self.batt][0]
            elif len([a for a in self.__wires if a['plug0']==int(self._sndigit[0])])>0: startingwire = [a for a in self.__wires if a['plug0']==int(self._sndigit[0])][0]
            else:
                startingwire = [a for a in sorted(self.__wires, key=lambda x: x['plug0'])][0]
        else:
            return [a for a in sorted(self.__wires, key=lambda x: x['plug0'], reverse=True)]
        cut = [startingwire]; self.__wires = [self.__wires[a%len(self.__wires)] for a in range(self.__wires.index(startingwire), len(self.__wires)+self.__wires.index(startingwire))]
        row = (int(ord(self._snletter[0]))-65)%13 if self._snletter!=[] else 0; reverse = True if startingwire['color'] in ['red', 'green', 'white'] else False
        for a in range(1, len(self.__wires)):
            if row==0 and self.__wires[a-1]['color'] not in ['yellow','blue','green']: cut.append(self.__wires[a])
            elif row==1 and self.__wires[a-1]['plug1']%2==0: cut.append(self.__wires[a])
            elif row==2 and self.__wires[a-1] in cut: cut.append(self.__wires[a])
            elif row==3 and self.__wires[a-1]['color'] in ['red','blue','black']: cut.append(self.__wires[a])
            elif row==4 and len(set([x['color'] for x in [self.__wires[a-3], self.__wires[a-2], self.__wires[a-1]]]))<3: cut.append(self.__wires[a])
            elif row==5 and ((self.__wires[a]['color']==self.__wires[a-1]['color'])^(self.__wires[a]['color']==self.__wires[a-2]['color'])): cut.append(self.__wires[a])
            elif row==6 and self.__wires[a-1]['color'] in ['yellow','white','green']: cut.append(self.__wires[a])
            elif row==7 and self.__wires[a-1] not in cut: cut.append(self.__wires[a])
            elif row==8 and self.__wires[a-1]['plug0']+2 == self.__wires[a-1]['plug1']: cut.append(self.__wires[a])
            elif row==9 and self.__wires[a-1]['color'] not in ['white','black','red']: cut.append(self.__wires[a])
            elif row==10 and self.__wires[a-1]['color']!=self.__wires[a-2]['color']: cut.append(self.__wires[a])
            elif row==11 and self.__wires[a-1]['plug1']>6: cut.append(self.__wires[a])
            elif row==12 and ((self.__wires[a-1]['color'] in ['black','white']) ^ (self.__wires[a-2]['color'] in ['black','white']) or (self.__wires[a-1]['color'] not in ['black','white'] and self.__wires[a-2]['color'] not in ['black','white'])): cut.append(self.__wires[a])
            row = row+1 if row<15 and not reverse else row-1 if row>0 and reverse else 0 if not reverse else 15
        return cut

    def solve(self):
        '''
        Solve the Follow the Leader module

        Returns:
            tuple (dict): The order of the wire that should be cut, where index 0 are the first. Each wire are represented on a dict with the following key: 'color' the color of the wire, 'plug0' the origin plug of the wire, 'plug1' the end plug of the wire
        '''
        return tuple(self.__calculate())