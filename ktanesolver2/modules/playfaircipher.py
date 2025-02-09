from ..edgework import edgework
from ..tools.colordict import _colorcheck

class playfaircipher(edgework):
    __daysoftheweek = {
        'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5, 'sat': 6, 'sun': 7
    }
    
    def __check(self, c, e, d):
        if not isinstance(c, str): raise TypeError("color must be in str")
        elif not isinstance(e, str): raise TypeError("encrypted must be in str")
        elif not isinstance(d, str): raise TypeError("day must be in str")
        elif d.lower() not in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','mon','tue','wed','thu','fri','sat','sun']: raise ValueError("day must be the name of any day or the first three letters of it")
        elif len(e)!=6: raise IndexError("Length of encrypted must be 6")
        match _colorcheck(c.lower()):
            case 'magenta' | 'm': c = 0
            case 'blue' | 'b': c = 1
            case 'orange' | 'o': c = 2
            case 'yellow' | 'y': c = 3
        return c, e.upper(), self.__daysoftheweek[d[0:3].lower()]

    def __init__(self, edgework:edgework, color:str, encrypted:str, day:str):
        '''
        Initialize a new playfaircipher instance

        Args:
            edgework (edgework): The edgework of the bomb
            color (str): The color of the screen
            encrypted (str): The encrpyted text that appears on the screen
            day (str): The day of the bomb generated
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__color, self.__encrypted, self.__day = self.__check(color, encrypted, day)
    
    def __calculate(self):
        key1=""; key2=""; keyX=""
        if self.__day%2==1 and "BOB*" in self._litind and self.__day!=7: self.__day+=1
        
        match self.__day:
            case 1: key1="PLAY"
            case 2: key1="HIDDEN"
            case 3: key1="SECRET"
            case 4: key1="CIPHER"
            case 5: key1="FAIL"
            case 6: key1="PARTYHARD"
            case 7: key1="BECOZY"
        
        if all([a in self._uniqueports for a in ["PARALLEL", "SERIAL"]]): key2=["SAFE","EFAS","MESSAGE","GROOVE"]
        elif sum([int(a) for a in self._sndigit])>10: key2=["CODE", "EDOC", "QUIET", "ETIUQ"]
        elif abs((self.batt-self.hold)-self.hold)>(self.batt-self.hold)*2: key2=["GROOVE", "EVOORG", "TEIUQ", "QUITE"]
        else: key2=["MESSAGE", "EGASSEM", "SAFE", "EDOC"]

        key2 = key2[self.__color]

        #modification
        if all([a not in self._snletter for a in "AIUEO"]):
            keyt = key1; key1 = key2; key2 = keyt
        if self.strikes>0:
            match self.strikes:
                case 1: keyX = "ONE"
                case 2: keyX = "TWO"
                case _: keyX = "MANY"
        keyfinal = key1+key2+keyX
        if sum([int(a) for a in self._sndigit]) in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
            keyfinal = keyfinal[::-1]
        
        keyfinal += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        #creating the board
        playground = []
        seen = set()
        for a in keyfinal:
            if a not in seen:
                seen.add(a); playground.append(a)
        if playground.index("I")>playground.index("J"):
            playground.pop(playground.index("I"))
            try: self.__encrypted[self.__encrypted.index("I")] = "J"
            except: pass
        elif playground.index("J")>playground.index("I"):
            playground.pop(playground.index("J"))
            try: self.__encrypted[self.__encrypted.index("J")] = "I"
            except: pass
        
        playground5 = [[],[],[],[],[]]
        for a in range(0,len(playground),5):
            playground5[a//5] = playground[a:a+5]
    
        #decrypting
        ans = []
        for a in range(0, len(self.__encrypted), 2):
            if playground.index(self.__encrypted[a])//5 == playground.index(self.__encrypted[a+1])//5:
                ans.append(playground5[(playground5[playground.index(self.__encrypted[a])//5].index(self.__encrypted[a])-1)%5])
                ans.append(playground5[(playground5[playground.index(self.__encrypted[a+1])//5].index(self.__encrypted[a+1])-1)%5])
            if playground5[playground.index(self.__encrypted[a])//5].index(self.__encrypted[a])==playground5[playground.index(self.__encrypted[a+1])//5].index(self.__encrypted[a+1]):
                ans.append(playground[(playground.index(self.__encrypted[a])-5)%len(playground)])
                ans.append(playground[(playground.index(self.__encrypted[a+1])-5)%len(playground)])
            else:
                r1 = playground.index(self.__encrypted[a])//5
                r2 = playground.index(self.__encrypted[a+1])//5
                c1 = playground5[r1].index(self.__encrypted[a])
                c2 = playground5[r2].index(self.__encrypted[a+1])
                ans.append(playground5[r1][c2])
                ans.append(playground5[r2][c1])
        
        #finding the answer
        return self.__find_answer(ans)
    
    def __find_answer(self, ans):
        table = {
            "STRIKE": ["ABCD", "CDAB", "BADC", "DABC"],
            "STRIK": ["BCDA", "DACB", "ADCB", "ABCD"],
            "STRYKE": ["CDAB", "ACBD", "DCBA", "BCDA"],
            "STRYK": ["DABC", "CBDA", "CBAD", "CDAB"],
            "ZTRIKE": ["ABDC", "BDAC", "BACD", "DACB"],
            "ZTRIK": ["BDCA", "DBCA", "ACDB", "ACBD"],
            "ZTRYKE": ["CABD", "BCAD", "CDBA", "CBDA"],
            "ZTRYK": ["DCAB", "CADB", "DBAC", "BDAC"]
        }
        return table.get("".join([a for a in ans if a !="X"]))[self.__color]

    def solve(self):
        '''
        Solve the Playfair Cipher module

        Returns:
            list (str): The correct order to press the buttons. First index represents the first button to press.
        '''
        return [a for a in self.__calculate()]