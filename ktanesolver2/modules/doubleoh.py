from ..edgework import edgework

class doubleoh(edgework):
    __table = [
        [
            [[60,'0X',15],[88,46,31],[74,27,53]],[[57,36,83],[70,22,64],['0X',41,18],],[[48,71,24],['0X',55,13],[86,30,62]]
        ],[
            [[52,10,'0X'],[33,65,78],[47,81,26]],[[43,85,37],[21,0,56],[68,14,72]],[[61,28,76],[12,44,87],[50,'0X',35]]
        ],[
            [['0X',38,42],[25,73,67],[11,54,80]],[[84,63,20],[16,58,'0X'],[32,77,45]],[[75,17,51],[34,82,40],[23,66,'0X']]
        ]
    ]

    def __check(self, n):
        if not isinstance(n, int): raise TypeError("currnumber must be in int")
        elif n<10: raise ValueError("number must be above than or equal to 10")
        return n
    
    def __init__(self, edgework:edgework, currnumber:int):
        '''
        Initialize a new doubleoh instance

        Args:
            edgework (edgework): The edgework of the bomb
            currnumber (int): The current number of your position that is NOT starting with 0. Must be any number that is above than or equal to 10
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__curr = self.__check(currnumber)

    def __calculate(self):
        ans = []
        y1=0; y2=0; x1=0; x2=0; flag=False
        for a in range(len(self.__table)):
            for b in range(len(self.__table[a])):
                for c in range(len(self.__table[a][b])):
                    if self.__curr in self.__table[a][b][c]:
                        y1 = a; x1 = b; y2 = c; x2 = self.__table[a][b][c].index(self.__curr)
                        flag=True
                        break
                if flag: break
            if flag: break
        if x2!=1 or y2!=1:
            def movex(x1,x2,y1,y2):
                if x2!=1:
                    if x2-1>0 and self.__table[y1][x1][y2][x2-1]!='0X': x2-=1
                    elif x2+1<3 and self.__table[y1][x1][y2][x2+1]!='0X': x2+=1
                    ans.append({tuple([self.__table[y1][x1][y2][0], self.__table[y1][x1][y2][1], self.__table[y1][x1][y2][2]]): self.__table[y1][x1][y2][x2]})
                return x1,x2,y1,y2
            def movey(x1,x2,y1,y2):
                if y2!=1:
                    if y2-1>0 and self.__table[y1][x1][y2-1][x2]!='0X': y2-=1
                    elif y2+1<3 and self.__table[y1][x1][y2+1][x2]!='0X': y2+=1
                    ans.append({tuple([self.__table[y1][x1][0][x2], self.__table[y1][x1][1][x2], self.__table[y1][x1][2][x2]]): self.__table[y1][x1][y2][x2]})
                return x1,x2,y1,y2
            if (self.__table[y1][x1][y2][x2-1]=='0X' and x2-1>0) or (self.__table[y1][x1][y2][x2+1]=='0X' and x2+1<3):
                x1,x2,y1,y2 = movey(x1,x2,y1,y2); x1,x2,y1,y2 = movex(x1,x2,y1,y2)
            else: x1,x2,y1,y2 = movex(x1,x2,y1,y2); x1,x2,y1,y2 = movey(x1,x2,y1,y2)
        if x1!=1 or y1!=1:
            if x1!=1:
                if x1-1>0 and self.__table[y1][x1-1][y2][x2]!='0X': x1-=1
                elif x2+1<3 and self.__table[y1][x1+1][y2][x2]!='0X': x1+=1
                ans.append({tuple([self.__table[y1][0][y2][x2], self.__table[y1][1][y2][x2], self.__table[y1][2][y2][x2]]): self.__table[y1][x1][y2][x2]})
            if y1!=1:
                if y1-1>0 and self.__table[y1-1][x1][y2][x2]!='0X': y1-=1
                elif y1+1<3 and self.__table[y1+1][x1][y2][x2]!='0X': y1+=1
                ans.append({tuple([self.__table[0][x1][y2][x2], self.__table[1][x1][y2][x2], self.__table[2][x1][y2][x2]]): self.__table[y1][x1][y2][x2]})
        return tuple(ans)
    
    def solve(self):
        '''
        Solve the Double-Oh module

        Returns:
            tuple (dict): The direction to reach 00. Each index contains a dict. Each dict have a key, where the key are the row/sequence number you need to find. The value of the key, are the number you need to land before going to the next one. For example: the current number is 35, and the dict says (50, '0X', 35): 35. In the module, keep pressing any button until you find these 3 numbers in a sequence. Once you've found it, land on the value of that key (which is 35)
        '''
        return self.__calculate()