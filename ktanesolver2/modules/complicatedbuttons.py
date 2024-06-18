from ..edgework import edgework
from ..tools.colordict import _colorcheck

class complicatedbuttons(edgework):
    __table = {
        0: {'white': 1, 'red': 2, 'blue': 2, tuple(sorted(['red','blue'])): 2},
        1: {'white': 1, 'red': 1, 'blue': 0, tuple(sorted(['red','blue'])): 's'},
        2: {'white': 0, 'red': 'h', 'blue': 's', tuple(sorted(['red','blue'])): 2},
        3: {'white': 'h', 'red': 'h', 'blue': 's', tuple(sorted(['red','blue'])): 0}
    }
    
    def __check(self, b):
        if not isinstance(b, list): raise TypeError("button must be in list")
        elif len(b)!=3: raise IndexError("Length of buttons must be 3")
        elif not all([isinstance(a, dict) for a in b]): raise TypeError("Element of button must be in dict")
        elif not all([all([c in ['color', 'label', 'position'] for c in a]) for a in b]): raise KeyError("Key must only consist of 'color', 'label' and 'position'")
        elif not all([(isinstance(a['color'], list) if isinstance(a['color'], list) and len(a['color'])==2 else isinstance(a['color'], str) if isinstance(a['color'], str) else False) and isinstance(a['label'], str) and isinstance(a['position'], int) for a in b]): raise TypeError("Value of color (must be list if multiple colors) and label must be in str whie value of position must be in int")
        elif not all([all([_colorcheck(x.lower()) in ['white','blue','red'] for x in a['color']]) if isinstance(a['color'], list) else _colorcheck(a['color']) in ['white','blue','red'] for a in b]): raise ValueError("color must be white, red or blue (or its abbreviation, refer to colrodict)")
        elif not all([a['position'] in range(0,3) for a in b]): raise ValueError("Position must be in range of 0-2")
        elif not len(set([a['position'] for a in b]))==3: raise ValueError("Each button's position must be unique")
        ans = []
        for a in b:
            ans.append({'color': [_colorcheck(b.lower()) for b in a['color'] if _colorcheck(b.lower())!='white'] if isinstance(a['color'], list) else _colorcheck(a['color'].lower() if a['color']!='' else 'white'), 'label': a['label'].lower(), 'position': a['position']})
        return sorted(ans, key=lambda x: x['position'])
    
    def __check2(self, c, l):
        if not isinstance(c, list): raise TypeError("color must be in list")
        elif not isinstance(l, list): raise TypeError("label must be in list")
        elif len(c)!=3: raise IndexError("Length of color must be 3")
        elif len(l)!=3: raise IndexError("Length of label must be 3")
        elif not all([isinstance(a, str) if isinstance(a, str) else isinstance(a, list) and len(a)==2 and all([isinstance(x, str) for x in a]) if isinstance(a, list) else False for a in c]): raise TypeError("Element of color must be str or list if multiple colors")
        elif not all([all([_colorcheck(b.lower()) in ['white','blue','red'] for b in a]) if isinstance(a, list) else _colorcheck(a.lower()) in ['white', 'blue', 'red'] for a in c]): raise ValueError("color must be white, red or blue (or its abbreviation, refer to colrodict)")
        elif not all([isinstance(a, str) for a in l]): raise TypeError("Element of label must be in str")
        ans = []
        for a in range(0, 3):
            ans.append({'color': ([_colorcheck(b.lower()) for b in c[a] if _colorcheck(b.lower())!='white'][0] if len([_colorcheck(b.lower()) for b in c[a] if _colorcheck(b.lower())!='white'])==1 else [_colorcheck(b.lower()) for b in c[a] if _colorcheck(b.lower())!='white']) if isinstance(c[a], list) else _colorcheck(c[a].lower()), 'label': l[a].lower(), 'position': a})
        return sorted(ans, key=lambda x: x['position'])
    
    def __init__(self, edgework:edgework, color:list|None=None, label:list[str|list[str]]|None=None, buttons:list[dict]|None=None):
        '''
        Initialize a new complicatedbuttons instance

        Args:
            edgework (edgework): The edgework of the bomb
            color (list (str|list)): The color of each button. If there are multiple, use list. CAUTION: color must be in sync with label and index 0 is treated as the top button
            label (list (str)): The label of each button. CAUTION: label must be in sync with color and index 0 is treated as the top button
            buttons (list (dict)): The information of each button in dict. Keys of dict must consist of only: 'color', 'label' and 'position'. Label must be in str while color can be in list or str (list if multiple colors, else str). Position must be in int and must be in range of 0-2
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        if buttons is not None:
            self.__buttons = self.__check(buttons)
        elif color is not None and label is not None:
            self.__buttons = self.__check2(color, label)
        else:
            raise TypeError("complicatedbuttons.__init__() missing 1 to 2 required positional argument: 'color', 'label' | 'buttons'")
    
    def __calculate(self):
        ans = []
        tableidx = {
            'press': {0:[0,1,2],1:[1,2,0],2:[2,0,1],3:[0,1,2]},
            'hold': {0:[1,0,2],1:[2,1,0],2:[0,2,1],3:[1,2,0]},
            'detonate': {0:[2,0,1], 1:[0,1,2], 2:[1,0,2], 3:[2,0,1]}
        }
        for a in self.__buttons:
            if a['label']=='press' and a['position']==1: ans.append(self.__table[3][tuple(sorted(a['color'])) if isinstance(a['color'], list) else a['color']])
            elif a['label']=='press': ans.append(self.__table[1][tuple(sorted(a['color'])) if isinstance(a['color'], list) else a['color']])
            elif a['position']==1: ans.append(self.__table[2][tuple(sorted(a['color'])) if isinstance(a['color'], list) else a['color']])
            else: ans.append(self.__table[0][tuple(sorted(a['color'])) if isinstance(a['color'], list) else a['color']])
        for a in range(len(ans)):
            if ans[a]==2: ans[a] = 1 if len(set(self.sn))<6 else 0
            elif ans[a]=='s': ans[a] = 1 if 'SERIAL' in self._uniqueports else 0
            elif ans[a]=='h': ans[a] = 1 if self.hold>=2 else 0
        ordertouse = tableidx[self.__buttons[0]['label']][0 if self.batt in range(0,2) else 1 if self.batt in range(2,4) else 2 if self.batt in range(4,6) else 3]
        if all([x==0 for x in ans]): return self.__buttons[ordertouse[1]]
        else:
            new = []
            for a in ordertouse:
                if ans[a]==1:
                    new.append(self.__buttons[a])
            return tuple(new)
    
    def solve(self):
        '''
        Solve the Complicated Buttons module

        Returns:
            tuple (int): The order of press with index of 0.
        '''
        return self.__calculate()