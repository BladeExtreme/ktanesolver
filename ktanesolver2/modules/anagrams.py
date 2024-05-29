from ..edgework import edgework

class anagrams(edgework):
    __bank = {
        tuple(sorted({'s', 'm', 'e', 'r', 'a', 't'})): ['stream', 'master', 'tamers'],
        tuple(sorted({'l', 'o', 'e', 'p', 'd'})): ['looped', 'poodle', 'pooled'],
        tuple(sorted({'l', 'e', 'r', 'a', 'c'})): ['cellar', 'caller', 'recall'],
        tuple(sorted({'s', 'e', 'a', 't', 'd'})): ['seated', 'sedate', 'teased'],
        tuple(sorted({'s', 'u', 'e', 'r', 'c'})): ['rescue', 'secure', 'recuse'],
        tuple(sorted({'s', 'e', 'r', 'a', 'h'})): ['rashes', 'shears', 'shares'],
        tuple(sorted({'b', 'l', 'e', 'y', 'r', 'a'})): ['barely', 'barley', 'bleary'],
        tuple(sorted({'s', 'u', 'e', 'r', 't', 'd'})): ['duster', 'rusted', 'rudest']
    }
    
    def __check(self, l):
        if not isinstance(l, str): raise TypeError("Word has an invalid type")
        elif len(l) != 6: raise IndexError("Length of word must be 6")
        return l
    
    def __init__(self, edgework: edgework, word: str):
        '''
        Initialize a new anagrams instance

        Args:
            edgework (edgework): The edgework of the bomb
            word (str): The word that appears on the module
        '''
        super().__init__(edgework.batt, edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__word = self.__check(word)
    
    def solve(self):
        '''
        Solve the Anagrams module

        Returns:
            Tuple (str, str): The possible words to be submitted
        '''
        ans = [a for a in self.__bank[tuple(sorted(set(self.__word)))] if a != self.__word]
        return tuple(ans)