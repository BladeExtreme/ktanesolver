from ..edgework import edgework

class seashells(edgework):
    __table = {
        'SHE SELLS': {'SEA SHELLS': 'BDABDAB', 'SHE SHELLS': 'ACEEAC', 'SEA SELLS': 'EACEACE', 'SHE SELLS': 'DAABDAB'},
        'SHE SHELLS': {'SEA SHELLS': 'BEEBBE', 'SHE SHELLS': 'CDCCDB', 'SEA SELLS': 'EAEAEA', 'SHE SELLS': 'BEEDA'},
        'SEA SHELLS': {'SEA SHELLS': 'ABABA', 'SHE SHELLS': 'EAAEEA', 'SEA SELLS': 'DBEAC', 'SHE SELLS': 'ABDBAA'},
        'SEA SELLS': {'SEA SHELLS': 'ACACEAC', 'SHE SHELLS': 'DBAEC', 'SEA SELLS': 'EBDADAB', 'SHE SELLS': 'CECEC'}
    }
    __definition = {
        'ON THE SEA SHORE': {'A': 'shoe', 'B': 'shih tzu', 'C': 'she', 'D': 'sit', 'E': 'sushi'},
        'ON THE SHE SORE': {'A': 'can', 'B': 'toucan', 'C': 'tutu', 'D': '2', 'E': 'cancan'},
        'ON THE SHE SURE': {'A': 'witch', 'B': 'switch', 'C': 'itch', 'D': 'twitch', 'E': 'stitch'},
        'ON THE SEESAW': {'A': 'burglar alarm', 'B': 'Bulgaria', 'C': 'armour', 'D': 'burger', 'E': 'llama'}
    }

    def __check(self, w):
        if not isinstance(w, str): raise TypeError("words must be in str")
        return w.upper()
    
    def __init__(self, edgework:edgework, words:str):
        '''
        Initialize a new seashells instance

        Args:
            edgework (edgework): The edgework of the bomb
            words (str): The full sentence that appears on the module
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__words = self.__check(words)
    
    def __calculate(self):
        row = " ".join(self.__words.split()[0:2]); col = " ".join(self.__words.split()[2:4]); buttons = " ".join(self.__words.split()[4:])
        ans = []
        for a in self.__table[row][col]:
            ans.append(self.__definition[buttons][a])
        return tuple(ans)
    
    def solve(self, words:str|None=None):
        '''
        Solve the Sea Shells module

        Args:
            words (str): The full sentence that appears on the module
        Returns:
            tuple (str): The order of buttons to press with these labels
        '''
        if words is not None:
            self.__words = self.__check(words)
        return self.__calculate()