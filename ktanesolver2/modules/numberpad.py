from ..edgework import edgework
from ..tools.colordict import _colorcheck

class numberpad(edgework):
    __table = [
        [2,5,7,8],
        [2,3,9,0,2,6,0,9,4,7,2,0,9,6,3,1],
        [4,3,9,4,0,9,7,9,6,4,6,2,2,8,7,4,9,8,1,5,8,0,0,9,6,0,9,2,3,6,2,3],
        [6,8,1,3,5,1,3,6,9,7,8,9,8,9,4,0,0,3,1,7,3,5,8,5,6,0,6,0,9,8,2,9,1,4,0,8,8,5,8,3,6,0,8,2,3,4,0,3,7,5,6,1,2,9,0,7,6,9,0,6,3,8,3,5]
    ]

    def __check(self, c):
        if not isinstance(c, list) and not isinstance(c, dict): raise TypeError("color must be in either list or dict")
        elif len(c)!=10: raise IndexError("Length of color must be 10")
        if isinstance(c, list):
            if not all([isinstance(a, str) for a in c]): raise TypeError("Element of color must be in str")
            return [_colorcheck(a.lower()) for a in c]
        elif isinstance(c, dict):
            if not all([a in range(0,10) for a in c]): raise KeyError("Key must consist of only: 0,1,2,3,4,5,6,7,8,9 in integer")
            elif not all([isinstance(a, str) for a in c.values()]): raise TypeError("Values of each key must be in str")
            return [_colorcheck(c[a].lower()) for a in range(0,10)]
	
    def __init__(self, edgework:edgework, color:list|dict):
        '''
		Initialize a new numberpad instance
		
		Args:
			edgework (edgework): The edgework of the bomb
			color (list): The color list from number 1 to number 0, in reading order. Index 0 represents number 1, index 1 represents number 2 and so on
			color (dict): The color of each number in dict. Keys must consist of: 1,2,3,4,5,6,7,8,9,0 in integer.
		'''
        super().__init__(edgework.batt, edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.strikes)
        self.__colorlist = self.__check(color)
    
    def __calculate(self):
        ans = []

        pA = 0 if self.__colorlist.count('yellow')>=3 else 1 if (self.__colorlist[3] in ['white','blue','red'] and self.__colorlist[4] in ['white','blue','red'] and self.__colorlist[5] in ['white','blue','red']) else 2 if any([a in ['A','I','U','E','O'] for a in self._snletter]) else 3; ans.append(self.__table[0][pA]); pB = pA*4
        pB += 0 if (self.__colorlist.count('blue')>=2 and self.__colorlist.count('green')>=3) else 1 if (self.__colorlist[4] not in ['blue', 'white']) else 2 if len([a for b in self.ports for a in b])<2 else 3; ans.append(self.__table[1][pB]); pC = (pA*8)+(pB*4)
        pC += 0 if self.__colorlist.count('white')>2 and self.__colorlist.count('yellow')>2 else 1; ans.append(self.__table[2][pC]); ans = ans[::-1] if ans else ans; pD = (pA*16)+(pB*4)+(pC*2)
        pD += 0 if self.__colorlist.count('yellow')<=2 else 1; ans.append(self.__table[3][pD]); ans = [(a+1)%10 if not pD else a for a in ans]
    
        if int(self._sndigit[-1])%2==0: temp=ans[0]; ans[0]=ans[2]; ans[2]=temp
        if self.batt%2==1: temp=ans[1]; ans[1]=ans[2]; ans[2]=temp
        if int(self._sndigit[-1])%2==1 and self.batt%2==0: temp=ans[0]; ans[0]=ans[3]; ans[3]=temp
        if sum(ans)%2==0: ans = ans[::-1]

        return ans

    def solve(self):
        '''
        Solve the Number Pad module

        Returns:
            int: The number code to be submitted
        '''
        return self.__calculate()