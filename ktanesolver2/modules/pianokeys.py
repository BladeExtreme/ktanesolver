from ..edgework import edgework

class pianokeys(edgework):
    __symboltable = {
        '𝄬': 'flat',
        '𝄴': 'common time', '𝄰': 'sharp',
        '𝄯': 'natural', '𝄐': 'fermata',
        '𝄵': 'cut time', '𝆗': 'turn',
        '𝄡': 'clef', '~': 'mordent'
    }
    
    def __check(self, s):
        if not isinstance(s, list): raise TypeError("symbollist must be in list")
        elif not all([isinstance(a, str) for a in s]): raise TypeError("Element of symbollist must be in str")
        elif len(s)!=3: raise IndexError("Length of symbollist must be 3")
        elif not all([a in self.__symboltable.values() or a in self.__symboltable.keys() for a in s]): raise ValueError("Element of symbollist cannot be found on symboltable. Use showNames() to show list of symbols/names")
        temp = [a for a in self.__symboltable.values()]
        return [self.__symboltable[a] if a not in temp else a for a in s]
    
    def __init__(self, edgework:edgework, symbollist:list):
        '''
        Initialize a new pianokeys instance

        Args:
            edgework (edgework): The edgework of the bomb
            symbollist (list (str)): The symbols that appears on the module. IMPORTANT: Since 'mordent' cannot be displayed correctly on some pc, please use '~' or just use 'mordent'
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__symbols = self.__check(symbollist)
    
    def __calculate(self):
        if 'flat' in self.__symbols and int(self._sndigit[-1])%2 == 0: return ['A#','A#','A#','A#','F#','G#','A#','G#','A#']
        elif ('common time' in self.__symbols or 'sharp' in self.__symbols) and self.hold >= 2: return ['D#','D#','D','D','D#','D#','D','D#','D#','D','D','D#']
        elif ('natural' in self.__symbols and 'fermata' in self.__symbols): return ['E','F#','F#','F#','F#','E','E','E']
        elif ('cut time' in self.__symbols or 'turn' in self.__symbols) and any('STEREO RCA' in a for a in self._uniqueports): return ['A#','A','A#','F','D#','A#','A','A#','F','D#']
        elif ('clef' in self.__symbols) and any('SND*'in a for a in self._litind): return ['E','E','E','C','E','G','G']
        elif ('mordent' in self.__symbols or 'fermata' in self.__symbols or 'common time' in self.__symbols) and self.batt >= 3: return ['C#','D','E','F','C#','D','E','F','A#','A']
        elif ('flat' in self.__symbols and 'sharp' in self.__symbols): return ['G','G','C','G','G','C','G','C']
        elif ('cut time' in self.__symbols or 'mordent' in self.__symbols) and any(numb in self._sndigit for numb in ['3', '7', '8']): return ['A','E','F','G','F','E','D','D','F','A']
        elif ('flat' in self.__symbols or 'turn' in self.__symbols or 'clef' in self.__symbols): return ['G','G','G','D#','A#','G','D#','A#','G']
        else: return ['B','D','A','G','A','B','D','A']
    
    def solve(self):
        '''
        Solve the Piano Keys module

        Returns:
            tuple (str): Notes to be pressed in that order. NOTE: There will be no flat keys, all of them have been adjusted to have sharps only
        '''
        return tuple(self.__calculate())