from ..edgework import edgework
from ..tools.colordict import _colorcheck

class sillyslots(edgework):
    __table = {
        'sassy': {'blue': 'sassy', 'red': 'silly', 'green': 'soggy', 'cherry': 'sally', 'grape': 'simon', 'bomb': 'sausage', 'coin': 'steven'},
        'silly': {'blue': 'sassy', 'green': 'silly', 'red': 'soggy', 'coin': 'sally', 'bomb': 'simon', 'grape': 'sausage', 'cherry': 'steven'},
        'soggy': {'green': 'sassy', 'blue': 'silly', 'red': 'soggy', 'coin': 'sally', 'cherry': 'simon', 'bomb': 'sausage', 'grape': 'steven'},
        'sally': {'red': 'sassy', 'blue': 'silly', 'green': 'soggy', 'grape': 'sally', 'cherry': 'simon', 'bomb': 'sausage', 'coin': 'steven'},
        'simon': {'red': 'sassy', 'green': 'silly', 'blue': 'soggy', 'bomb': 'sally', 'grape': 'simon', 'cherry': 'sausage', 'coin': 'steven'},
        'sausage': {'red': 'sassy', 'blue': 'silly', 'green': 'soggy', 'grape': 'sally', 'bomb': 'simon', 'coin': 'sausage', 'cherry': 'steven'},
        'steven': {'green': 'sassy', 'red': 'silly', 'blue': 'soggy', 'cherry': 'sally', 'bomb': 'simon', 'coin': 'sausage', 'grape': 'steven'}
    }

    def __check(self, b):
        if not isinstance(b, list): raise TypeError("slots must be in list")
        elif len(b)!=3: raise IndexError("Length of slots must be 3")
        elif not all([isinstance(a, dict) for a in b]): raise TypeError("Element of slots must be in dict")
        elif not all([all([c in ['color', 'symbol', 'slot'] for c in a]) for a in b]): raise KeyError("Key must only consist of 'color', 'symbol' and 'slot'")
        elif not all([isinstance(a['color'], str) and isinstance(a['symbol'], str) for a in b]): raise TypeError("Value of color and symbol must be in str whie value of slot must be in int")
        elif not all([_colorcheck(a['color'].lower()) in ['green','blue','red'] for a in b]): raise ValueError("color must be green, red or blue (or its abbreviation, refer to colrodict)")
        elif not all([a['symbol'].lower() in ['cherry', 'grape','bomb','coin'] for a in b]): raise ValueError("symbol must be 'cherry','grape','coin', or 'bomb'")
        elif not all([a['slot'] in range(0,3) for a in b]): raise ValueError("Slot must be in range of 0-2")
        elif not len(set([a['slot'] for a in b]))==3: raise ValueError("Each slots' position must be unique")
        ans = []
        for a in b:
            ans.append({'color':  _colorcheck(a['color'].lower()), 'symbol': a['symbol'].lower(), 'slot': a['slot']})
        return sorted(ans, key=lambda x: x['slot'])
    
    def __check2(self, c, s):
        if not isinstance(c, list): raise TypeError("color must be in list")
        elif not isinstance(s, list): raise TypeError("symbol must be in list")
        elif len(c)!=3: raise IndexError("Length of color must be 3")
        elif len(s)!=3: raise IndexError("Length of symbol must be 3")
        elif not all([isinstance(a, str) for a in c]): raise TypeError("Element of color must be str")
        elif not all([_colorcheck(a.lower()) in ['green', 'blue', 'red'] for a in c]): raise ValueError("color must be green, red or blue (or its abbreviation, refer to colrodict)")
        elif not all([isinstance(a, str) for a in s]): raise TypeError("Element of symbol must be in str")
        elif not all([a.lower() in ['cherry','grape','bomb','coin'] for a in s]): raise ValueError("symbol must be 'cherry','grape','coin', or 'bomb'")
        ans = []
        for a in range(0, 3):
            ans.append({'color': _colorcheck(c[a].lower()), 'symbol': s[a].lower(), 'slot': a})
        return sorted(ans, key=lambda x: x['slot'])

    def __check3(self, k):
        if not isinstance(k, str): raise TypeError("keyword must be in str")
        elif k.lower() not in ['sassy','silly','soggy','sally','simon','sausage','steven']: raise ValueError("This is not a valid keyword")
        return k.lower()
    
    def __init__(self, edgework:edgework, keyword:str, colors:list[list[str]]|None=None, symbols:list[list[str]]|None=None, slots:list[dict]|None=None):
        '''
        Initialize a new sillyslots instance

        Args:
            edgework (edgework): The edgework of the bomb
            keyword (str): The keyword that apppears on the top of the module
            color (list (str)): The color of each button. CAUTION: color must be in sync with label and index 0 is the most left slot
            symbol (list (str)): The symbol of each button. CAUTION: symbol must be in sync with color and index 0 is the most left slot
            slots (list (dict)): The information of each button in dict. Keys of dict must consist of only: 'color', 'symbol' and 'slot'. Value of Color and symbol must be in str while value of slot must be in int and must be in range of 0-2
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__keyword = self.__check3(keyword)
        if slots is not None:
            self.__slots = self.__check(slots); self.__oldslots = []; self.__temp = []
        elif colors is not None and symbols is not None:
            self.__slots = self.__check2(colors, symbols); self.__oldslots = []; self.__temp = []
        else:
            raise TypeError("sillyslots.__init__() missing 1 to 2 required positional argument: 'colors', 'symbols' | 'slots'")
    
    def __calculate(self):
        ans = []
        for a in self.__slots:
            ans.append(" ".join([self.__table[self.__keyword][a['color']], self.__table[self.__keyword][a['symbol']]]))
        self.__oldslots.append(ans); self.__temp.append([tuple([a['color'], a['symbol']]) for a in self.__slots])
        temp = [self.__table[self.__keyword][b[0]]+" "+self.__table[self.__keyword][b[1]] for b in self.__temp[self.__oldslots.index(ans)-1]] if len(self.__oldslots)>1 else '0'

        if ans.count('silly sausage')==1: return 'pull'
        if ans.count('sassy sally')==1 and ('soggy' in [self.__table[self.__keyword][b[0]]+" "+self.__table[self.__keyword][b[1]] for b in self.__temp[self.__oldslots.index(ans)-2]][ans.index('sassy sally')] if len(self.__oldslots)>2 and 'sassy sally' in ans else True): return 'pull'
        if ans.count('soggy stevens')>=2: return 'pull'
        if len([a for a in ans if 'simons' in a])==3 and len([a for a in ans if 'sassy' in a])>0: return 'pull'
        if any([(ans[a]=='sassy' and ans[a+1]=='soggy') or (ans[a]=='soggy' and ans[a+1]=='sassy') for a in range(0,2)]) and not all([ans[a]==['simon','sassy','soggy'][a] or ans[a]==['soggy','sassy','simon'][a] for a in range(0,3)]): return 'pull'
        if len([a for a in ans if 'silly' in a])==2 and not any(['steven' in a for a in ans if a=='silly']): return 'pull'
        if len([a for a in ans if 'soggy' in a])==1 and not any(['sausage' in a for a in temp]): return 'pull'
        if len(set(ans))==1 and not all([[self.__table[self.__keyword][b[0]]+" "+self.__table[self.__keyword][b[1]].count("soggy sausage")>1 for b in self.__temp[self.__oldslots.index(ans)-a]] for a in range(1, len(self.__oldslots))]): return 'pull'
        if len(set([a[0:5] for a in ans]))==1 and not any(['sally' in a for a in ans]) or (temp.count('silly steven')): return 'pull'
        if ans.count('silly simon')>0 and not any([[self.__table[self.__keyword][b[0]]+" "+self.__table[self.__keyword][b[1]].count("sassy sausage")>1 for b in self.__temp[self.__oldslots.index(ans)-a]] for a in range(1, len(self.__oldslots))]): return 'pull'
        return 'keep'
    
    def solve(self, keyword:str|None=None, colors:list[list[str]]|None=None, symbols:list[list[str]]|None=None, slots:list[dict]|None=None):
        '''
        Solve the Silly Slots module
        
        Args:
            keyword (str): The keyword that apppears on the top of the module
            color (list (str)): The color of each button. CAUTION: color must be in sync with label and index 0 is the most left slot
            symbol (list (str)): The symbol of each button. CAUTION: symbol must be in sync with color and index 0 is the most left slot
            slots (list (dict)): The information of each button in dict. Keys of dict must consist of only: 'color', 'symbol' and 'slot'. Value of Color and symbol must be in str while value of slot must be in int and must be in range of 0-2
        Returns:
            str: Either keep or pull the slots
        '''
        if keyword is not None: self.__keyword = self.__check3(keyword)
        if slots is not None:
            self.__slots = self.__check(slots)
        elif colors is not None and symbols is not None:
            self.__slots = self.__check2(colors, symbols)
        elif keyword is not None and slots is None and colors is None:
            raise TypeError("sillyslots.solve() missing 1 to 2 required positional argument: 'colors', 'symbols' | 'slots'")
        return self.__calculate()