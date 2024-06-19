from ..edgework import edgework

class adventuregame(edgework):
    __enemystats = {
        'demon': {'str': 50, 'dex': 50, 'int': 50},
        'dragon': {'str': 10, 'dex': 11, 'int': 13},
        'eagle': {'str': 4, 'dex': 7, 'int': 3},
        'goblin': {'str': 3, 'dex': 6, 'int': 5},
        'golem': {'str': 9, 'dex': 4, 'int': 7},
        'troll': {'str': 8, 'dex': 5, 'int': 4},
        'lizard': {'str': 4, 'dex': 6, 'int': 3},
        'wizard': {'str': 4, 'dex': 3, 'int': 8}
    }
    __weaponstats = {
		'broadsword': ['str', 0],
		'caber': ['str', 2],
		'nasty knife': ['dex', 0],
		'longbow': ['dex', 2],
		'magic orb': ['int', 0],
		'grimoire': ['int', 2]
    }
    
    def __check(self, e,s,i):
        if not isinstance(e, str): raise TypeError("enemy must be in str")
        elif not isinstance(s, dict): raise TypeError("stats must be in dict")
        elif not isinstance(i, list): raise TypeError("itemweapon must be in list")
        elif not all([a in ['str','dex','int','height','temperature','gravity','pressure'] for a in s]): raise KeyError("Keys must consist of: 'str', 'dex', 'int', 'height', 'temperature', 'gravity', and 'pressure'")
        elif not all([all([isinstance(s['str'], int) and isinstance(s['dex'], int) and isinstance(s['int'],int) and isinstance(s['pressure'], int)]) and isinstance(s['height'], str) and all([isinstance(s['gravity'], float), isinstance(s['temperature'], float)])]): raise TypeError("Values of temperature and gravity must be in float. Values of height must be in str and must contain quotation mark or double quotation mark to reprsent feet and inch")
        elif not all([isinstance(a, str) for a in i]): raise TypeError("Element of itemweapon must be in str")
        elif 'potion' in [a.lower() for a in i]: raise ValueError("Use potion first!")
        return e.lower(), s, [a.lower() for a in i if a.lower() not in self.__weaponstats], [a.lower() for a in i if a.lower() in self.__weaponstats]
    
    def __init__(self, edgework:edgework, enemy:str, stats:dict[int|float|str], itemweapon:list[str]):
        '''
        Initialize a new adventuregame instance

        Args:
            edgework (edgework): The edgework of the bomb
            enemy (str): The type of the enemy
            stats (dict (int|float|str)): The player's statistics. Keys must consist of: 'str', 'dex', 'int', 'height', 'self.__stats['temperature']erature', 'gravity', and 'pressure'. Values of str, dex, int and pressure must be in integer. Values of temperature and gravity must be in float. Values of height must be in str and must contain quotation mark or double quotation mark to reprsent feet and inch
            itemweapon (list (str)): All items and weapons that are available to use
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__enemy, self.__stats, self.__item, self.__weapons = self.__check(enemy ,stats, itemweapon)
    
    def __calculate(self):
        itemrule = {
            'balloon': True if (self.__stats['gravity'] < 9.3) or (self.__stats['pressure'] > 110 and self.__enemy != 'eagle') else False,
		    'self.battery': True if self.batt <= 1 and (self.__enemy != 'golem' and self.__enemy != 'wizard') else False,
		    'bellows': True if ((self.__enemy == 'eagle' or self.__enemy == 'dragon') and self.__stats['pressure'] > 105) or (self.__enemy != 'eagle' and self.__enemy != 'dragon' and self.__stats['pressure'] < 95) else False,
		    'cheat code': False,
		    'crystal ball': True if (self.__stats['int'] > int(self._sndigit[-1])) and (self.__enemy != 'wizard') else False,
		    'feather': True if (self.__stats['dex'] > self.__stats['str'] or self.__stats['dex'] > self.__stats['int']) else False,
		    'hard drive': True if any([[a for b in self.ports for a in b].count(x)>=2 for x in self._uniqueports]) else False,
		    'lamp': True if self.__stats['temperature'] < 12 and self.__enemy != 'lizard' else False,
		    'moonstone': True if len(self._unlitind) >= 2 else False,
		    'potion': True,
		    'small dog': True if (self.__enemy != 'demon' and self.__enemy != 'dragon' and self.__enemy != 'troll') else False,
		    'stepladder': True if int(self.__stats['height'][0:self.__stats['height'].index("'")]) < 4 and (self.__enemy != 'goblin' and self.__enemy != 'lizard') else False,
		    'sunstone': True if len(self._litind) >= 2 else False,
		    'symbol': True if (self.__enemy == 'demon' or self.__enemy == 'golem') or (self.__stats['temperature'] > 31) else False,
		    'ticket': True if ((int(self.__stats['height'][0:self.__stats['height'].index("'")]) >= 4) or (int(self.__stats['height'][0:self.__stats['height'].index("'")]) == 4 and int(self.__stats['height'][self.__stats['height'].index("'")+1:self.__stats['height'].index('"')]) >= 6)) and (self.__stats['gravity'] >= 9.2 and self.__stats['gravity'] <= 10.4) else False,
		    'trophy': True if self.__stats['str'] > int(self._sndigit[0]) or self.__enemy == 'troll' else False
        }
        itemst = [itemrule[a] for a in self.__item]
        enemyst = self.__enemystats[self.__enemy]; usew = []
        for a in self.__weapons:
            usew.append((self.__stats[self.__weaponstats[a][0]]+self.__weaponstats[a][1])-enemyst[self.__weaponstats[a][0]])
        return tuple([tuple([self.__item[a] for a in range(len(itemst)) if itemst[a]]), self.__weapons[usew.index(max(usew))]])

    
    def solve(self):
        '''
        Solve the Adventure Game module

        Returns:
            tuple (tuple, str): The items to use and the weapons to use. Index 0 is the list of items while index 1 is the weapon. NOTE: You must use items first before using a weapon
        '''
        return self.__calculate()