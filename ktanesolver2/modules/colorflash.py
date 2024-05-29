from ..edgework import edgework
from ..colordict import _colorcheck

class colorflash(edgework):
    def __check(self, w, c):
        if not isinstance(w, list): raise TypeError("Word must be a list")
        elif not isinstance(c, list): raise TypeError("Color must be a list")
        elif any([True if not isinstance(a, str) else False for a in w]): raise TypeError("Content of word must be str")
        elif any([True if not isinstance(a, str) else False for a in c]): raise TypeError("Content of color must be str")
        return _colorcheck([a.lower() for a in w]), _colorcheck([a.lower() for a in c])
    
    def __init__(self, edgework: edgework, word: list, color: str):
        '''
        Initialize a new colorflash instance

        Args:
            edgework (edgework): The edgework of the bomb
            word (list [str]): The words that appears on the module
            color (list [str]): The color of the word that appears on the module
        '''
        super().__init__(edgework.batt, edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__word, self.__color = self.__check(word, color)
        self.__sequence = [[a,b] for a,b in zip(self.__word, self.__color)]
    
    def __calculate(self):
        i = self.__color[-1]
        if(i=='red'):
            if self.__word.count('green') >= 3: return [a for a in range(len(self.__sequence)) if 'green' in self.__sequence[a]][2], 'yes'
            elif self.__color.count('blue') >= 1: return self.__word.index('magenta'), 'no'
            else: return [a for a in range(len(self.__sequence)) if 'white' in self.__sequence[a]][-1], 'yes'
        elif(i=='yellow'):
            if self.__sequence.get(['blue', 'green']): return self.__color.index('green'), 'yes'
            elif ['white', 'white'] in self.__sequence or ['white', 'red'] in self.__sequence: return [a for a in self.__sequence if self._sequence[0] != self.__sequence[-1]][1], 'yes'
            else: return len([a for a in self.__sequence if 'magenta' in self.__sequence])-1, 'no'
        elif(i=='green'):
            if [True if self.__sequence[a][0] == self.__sequence[a+1][0] and self.__sequence[a][1] != self.__sequence[a+1][1] else False for a in range(len(self.__sequence)-1)]: return 4, 'no'
            elif self.__word.count('magenta') >= 3: return [a for a in range(len(self.__sequence)) if 'yellow' in self.__sequence[a]][0], 'no'
            else: return [a for a in range(len(self.__sequence)) if self.__sequence[a][0] == self.__sequence[a][1]][0], 'yes'
        elif(i=='blue'):
            if len([a for a in self.__sequence if a[0] != a[1]]) >= 3: return [a for a in range(len(self.__sequence)) if self.__sequence[a][0] != self.__sequence[a][1]][0], 'yes'
            elif ['red', 'yellow'] in self.__sequence or ['yellow', 'white'] in self.__sequence: return self.__sequence.index(['white', 'red']), 'no'
            else: return [a for a in range(len(self.__sequence)) if 'green' in self.__sequence[a]][-1], 'yes'
        elif(i=='magenta'):
            if [True if self.__sequence[a][0] == self.__sequence[a+1][0] and self.__sequence[a][1] != self.__sequence[a+1][1] else False for a in range(len(self.__sequence)-1)]: return 2, 'yes'
            elif self.__word.count('yellow') > self.__color.count('blue'): return [a for a in range(len(self.__word)) if 'yellow' in self.__word[a]][-1], 'no'
            else: return [a for a in range(len(self.__sequence)) if self.__sequence[a][1] == self.__color[6]][0], 'no'
        elif(i=='white'):
            if self.__color[2] == self.__word[3] or self.__color[2] == self.__word[4]: return [a for a in range(len(self.__sequence)) if 'blue' in self.__sequence[a]][0], 'no'
            elif ['yellow', 'red'] in self.__sequence: return [a for a in range(len(self.__color)) if self.__color[a] == 'blue'][-1], 'yes'
            else: 'any', 'no'

    def solve(self):
        '''
        Solve the Color Flash module

        Returns:
            Tuple (int|str, str): Returns the submit index of word/color list, and the correct button to press. Index starts at 0.
        '''
        idx, press = self.__calculate()
        return tuple([idx, press])