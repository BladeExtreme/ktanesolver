from ..edgework import edgework

class pointoforder(edgework):
    __ranklist = ['c','s','d','h']
    
    def __check(self, c):
        suitlist = ['c','s','d','h','club','spade','diamond','heart']; ranklist = ['1','2','3','4','5','6','7','8','9','10','a','j','q','k','jack','queen','king','ace']
        
        if not isinstance(c, list): raise TypeError("cards must be in list")
        elif len(c)!=5: raise IndexError("Length of cards must be 5")
        elif not all([isinstance(a, list) for a in c]): raise TypeError("Element of cards must be in list")
        elif not all([len(a)==2 for a in c]): raise IndexError("Length of cards' elements must be 2")
        
        c = [['j' if a[0]==11 else 'q' if a[0]==12 else 'k' if a[0]==13 else 'a' if a[0]==1 else str(a[0]),a[1]] for a in c]
        
        if not all([isinstance(a, str) for b in c for a in b]): raise TypeError("Suit of cards must be in str and Rank of cards may be in int or str")
        elif not all([a[0].lower() in ranklist and a[1].lower() in suitlist for a in c]): raise ValueError("Rank/Suit must be valid")
        c = [[11 if a[0][0]=='j' else 12 if a[0][0]=='q' else 13 if a[0][0]=='k' else 1 if a[0][0]=='a' else int(a[0]),a[1][0]] for a in c]
        return c
    
    def __init__(self, edgework:edgework, cards:list):
        '''
        Initialize a new pointoforder instance

        Args:
            edgework (edgework): The edgework of the bomb
            cards (list [int|str, str], ...): The cards that appears on the module in list. Each list must contain the rank then the suit. Rank can be in int/str, and Suit must be in str
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__cards = self.__check(cards)
    
    def __calculate(self):
        rule1table = {
            's': [['s', 'h'], ['s', 'd'], ['h', 'c'], ['d', 'c']], 
            'h': [['h', 'c'], ['h', 's'], ['c', 'd'], ['s', 'd']], 
            'c': [['c', 'd'], ['c', 'h'], ['d', 's'], ['h', 's']], 
            'd': [['d', 's'], ['d', 'c'], ['s', 'h'], ['c', 'h']]
        }
        rule2alt = (int(ord(self.sn[3])-64)%3)+3
        rule3diff = [(int(ord(self.sn[4])-64)%3)+2, (int(ord(self.sn[4])-64)%3)+3]
        col = 0 if self.sn[0].isalpha() and self.sn[1].isalpha() else 1 if self.sn[0].isalpha() else 3 if self.sn[0].isnumeric() and self.sn[1].isnumeric() else 2

        rule1 = all([self.__cards[a][1] in rule1table[self.__cards[a-1][1]][col] for a in range(1, len(self.__cards))])
        rule2 = []
        rule3 = []

        result = 0 if self.__cards[0][0]%rule2alt==0 else 1
        for a in range(1,len(self.__cards)):
            if self.__cards[a-1][0]%rule2alt==0 and self.__cards[a][0]%rule2alt!=0 and result==0: rule2.append(True)
            elif self.__cards[a-1][0]%rule2alt!=0 and self.__cards[a][0]%rule2alt==0 and result==1: rule2.append(True)
            else: rule2.append(False)
            result = (result+1)%2
        rule2 = all(rule2)

        for a in range(1, len(self.__cards)):
            if abs(self.__cards[a-1][0]-self.__cards[a][0]) in rule3diff: rule3.append(True)
            else: rule3.append(False)
        rule3 = all(rule3)

        ans = [None,None]
        ans[0] = [a for a in range(1,14) if (a%rule2alt==0 if rule2 and result==1 else a%rule2alt!=0 if rule2 and result==0 else True) and (abs(self.__cards[-1][0]-a) in rule3diff if rule3 else True)]
        ans[1] = rule1table[self.__cards[-1][1]][col] if rule1 else list(set([self.__cards[a][1] for a in range(len(self.__cards))]))
        return ['jack' if a==11 else 'queen' if a==12 else 'king' if a==13 else 'ace' if a==0 else str(a) for a in ans[0]], ['club' if a=='c' else 'spade' if a=='s' else 'diamond' if a=='d' else 'heart' for a in ans[1]]

    def solve(self):
        '''
        Solve the Point of Order module

        Returns:
            tuple (list, list): The acceptable card for the module to solve. Index 0 list represents the rank of the valid card, index 1 list represents the suit of the valid card
        '''
        return tuple(self.__calculate())