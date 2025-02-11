from ..edgework import edgework

class x01(edgework):
    def __check(self, n):
        if not isinstance(n, list): raise TypeError("numbers must be in list")
        elif not all(isinstance(a, int) for a in n): raise TypeError("Element of numbers must be in int")
        elif len(n)!=10: raise IndexError("Length of numbers must be 10")
        elif not all(a>=0 for a in n): raise ValueError("Element of numbers cannot be negative")
        return n
    
    def __init__(self, edgework:edgework, numbers:list[int]):
        '''
        Initialize a new x01 instance

        Args:
            edgework (edgework): The edgework of the bomb
            numbers (list [int]): The score that appears on the module for each segments. NOTE: The list assumes that the first index is the topmost and its segment color is red
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__numbers = self.__check(numbers)
    
    def __checkrules(self, points):
        rules = set()
        for a in range(0,len(self.__numbers)):
            if all([b<=6 for b in [self.__numbers[a], self.__numbers[(a+1)%len(self.__numbers)], self.__numbers[(a+2)%len(self.__numbers)]]]): rules.add(0)
            if all([b>=15 for b in [self.__numbers[a], self.__numbers[(a+1)%len(self.__numbers)], self.__numbers[(a+2)%len(self.__numbers)]]]): rules.add(1)
            if all([b%2==0 for b in [self.__numbers[a], self.__numbers[(a+1)%len(self.__numbers)], self.__numbers[(a+2)%len(self.__numbers)]]]): rules.add(3)
        for a in range(0,len(self.__numbers)):
            if all([b%2==1 for b in [self.__numbers[a], self.__numbers[(a+1)%len(self.__numbers)], self.__numbers[(a+2)%len(self.__numbers)], self.__numbers[(a+3)%len(self.__numbers)]]]): rules.add(2)
        if any([a in self._snletter for a in "MVG"]): rules.add(4)
        if len([a for a in self.__numbers if a>10])==5: rules.add(5)
        if points<=45: rules.add(6)
        else: rules.add(7)

        dart_count = 0; restriction=[]
        match next(iter(rules)):
            case 0: dart_count = 3; restriction = [3,7]
            case 1: dart_count = 4; restriction = [4,8]
            case 2: dart_count = 3; restriction = [1,6]
            case 3: dart_count = 4; restriction = [2,4]
            case 4: dart_count = 4; restriction = [3,5,9]
            case 5: dart_count = 3; restriction = [7,8]
            case 6: dart_count = 2; restriction = []
            case 7: dart_count = 3; restriction = [2,5,9]
        return dart_count, restriction

    def __calculate(self):
        redtotal = []; greentotal=[]
        for a in range(0,len(self.__numbers),2):
            redtotal.append(self.__numbers[a])
            greentotal.append(self.__numbers[a+1])
        if sum(redtotal)==sum(greentotal): to_score=69
        else:
            colnum = len(self.ind)+len([a for b in self.ports for a in b])
            if colnum in range(0,3): colnum=0
            elif colnum in range(3,6): colnum=1
            else: colnum=2

            rownum = ((self.batt-self.hold))+len(self._sndigit)
            match rownum:
                case rownum if rownum in range(0,3): rownum=[74,53,79]
                case rownum if rownum in range(3,5): rownum=[62,41,70]
                case rownum if rownum==5: rownum=[42,47,86]
                case rownum if rownum in range(6,8): rownum=[38,66,51]
                case rownum if rownum >=8: rownum=[80,67,58]
            to_score = rownum[colnum]
            if sum(redtotal)>sum(greentotal): to_score += 10
            else: to_score -= 8
        darts, restriction = self.__checkrules(to_score)
        return self.__bfs(0, to_score, darts, restriction)
    
    def __checkrestriction(self, throws, darts, restrictions):
        good_restriction = set(); bullseye = 0; sinduotreb=set(); the_end=darts==len(throws); usedSingleOdd = False
        for score,mult in throws:
            if (mult==1) and (score%2==1) and (score!=-25): usedSingleOdd = True
            if (mult==-1) and (score==-25): bullseye+=1
            sinduotreb.add(mult)
        if (1 in restrictions) and (not usedSingleOdd): good_restriction.add(1)
        if the_end:
            if (2 in restrictions) and (throws[-1][1]==2):
                if (self.__numbers.index(throws[-1][0]) not in range(3,8)): good_restriction.add(2)
            if (3 in restrictions):
                for score,mult in throws:
                    if mult==-1: continue
                    if (self.__numbers.index(score) not in range(3,8)) and (mult==2):
                        good_restriction.add(3); break
            if (4 in restrictions) and (throws[-1][1]==2):
                if (self.__numbers.index(throws[-1][0])%2==1): good_restriction.add(4)
            if (5 in restrictions) and bullseye==1: good_restriction.add(5)
            if (6 in restrictions):
                for score,mult in throws:
                    if mult==3: good_restriction.add(6); break
            if (7 in restrictions) and sinduotreb==set([1,2,3]): good_restriction.add(7)
            if (8 in restrictions):
                for score,mult in throws:
                    if mult==-1: continue
                    if (mult==3) and (score%2==0): good_restriction.add(8); break
            if (9 in restrictions):
                temp = []
                for score,mult in throws:
                    temp.append(abs(score))
                if len(set(temp))==darts: good_restriction.add(9)
            if throws[-1][1]!=2: return False
        if not the_end:
            before_restriction = [a for a in restrictions if a not in [2,3,4,5,6,7,8,9]]
            return good_restriction==set(before_restriction)
        else: return good_restriction==set(restrictions)


    def __bfs(self, score, to_score, darts, restrictions):
        queue = [[score, [], 0]]

        while queue:
            current_score, throws, darts_used = queue.pop(0)
            if current_score==to_score and len(throws)==darts: return throws
            if current_score<0 or darts_used>darts: continue

            for seg in self.__numbers+[-25,-50]:
                if seg not in [-25,-50]:
                    for mul in [1,2,3]:
                        new_throws = throws+[[seg,mul]]
                        new_score = current_score+(seg*mul)
                        if self.__checkrestriction(new_throws, darts, restrictions):
                            queue.append([new_score, new_throws, darts_used+1])
                else:
                    new_throws = throws+[[seg,-1]]
                    new_score = current_score+(seg*-1)
                    if self.__checkrestriction(new_throws, darts, restrictions):
                        queue.append([new_score, new_throws, darts_used+1])
        return throws

    def solve(self, text:bool=True):
        '''
        Solve the X01 module

        Args:
            text (bool): The option to return the correct dart throws as text.By default, this argument is true.

        Returns:
            list (list [str|list [int]]): The correct dart throws to solve the module. First index is the first dart throw and so on. If the text argument is False, the list will return a nested list. Each nested list will have 2 values, first index values are the score to hit and the second index value are the multiplier. Multiplier of 0 indicates Bullseye. If the text argument is true, the letter "S","D","T", and "Bullseye" represents Single, Double, Treble (Triple) and Bullseye respectively.
        '''
        result = self.__calculate()
        if result is not None:
            if text:
                ans = []
                for a in range(len(result)):
                    mul = "S" if result[a][1]==1 else "D" if result[a][1]==2 else "T" if result[a][1]==3 else "Bullseye "
                    if mul!="Bullseye ":
                        ans.append(f"{mul}{result[a][0]}")
                    else: ans.append(f"{'SB' if result[a][0]==-25 else 'DB'}")
                return ans
            else:
                for a in result:
                    if a[0]<0:
                        a[0]*=-1; a[1]=0
                return result  
        else: return None