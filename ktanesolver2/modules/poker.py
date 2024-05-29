from ..edgework import edgework

class poker(edgework):
    __rankdict = {"ace":'1', "two": '2', "five": '5', "king":'13'}
    __suitdict = {"spade": 's', "club":'c', "diamond":'d', "heart":'h'}
    __flowchart = {
        tuple(['1','s']): ['ALL-IN', 'MAX RAISE', 'MIN RAISE', 'CHECK', 'FOLD', 'CHECK', 'MIN RAISE', 'CHECK', 'ALL-IN', 'MAX RAISE', 'CHECK', 'MAX RAISE', 'FOLD', 'CHECK', 'FOLD', 'CHECK'],
        tuple(['13','h']): ['ALL-IN', 'MAX RAISE', 'CHECK', 'MAX RAISE', 'FOLD', 'CHECK', 'FOLD', 'FOLD', 'CHECK', 'MIN RAISE', 'CHECK', 'CHECK', 'CHECK', 'FOLD', 'FOLD', 'FOLD'],
        tuple(['5','d']): ['MIN RAISE', 'FOLD', 'MIN RAISE', 'CHECK', 'FOLD', 'CHECK', 'FOLD', 'CHECK', 'CHECK', 'MAX RAISE', 'MAX RAISE', 'FOLD', 'ALL-IN', 'MIN RAISE', 'MIN RAISE', 'CHECK'],
        tuple(['2','c']): ['FOLD', 'CHECK', 'MAX RAISE', 'MAX RAISE', 'CHECK', 'MIN RAISE', 'CHECK CHECK', 'MIN RAISE', 'CHECK', 'MIN RAISE', 'FOLD', 'CHECK', 'MIN RAISE', 'FOLD', 'CHECK']
    }
    
    def __check(self, r, s):
        if not isinstance(r, str): raise TypeError("Rank must be in str")
        elif not isinstance(s, str): raise TypeError("Suit must be in str")
        elif r not in ['ace', '2', '5', 'two', 'five', 'king']: raise ValueError("This rank is invalid")
        elif s not in ['spade', 'club', 'diamond', 'heart']: raise ValueError("This suit is invalid")

        try: r = self.__rankdict[r]
        except: pass
        try: s = self.__suitdict[s]
        except: pass

        return [r,s]
    def __check2(self, r):
        if not isinstance(r, str): raise TypeError("Response must be in str")
        return r
    def __check3(self, c, b):
        if not isinstance(c, list): raise TypeError("Cardlist must be in list")
        elif len(c) != 4: raise IndexError("Length of cardlist must be 4")
        elif not isinstance(b, int): raise TypeError("Bet must be in int")
        elif any([True if not isinstance(a, str) else False for a in c]): raise TypeError("Each card in cardlist must be in str")
        elif any([True if a not in ['spade', 'club', 'diamond', 'heart'] else False for a in c]): raise ValueError("One of card suit is invalid")
        elif b not in [25,50,100,500]: raise ValueError("This betting number is invalid")
        else: return [self.__suitdict[a] for a in c],b

    def __init__(self, edgework:edgework, rank:str, suit:str):
        '''
        Initialize a new poker instance

        Args:
            edgework (edgework): The edgework of the bomb
            rank (str): The rank of the card
            suit (str): The suit of the card
        '''
        super().__init__(edgework.batt, edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__card = self.__check(rank.lower(), suit.lower())

    def __checkrule(self, state, condition, rule):
        if rule=='in':
            if isinstance(condition, list):
                if any([True if a in condition else False for a in state]): return True
            else:
                if condition in state: return True
        elif rule=='equal more':
            if state >= condition: return True
        elif rule=='more':
            if state > condition: return True
        elif rule == 'less':
            if state < condition: return True
        elif  rule == 'equal less':
            if state <= condition: return True
        return False

    def __calculate1(self):
        binary = ''
        if self.__card == ['1','s']:
            binary += '0' if self.__checkrule(self.batt, 3, 'equal more')  else '1'
            if binary[-1] == '0':
                binary += '0' if self.__checkrule(self._litind, 'FRK*', 'in') or self.__checkrule(self._litind, 'BOB*', 'in') else '1'
                if binary[-1] == '0':
                    binary += '0' if sum([int(a) for a in self._sndigit])%2==0 else '1'
                    if binary[-1] == '0': binary += '0' if self.__checkrule(self._uniqueports, 'RJ-45', 'in') else '1'
                    else: binary += '0' if self.__checkrule(self._uniqueports, 'PS/2', 'in') else '1'
                else:
                    binary += '0' if self.__checkrule(self.batt-((self.batt-self.hold)*2), (self.batt-self.hold)*2, 'more') else '1'
                    if binary[-1] == '0': binary += '0' if self.__checkrule(self._snletter, ['a','i','u','e','o'], 'in') else '1'
                    else: binary += '0' if int(self._sndigit[-1])%2 == 0 else '1'
            else:
                binary += '0' if self.__checkrule(self._snletter, ['a','i','u','e','o'], 'in') else '1'
                if binary[-1] == '0':
                    binary += '0' if self.__checkrule(self._unlitind, 'CAR', 'in') else '1'
                    if binary[-1] == '0': binary += '0' if self.__checkrule(self._uniqueports, 'DVI-D', 'in') else '1'
                    else: binary += '0' if self.__checkrule(self._uniqueports, 'PARALLEL', 'in') else '1'
                else:
                    binary += '0' if self.__checkrule(self._uniqueports, 'SERIAL', 'in') else '1'
                    if binary[-1] == '0': binary += '0' if self.__checkrule(self._unlitind, 'SND', 'in') or self.__checkrule(self._unlitind, 'TRN', 'in') else '1'
                    else: binary += '0' if self.__checkrule(self._litind, 'SIG*', 'in') or self.__checkrule(self._litind, 'FRQ*', 'in') else '1'
        elif self.__card == ['13','h']:
            binary += '0' if sum([int(a) for a in self._sndigit])%2 == 1 else '1'
            if binary[-1] == '0':
                binary += '0' if self.__checkrule(self.batt, 1, 'equal more') else '1'
                if binary[-1] == '0':
                    binary += '0' if self.__checkrule(self._litind, ['IND*','MSA*','TRN*'], 'in') else '1'
                    if binary[-1] == '0': binary += '0' if self.__checkrule(self._uniqueports, 'STEREO RCA', 'in') else '1'
                    else: binary += '0' if self.__checkrule(self._uniqueports, 'RJ-45', 'in') and self.__checkrule(self._uniqueports, 'SERIAL', 'in') else '1'
                else:
                    binary += '0' if self.__checkrule(self._uniqueports, 'PS/2', 'in') or self.__checkrule(self._uniqueports, 'DVI-D', 'in') else '1'
                    if binary[-1] == '0': binary += '0' if self.__checkrule(self._litind, 'SND*', 'in') else '1'
                    else: binary += '0' if self.__checkrule(self._unlitind, 'TRN', 'in') or self.__checkrule(self._unlitind, 'FRK', 'in') else '1'
            else:
                binary += '0' if self.__checkrule(self._uniqueports, 'PARALLEL', 'in') else '1'
                if binary[-1] == '0':
                    binary += '0' if self.__checkrule((self.batt-self._hold)*2, 3, 'equal less') else '1'
                    if binary[-1] == '0': binary += '0' if self.__checkrule(self._unlitind, 'MSA', 'in') or self.__checkrule(self._litind, 'NSA*', 'in') else '1'
                    else: binary += '0' if self.__checkrule(self._litind, 'FRQ*', 'in') else '1'
                else:
                    binary += '0' if self.__checkrule(self._unlitind, 'BOB', 'in') or self.__checkrule(self._unlitind, 'FRQ', 'in') else '1'
                    if binary[-1] == '0': binary += '0' if self.__checkrule((self.batt-self.hold)*2, self.batt-((self.batt-self.hold)*2), 'more') else '1'
                    else: binary += '0' if self.batt <= 5 else '1'
        elif self.__card == ['5','d']:
            binary += '0' if self.__checkrule((self.batt-self.hold)*2, self.batt-((self.batt-self.hold)*2), 'more') else '1'
            if binary[-1] == '0':
                binary += '0' if self.__checkrule(self._snletter, ['a','i','u','e','o'], 'in') else '1'
                if binary[-1] == '0':
                    binary += '0' if self.__checkrule(len(self._uniqueports), 1, 'more') else '1'
                    if binary[-1] == '0': binary += '0' if self.__checkrule(self._unlitind, 'CLR', 'in') or self.__checkrule(self._litind, 'CAR*', 'in') else '1'
                    else: binary += '0' if self.__checkrule(self._unlitind, 'NSA', 'in') or self.__checkrule(self._litind, 'MSA*', 'in') else '1'
                else:
                    binary += '0' if self.__checkrule(self._uniqueports, 'PS/2', 'in') or self.__checkrule(self._uniqueports, 'RJ-45', 'in') else '1'
                    if binary[-1] == '0': binary += '0' if self.__checkrule(len(self._unlitind), 0, 'more') else '1'
                    else: binary += '0' if self.__checkrule(self._unlitind, 'CLR', 'in') else '1'
            else:
                binary += '0' if int(self._sndigit[-1])%2 == 1 else '1'
                if binary[-1] == '0':
                    binary += '0' if self.__checkrule(self._litind, 'BOB*', 'in') or self.__checkrule(self._unlitind, 'FRQ', 'in') or self.__checkrule(self._unlitind, 'SIG', 'in') else '1'
                    if binary[-1] == '0': binary += '0' if self.__checkrule(len(self._uniqueports), 0, 'more') else '1'
                    else: binary += '0' if self.__checkrule(self._uniqueports, 'PARALLEL', 'in') else '1'
                else:
                    binary += '0' if self.__checkrule(self._litind, 0, 'more') else '1'
                    if binary[-1] == '0': binary += '0' if self.__checkrule(len(self._uniqueports, 3, 'less')) else '1'
                    else: binary += '0' if self.__checkrule(self._uniqueports, 'DVI-D', 'in') and self.__checkrule(self._uniqueports, 'STEREO RCA', 'in') else '1'
        elif self.__card == ['2','c']:
            binary += '0' if self.__checkrule(self._litind, ['TRN*', 'BOB*', 'IND*'], 'in') else '1'
            if binary[-1] == '0':
                binary += '0' if self.__checkrule(self.batt, 5, 'equal less') else '1'
                if binary[-1] == '0':
                    binary += '0' if self.__checkrule(self._uniqueports, 'DVI-D', 'in') or self.__checkrule(self._uniqueports, 'STEREO RCA', 'in') else '1'
                    if binary[-1] == '0': binary += '0' if self.__checkrule(self._snletter[-1], ['a','i','u','e','o'], 'in') else '1'
                    else: binary += '0'
                else:
                    binary += '0' if self.__checkrule(sum([int(a) for a in self._sndigit]), 12, 'more') else '1'
                    if binary[-1] == '0': binary += '0' if self.__checkrule(self._uniqueports, 'PS/2', 'in') and self.__checkrule(self._uniqueports, 'PARALLEL', 'in') else '1'
                    else: binary += '0'
            else:
                binary += '0' if self.__checkrule(len(self._snletter)%2, 0, 'equal') else '1'
                if binary[-1] == '0':
                    binary += '0' if self.__checkrule(self._uniqueports, 'PARALLEL', 'in') and self.__checkrule(self._uniqueorts, 'SERIAL', 'in') else '1'
                    if binary[-1] == '0': binary += '0' if self.__checkrule((self.batt-self.hold)*2, self.batt-((self.batt-self.hold)*2), 'more') else '1'
                    else: binary += '0' if self.__checkrule(self.batt-((self.batt-self.hold)*2), (self.batt-self.hold)*2, 'more') else '1'
                else:
                    binary += '0' if self.__checkrule(self._uniqueports, 'RJ-45', 'in') else '1'
                    if binary[-1] == '0': binary += '0' if self.__checkrule(self.batt-((self.batt-self.hold)*2), 2, 'more') else '1'
                    else: binary += '0' if self.__checkrule(self.batt, 2, 'more') else '1'
        else: raise ValueError("This combination of rank and suit does not exist for the diagram")

        return self.__flowchart[tuple(self.__card)][int(binary, 2)]
    def __calculate2(self):
        if self.__bet==25:
            if self.__cardlist[0] in ['h','d'] and self.__checkrule(self._litind, 'BOB*', 'in'): return 4
            elif self.__response == 'awful play' and self.__card == ['1','s']: return 1
            elif self.__checkrule(self._unlitind, 'FRQ', 'in') and self.__cardlist[-1] in ['s','c']: return 2
            elif self.__cardlist.count('d') >= 1 and (self.__response == "really" or self.__response == 'really rearlly'): return 3
            elif self.__cardlist[-1] == 's' and self.batt < 4: return 3
            elif self.__cardlist[2] == 'd' and self.__cardlist[1] != 'c': return 2
            elif self.__response == 'are you sure' and self.__card == ['2','c']: return 1
            elif self.__card == ['5','d']: return 4
            elif self.__cardlist[1] == 'c' and self._uniqueports.count('RJ-45') == 0: return 2
            else: return 1
        elif self.__bet == 50:
            if self.__response == "sure about that" and self.__cardlist[-1] == 'h': return 1
            elif self.__cardlist.count('c') == 0 and self.__card == ['2','c']: return 3
            elif self.__cardlist.count('d') == 0 and any([True if self.__cardlist[a]=='h' and self.__cardlist[a+1]=='s' else False for a in range(len(self.__cardlist))]): return 4
            elif self.__cardlist[0] == 'h' and self.__card != ['13','h']: return 2
            elif self.__response == 'really really' and self.__cardlist[0] == 'h' or self.__cardlist[1] == 'h': return 4
            elif self.__card == ['5','d'] and self._uniqueports.count("PARALLEL") >= 1: return 1
            elif self.__checkrule(self._litind, 'TRN*', 'in') and sum([self.__cardlist.count('c'), self.__cardlist.count('s')]) >= 1: return 2
            elif self.__response == "terrible play": return 3
            elif sum([int(a) for a in self._sndigit]) < 10: return 1
            else: return 3
        elif self.__bet == 100:
            if self.__response == "really really": return 2
            elif self.__response == "really": return 4
            elif self.batt-((self.batt-self.hold)*2)==0 and self.__card == ['1','s']: return 1
            elif sum([int(a) for a in self._sndigit]) in [2,3,5,7,11,13,17,19,23,27,29,31,37,41,43,47,53] and self.__cardlist.count('h') >= 1: return 4
            elif (self.__cardlist.count('s') >= 1 or self.__cardlist.count('c') >= 1) and self.__response == 'sure about that': return 3
            elif self.__checkrule(self._unlitind, 'MSA', 'in'): return 1
            elif self.__cardlist.count('d') >= 1: return 3
            elif self.__response == 'awful play': return 4
            else: return 2
        elif self.__bet == 500:
            if self.__cardlist.count('c') > 1: return 3
            elif self.__checkrule(self._snletter, ['a','i','u','e','o'], 'in') and self.__cardlist.count('s') >= 1: return 2
            elif len(self._uniqueports) == 0 and self.__cardlist.count('h') >= 1: return 1
            elif self.__cardlist.count('h') == 0 and self.__cardlist.count('d') == 0: return 4
            elif self.__response == "are you really sure": return 4
            elif len(self._litind) == 0 and self.__cardlist[0] == 'h': return 3
            elif len(self._unlitind) >= 1 and self.__cardlist[1] == 'c': return 2
            elif self.__response == "really" and self.__cardlist.count('c') == 0 and self.__cardlist.count('s') == 0: return 1
            elif self.batt-((self.batt-self.hold)*2) > 1: return 3
            else: return 4

    def __respond(self, response:str):
        table = {
            "terrible play": [1,1,1,0],
            "awful play": [0,1,1,0],
            "really": [1,0,0,0],
            "really really": [0,0,1,0],
            "sure about that": [1,0,0,1],
            "are you sure": [0,1,1,1]
        }
        table2 = {
            tuple(['1','s']): 0,
            tuple(['13', 'h']): 1,
            tuple(['5', 'd']): 2,
            tuple(['2', 'c']): 3
        }
        self.__response = ''.join([a.replace("!","").replace("?","").replace(",","") for a in self.__check2(response.lower())])
        return 'truth' if table[self.__response][table2[tuple(self.__card)]]==1 else 'bluff'

    def __betting(self, cardlist:list, bet:int):
        try: self.__response
        except(AttributeError): raise AttributeError("Opponent's response has not been set")
        self.__cardlist, self.__bet = self.__check3([a.lower() for a in cardlist], bet)
        ans = self.__calculate2()
        return tuple([ans-1, ans, cardlist[ans-1]])

    def solve(self, response:str|None=None, cardlist:list|None=None, bet:int|None=None, stage:int=0):
        '''
        Solve the Poker module

        Args:
            stage (int): The stage on which stage of poker needs to be solved. Accepts only 0 to 2. By default is 0. 0 represents the initial stage (fold, check, etc.). 1 represents the bluff/truth stage. 2 reprsents the betting stage.
        Returns:
            str: Returns which button to press.
            Tuple (int, int, str): The tuple for the correct cardlist index, nth order from module (starting by 1), the suit.
        '''
        if not isinstance(stage, int): raise TypeError("Stage must be in int")
        elif stage<0 or stage>2: raise ValueError("Stage must be in range of 0-2")

        if stage==0:
            ans = self.__calculate1()
        elif stage==1:
            ans = self.__respond(response)
        elif stage==2:
            ans = self.__betting(cardlist, bet)
        return ans