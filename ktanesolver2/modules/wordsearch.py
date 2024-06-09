from ..edgework import edgework

class wordsearch(edgework):
    __wordlist = [
        ['HOTEL','DONE'], ['SEARCH','QUEBEC'], ['ADD','CHECK'], ['SIERRA','FIND'], ['FINISH','EAST'],
        ['PORT','COLOR'], ['BOOM', 'SUBMIT'], ['LINE', 'BLUE'], ['KABOOM','ECHO'], ['PANIC', 'FALSE'],['MANUAL','ALARM'],['DECOY','CALL'],
        ['SEE','TWENTY'],['INDIA','NORTH'],['NUMBER','LOOK'],['ZULU','GREEN'],['VICTOR','XRAY'],['DELTA','YES'],['HELP','LOCATE'],
        ['ROMEO','BEEP'],['TRUE','EXPERT'],['MIKE','EDGE'],['FOUND','RED'],['BOMBS','WORD'],['WORK','UNIQUE'],['TEST','JINX'],
        ['GOLF','LETTER'],['TALK','SIX'],['BRAVO','SERIAL'],['SEVEN','TIMER'],['MODULE','SPELL'],['LIST','TANGO'],['YANKEE','SOLVE'],
        ['CHART','OSCAR'],['MATH','NEXT'],['READ','LISTEN'],['LIMA','FOUR'],['COUNT','OFFICE']
    ]
    __letpos = [
                "...V","..VU","..US","..SZ","..Z.",
        "...P",".VPQ","VUQN","USNX","SZXF","Z.FY","..Y.",
        ".P.T","PQTI","QNIM","NXME","XFED","FYDA","Y.A.",
        ".T.K","TIKB","IMBW","MEWH","EDHJ","DAJO","A.O.",
        ".K..","KB..","BWRL","WHLC","HJCG","JOG.","O...",
                ".R..","RL..","LC..","CG..","G..."
    ]
    
    def __check(self, l):
        if not isinstance(l, dict) and not isinstance(l, list): raise TypeError("cornerletters must be in dict or list")
        if isinstance(l, dict):
            if len(l) != 4: raise IndexError("Length of cornerletters must be 4")
            elif not all([isinstance(a, str) for a in l.keys()]): raise TypeError("Keys of cornerletters must be in str")
            elif not all([a in ['tl','tr','bl','br'] for a in l]): raise KeyError("Keys must be: tl, tr, bl, br only")
            elif not all([isinstance(a, str) for a in l.values()]): raise TypeError("Values of cornerletters must be in str")
            elif not all([len(a)==1 for a in l.values()]): raise TypeError("Length of cornerletters' values must be 1")
            return [l['tl'].upper(), l['tr'].upper(), l['bl'].upper(), l['br'].upper()]
        if isinstance(l, list):
            if any([True if not isinstance(a, str) else False for a in l]): raise TypeError("Elements of cornerletters must be in str")
            elif len(l) != 4: raise IndexError("Length of cornerletters must be 4")
            elif any([True if len(a)!= 1 else False for a in l]): raise ValueError("Length of cornerletters elements must be 1")
            return [a.upper() for a in l]
    
    def __init__(self, edgework:edgework, cornerletters:list|dict):
        '''
        Initialize a new wordsearch instance

        Args:
            edgework (edgework): The edgework of the bomb
            cornerletters (list [str,str,str,str]): The letters that appears on the corners of the module. List of cornerletters are in reading order, meaning index 0 represents top left and index 2 represents bottom left
            cornerletters (dict {'tl': str, 'tr': str, ...}): The letters that appears on the corners of the module in dictionary.
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__letters = self.__check(cornerletters)
    
    def __calculate(self):
        parity = int(self._sndigit[-1])%2
        ans = []
        for n,letter in zip(range(len(self.__letters)), self.__letters):
            ans.append(self.__wordlist[[self.__letpos.index(a) for a in self.__letpos if a[n]==letter][0]][parity])
        return ans

    def solve(self):
        '''
        Solve the Word Search module

        Returns:
            Tuple (str, ...): The valid words to be used in word search

        '''
        ans = set(self.__calculate())
        return tuple(ans)