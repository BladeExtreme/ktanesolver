from ..edgework import edgework

class onlyconnect(edgework):
    def __check(self, t, s):
        if not isinstance(t, str): raise TypeError("teamname must be in str")
        elif not isinstance(s, list) and not isinstance(s, dict): raise TypeError("symbols must be in list or dict")
        if isinstance(s, list):
            if len(s)!=6: raise IndexError("Length of symbols must be 6")
            elif not all([isinstance(a, str) for a in s]): raise TypeError("Element of symbols must be in str")
            return t.upper(), [a.lower() for a in s]
        elif isinstance(s, dict):
            if not all([a in ['tl','tm','tr','bl','bm','br'] for a in s]): raise KeyError("symbol's keys must consist of: 'tl', 'tm', 'tr', 'bl', 'bm', 'br' representing the position of that symbols")
            elif not all([isinstance(a, str) for a in s.values()]): raise TypeError("Value of symbols must be in str")
            return t.upper(), [s[a].lower() for a in ['tl','tm','tr','bl','bm','br']]
    
    def __init__(self, edgework:edgework, teamname:str, symbols:list[str]|dict[str,str]):
        '''
        Initialize a new onlyconnect instance

        Args:
            edgework (edgework): The edgework of the bomb
            teamname (str): The name of the team
            symbols (list|dict): The order of symbols that appears on the module. Symbols can be in list, and must be ordered in reading order (index 0 is top left, index 3 is bottom left). If it's dict, the keys must consist of: 'tl', 'tm', 'tr', 'bl', 'bm', 'br' representing the position of that symbols
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__team, self.__symbols = self.__check(teamname, symbols)
    
    def __calculate1(self):
        criterion = {
            "two reeds": [0,'PS/2'], "lion": [1,"PARALLEL"], "twisted flax": [2,"RJ-45"],
            "horned viper": [3, 'STEREO RCA'], 'water': [4,'SERIAL'], 'eye of horus': [5, 'DVI-D']
        }
        goodcriterion = [0,0,0,0,0,0]
        for a,b in criterion.items():
            temp = 0
            if self.__symbols.index(a)==b[0]: temp+=1
            if self.sn[b[0]] in self.__team if self.sn[b[0]].isalpha() else 'Z' in self.__team if self.sn[b[0]]=='0' else chr(int(self.sn[b[0]])+64) in self.__team: temp+=1
            if b[1] in self._uniqueports: temp+=1
            goodcriterion[self.__symbols.index(a)] = temp
        for a in goodcriterion:
            if goodcriterion.count(a)==1: return self.__symbols[goodcriterion.index(a)]
    
    def showLetters(self):
        temp = {
            'á,ć,é,í,ń,ó,ś,ú,ý,ź': 'Acute',
            'ő,ű': 'Double acute',
            'à,è,ì,ò,ù': 'Grave',
            'â,ĉ,ê,ĝ,ĥ,î,ĵ,ô,ŝ,û,ŵ,ŷ': 'Circumflex',
            'ä,ë,ï,ö,ü,ÿ': 'Umlaut or diaeresis',
            'č,ď,ě,ň,ř,š,ť,ž': 'Hacek or caron',
            'ç,ş': 'Cedilla',
            'ģ,ķ,ļ,ņ,ș,ț': 'Comma',
            'å,ů': 'Ring',
            'ă,ğ,ŭ': 'Breve',
            'ã,ñ,õ': 'Tilde',
            'ā,ē,ī,ū': 'Macron or line',
            'ą,ę,į,ų': 'Ogonek',
            'ė,ż': 'Dot above',
            'đ,ł,ø': 'Slash or stroke',
            'æ,œ': 'Ligature',
            'ð': 'Eth',
            'ı': 'Dotless i',
            'ß': 'Eszett or sharp s',
            'þ': 'Thorn'
        }
        for a,b in temp.items():
            print(f"{b}: {a}")

    def __calculate2(self):
        table = [
            ['çë', 'w'],
            ['äö', 'bcfqwxz'],
            ['ŵŷ', 'kqvxz'],
            ['åæø', ''],
            ['äåö', ''],
            ['äößü', ''],
            ['ćčđšž', 'qwxy'],
            ['âăîșț', ''],
            ['ĉĝĥĵŝŭ', 'qwxy'],
            ['äöõšüž', 'wxy'],
            ['çğıöşü', 'qwx'],
            ['áéíñóúü', ''],
            ['áéíóöőúüű', ''],
            ['ąčėęįšūųž', 'qwx'],
            ['ąćęłńóśźż', 'qvx'],
            ['àçéèíïóòúü', ''],
            ['áæðéíóöþúý', 'cqwz'],
            ['āčēģīķļņšūž', 'qwxy'],
            ['áàâãçéêíóôõúü', 'kwy'],
            ['áčďéěíňóřšťúůýž', ''],
            ['àâäæçéèêëîïôöœùûüÿ', '']
        ]
        ans = []
        while len(self.__letters)!=0:
            for a in range(len(table)):
                temp = []
                for b in self.__letters:
                    if b in table[a][0] if b not in 'abcdefghijklmnopqrstuvwxyz' else b not in table[a][1]: temp.append(b)
                if len(temp)==3:
                    ans.append(tuple(temp))
                    for b in range(0,3):
                        self.__letters.pop(self.__letters.index(temp[b]))
                    break
        return tuple(ans)
    
    def solve(self, letters:list[str]|None=None):
        '''
        Solve the Only Connect module

        Args:
            letters (list (str)): The 9 letters that appears on the module in any order
        Returns:
            str: The symbol that should be pressed first.
            tuple (tuple, tuple): The group of letters that should be pressed. Each tuple represent a single group. Order of tuple does not matter. Use showLetters() to copy all types of letters
        '''
        if letters is not None:
            if not isinstance(letters, list): raise TypeError("letters must be in list")
            elif len(letters)!=9: raise IndexError("Length of letters must be 9")
            elif len(set(letters))!=9: raise ValueError("letters must be unique")
            elif not all([isinstance(a, str) for a in letters]): raise TypeError("Element of letters must be str")
            self.__letters = letters
            return self.__calculate2()
        return self.__calculate1()