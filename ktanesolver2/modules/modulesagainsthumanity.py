from ..edgework import edgework

class modulesagainsthumanity(edgework):
    def __check(self, w, c):
        if not isinstance(w, dict): raise TypeError("word must be in either list or dict")
        elif not isinstance(c, list): raise TypeError("cardpost must be in list")
        elif len(c)!=2: raise IndexError("Length of cardpos must be 2")
        elif not all([isinstance(a, str) for a in c]): raise TypeError("Element of cardpos must be in str")
        elif not ([a.lower() for a in c]==['black','white'] or [a.lower() for a in c]==['white','black']): raise ValueError("Value of cardpos must either be in 'black' or 'white' but cannot be both")
        elif not all([a in ['black', 'white'] for a in w]): raise KeyError("Key must consist of 'black' and 'white'")
        elif not all([isinstance(a, str) for a in w.values()]): raise TypeError("Value of words must be in str")
        return {'black': w['black'].lower(), 'white': w['white'].lower()}, c

    def __init__(self, edgework:edgework, word:list|dict, cardpos:list):
        '''
        Initialize a new modulesagainsthumanity instance

        Args:
            edgework (edgework): The edgework of the bomb
            word (dict (str)): The full sentence that appears on each card. Key must consist of: 'black' and 'white'
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__card, self.__position = self.__check(word, cardpos)
        self.__currpos = [0, 0]
    
    def __calculate2(self):
        ans = {'black': 0, 'white': 0}
        
        if self.__black and self.__white:
            ans['black'] = 4
            ans['white'] = 3
        elif self.__black: ans['white'] = 2
        elif self.__white: ans['black'] = 1
        else:
            if any([a in ['M','A','H'] for a in self._snletter]): ans['white']=-2; ans['black']=-2
            elif self.__position[0]=='black':
                finalblack = len(self._uniqueports)-1; finalwhite = len(self.ind)-1
                ans['black'] = finalblack-self.__currpos[0]; ans['white'] = finalwhite-self.__currpos[1]
            else:
                finalblack = (self.total_modules)%10-1
                ans['black'] = finalblack-self.__currpos[0]
        return ans

    def __calculate(self):
        ans = {'black': 0, 'white': 0}
        poopblack = self.__card['black'].count('p')>=2 and self.__card['black'].count('o')>=2
        poopwhite = self.__card['white'].count('p')>=2 and self.__card['white'].count('o')>=2
        
        if not poopblack:
            ans['black'] = len(self._unlitind)+len([a for b in self.ports for a in b])-1
        else: ans['black'] = 1
        if not poopwhite:
            ans['white'] = len(self._litind)+self.batt-1
        else: ans['white'] = 1
        return ans

    def solve(self, blackcard:bool|None=None, whitecard:bool|None=None):
        '''
        Solve the Modules Against Humanity module

        Args:
            blackcard (bool|None): State if the module being implied in the black card, exist in the current bomb
            whitecard (bool|None): State if the module being implied in the white card, exist in the current bomb
        Returns:
            dict (int): The number of cards you need to add from your initial position
        '''
        if blackcard is not None and whitecard is not None:
            if not isinstance(blackcard, bool): raise TypeError("blackcard must be in bool")
            elif not isinstance(whitecard, bool): raise TypeError("whitecard must be in bool")
            self.__black = blackcard; self.__white = whitecard
            ans = self.__calculate2()
        elif (blackcard is None) ^ (whitecard is None):
            raise TypeError("blackcard and whitecard must be both None or not")
        else:
            ans = self.__calculate()
            self.__currpos[0]+=ans['black']; self.__currpos[1]+=ans['white']
        return ans