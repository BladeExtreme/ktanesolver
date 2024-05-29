from ..edgework import edgework

class cryptography(edgework):
    __lettcount = [
      [1, 6, 4, 3], [1, 9, 9, 8], [2, 3, 3, 3], [2, 3, 3, 4], [2, 4, 4, 4], [2, 4, 3, 3], [2, 4, 3, 6], [2, 6, 2, 3], [2, 6, 5, 4], [2, 7, 3, 3], [3, 2, 3, 1],
       [3, 4, 3, 5], [3, 4, 3, 7], [3, 4, 4, 3], [3, 4, 5, 3], [3, 4, 6, 3], [3, 5, 2, 2], [3, 5, 4, 2], [3, 7, 2, 7], [3, 8, 4, 3], [4, 3, 4, 3], [4, 3, 5, 2],
        [4, 3, 5, 4], [4, 4, 2, 10], [4, 4, 3, 4], [4, 5, 4, 4], [4, 7, 5, 4], [5, 2, 2, 5], [5, 2, 5, 5], [6, 3, 13, 3], [6, 4, 7, 3], [7, 3, 2, 4], [7, 3, 3, 4],
         [7, 4, 2, 3], [7, 5, 7, 3], [8, 4, 3, 4], [9, 6, 3, 2]
    ]
    __sentences = [
      "AFROSTYIMEWNHDBC", "ASQUEZINGWRCHPLTOVD", "ITWASLHEMO", "ITWASHEVRYNGLKD", "NOWIDTHABLESRFGMUPY", "TOEDGHISWAYLNCRPFUMK", "HEICDSOFNTGAY", "OFCURSEHDI", "NOWARMTHCULDIYE", "HECARIDSOWNLTMPUYB", "BUTHEWASIGFDNROC", "THEFIRMWASKNOCGDLY",
      "BUTWHADISCROGE", "ANDWHETYSIMCOGULRP", "ANDTHEWOULGIRSYBVKM", "THECOLDWINMFRZSAUPVKG", "HOWCULDITBERS", "ANDITHWOEGRCSM", "THEMNIOFARLYSUBGCKPD", "THEAVISRNDOWLCUBFGMYP", "MADEHISYRTNLPBUOKWGVC", "HARDNSPFLITOMWCEVUKG", "EVNTHBLIDMSOGAPRKW",
      "THISMUBEDNCLYROGWFA", "WHENILYOUCMTS", "THEYOFNCAMDWSLRGVI", "FOULWEATHRDINKVM", "THERISNODUBAMLYW", "THERISODYAFWBVUCGNML", "SECRTANDLFOIY", "NOBDYEVRSTPHIMAWGLKCU", "SCROGEANDHWPTFIKMY", "SCROGEWAHILXUTDMNYF", "SCROGEKNWHAD", "SCROGENVPAITDULMY", "EXTRNALHDCOIFUSG", "SOMETIPLNWHBUCADRGY"
    ]
    
    def __check(self, e, b):
        if not isinstance(e, str): raise TypeError("Encryptred sentence must be in str")
        elif len([a for a in ['\\', '/', '?', '.', '!', ',', '\'', '\"'] if a in e])>0: raise ValueError("The encrypted sentence cannot have symbols")
        elif not isinstance(b, list): raise TypeError("Buttons must be in list")
        elif len(b) != 5: raise IndexError("Length of button must be 5")
        elif not all([isinstance(a, str) for a in b]): raise TypeError("Content of buttons must be in str")
        elif not all([len(a)==1 for a in b]): raise IndexError("Length each content buttons must be 1")
        return e,b
    
    def __init__(self, edgework:edgework, encrypted: str, buttons: list):
        '''
        Initialize a new cryptography instance

        Args:
            edgework (edgework): The edgework of the bomb
            encrypted (str): The encrypted sentence in the module
            buttons (list [str, str, str, str, str]): The letter buttons that appears on the module
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__encrypted, self.__buttons = self.__check(encrypted.lower(), [a.lower() for a in buttons])
    
    def __calculate(self):
        length = []
        words = []
        for a in range(len(self.__encrypted)):
            if self.__encrypted[a] != ' ': words.append(self.__encrypted[a])
            else:
                length.append(len(words))
                words = []
            if len(length) == 4: break
        return self.__sentences[self.__lettcount.index(length)]

    def solve(self):
        '''
        Solve the Cryptography module

        Returns:
            Tuple (str, str, str, str, str): The correct order to press the letter buttons
        '''
        ans = self.__calculate()
        return tuple([a.lower() for a in ans if a.lower() in self.__buttons])