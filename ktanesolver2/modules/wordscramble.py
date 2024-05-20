from ..edgework import edgework

class wordscramble(edgework):
    __list = ['banana', 'attack', 'damage', 'napalm', 'ottawa', 'kaboom', 'blasts',
              'charge', 'archer', 'casing', 'cannon', 'keypad', 'disarm', 'flames',
              'kevlar', 'weapon', 'sapper', 'mortar', 'button', 'robots', 'bursts',
              'device', 'rocket', 'defuse', 'widget', 'module', 'letter', 'semtex',
              'person', 'wiring']
    
    def __check(self, w):
        if not isinstance(w, list): raise TypeError("Scrambled has an invalid type")
        elif len(w) != 6: raise IndexError("The length of the scrambled list must be 6")
        elif any([not isinstance(a, str) for a in w]): raise TypeError("List's value has an invalid type")
        else: return sorted(w)
    
    def __init__(self, edgework: edgework, scrambled: list):
        '''
        Intialize a new wordscramble instance

        Args:
            edgework (edgework): The edgework of the bomb
            scrambled (list [str]): The scrambled letter that appears on the bomb
        '''        
        super().__init__(edgework.batt, edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.strikes)
        self.__letter = self.__check([a.lower() for a in scrambled])
    
    def __calculate(self, w):
        for a in self.__list:
            if sorted([b for b in a]) == w: return a
        return -1

    def solve(self):
        '''
        Solve the Word Scramble module

        Returns:
            str: The unjumbled word
        Raises:
            ValueError: Unable to find the stored word
        '''
        a = self.__calculate(self.__letter)
        if a == -1: raise ValueError("Cannot find stored words with these set of letters, are you sure you got the letters correct?")
        else: return a
