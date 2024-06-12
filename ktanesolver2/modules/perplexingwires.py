from ..edgework import edgework
from ..tools.colordict import _colorcheck

class perplexingwires(edgework):
    def __check(self, l):
        if not isinstance(l, list): raise TypeError("led must be in list")
        elif not all([isinstance(a, bool) for a in l]): raise TypeError("Element of led must be in bool")
        elif len(l)!=3: raise IndexError("Length of led must be 3")
        return l

    def __check2(self, w):
        if not isinstance(w, list): raise TypeError("wires must be in list")
        elif not all([isinstance(a, dict) for a in w]): raise TypeError("Element of wires must be in dict")
        elif not all([all([b in ['wirecolor','wirecross','star','indexstar','arrowdirection','arrowcolor'] for b in a]) for a in w]): raise TypeError("Keys of each wires must consists only of: 'wirecolor', 'wirecross', 'star', 'indexstar', 'arrowdirection', and 'arrowcolor'")
        elif not all(all([isinstance(a['wirecolor', str]) and isinstance(a['wirecross'], bool) and isinstance(a['star'], bool) and isinstance(a['arrowdirection'], str) and isinstance(a['arrowcolor'], str) for a in w])): raise TypeError("Value of each wires must be str for 'wirecolor', 'arrowdirection' and 'arrowcolor' keys; bool for 'star' and 'wirecross; and int for 'indexstar'")
        elif not all([a['arrowdirection'].lower() not in ['u','l','d','r','up','left','down','right'] for a in w]): raise ValueError("Value of arrowdirection must be either: u/up, l/left, r/right, or d/down")
        return w
    
    def __check3(self, c,r,s,n,d,a):
        if not isinstance(c, list): raise TypeError("wirecolor must be in list")
        elif not isinstance(r, list): raise TypeError("wirecross must be in list")
        elif not isinstance(s, list): raise TypeError("star must be in list")
        elif not isinstance(n, list): raise TypeError("starfromindexwire must be in list")
        elif not isinstance(d, list): raise TypeError("arrowdirection must be in list")
        elif not isinstance(a, list): raise TypeError("arrowcolor must be in list")
        elif not len(c)==len(r)==len(d)==len(a): raise IndexError("Length of wirecolor, wirecross, starfromindexwire, arrowdirection and arrowcolor must be same")
        elif not len(s)==len(n): raise IndexError("Length of star and starfromindexwire must be 4")
        elif not all([isinstance(b, str) for b in c]): raise TypeError("Element of wirecolor must be in str")
        elif not all([isinstance(b, bool) for b in r]): raise TypeError("Element of wirecross must be in bool")
        elif not all([isinstance(b, bool) for b in s]): raise TypeError("Element of star must be in bool")
        elif not all([isinstance(b, list) for b in n]): raise TypeError("Element of starfromindexwire must be in list")
        elif not all([isinstance(b, int) for c in n for b in c]): raise TypeError("Each element of starfromindexwire must be in int")
        elif not all([isinstance(b, str) for b in d]): raise TypeError("Element of arrowdirection must be in str")
        elif not all([isinstance(b, str) for b in a]): raise TypeError("Element of arrowcolor must be in str")
        elif not all([b.lower() in ['u','l','d','r','up','left','down','right'] for b in d]): raise ValueError("Value of arrowdirection must be either: u/up, l/left, r/right, or d/down")
        arr = []
        for b in range(len(c)):
            temp = {'wirecolor': None, 'wirecross': None, 'star': None, 'indexstar': None, 'arrowdirection': None, 'arrowcolor': None}
            temp['wirecolor'] = _colorcheck(c[b].lower()); temp['wirecross'] = r[b]; temp['arrowdirection'] = d[b].lower(); temp['arrowcolor'] = _colorcheck(a[b]);
            temp['indexstar'] = n.index([c for c in n if b in c][0])
            temp['star'] = s[temp['indexstar']]
            arr.append(temp)
        return arr
    
    def __init__(self, edgework:edgework, led:list, wirecolor:list|None=None, wirecross:list|None=None, star:list|None=None, starfromindexwire:list|None=None, arrowdirection:list|None=None, arrowcolor:list|None=None, wires:list|None=None):
        '''
        Initialize a new perplexingwires instance

        Args:
            edgework (edgework): The edgework of the bomb
            wirecolor (list [str, ...]): The color of the wire from most left to most right. CAUTION: wirecolor must sync with wirecross, starfromindexwire, arrowdirection, arrowcolor
            wirecross (list [bool, ...]): The state if the wire crosses with another wire or not. CAUTION: wirecross must sync with wirecolor, starfromindexwire, arrowdirection, arrowcolor
            star (list [bool, ...]): The state of the star if its lit or not. CAUTION: star must sync with starfromindexwire
            starfromindexwire(list [[int,...]]): The index of wire that connects to this wire. All elements must be list, even only one wire is connected to the star. CAUTION: starfromindexwire must be sync with star and wirecolor, wirecross, arrowdirection, arrowcolor
            arrowdirection (list [str, ...]): The direction of the arrow that appears on each wire. Must be either u/up, l/left, r/right, d/down. CAUTION: arrowdirection must be in sync with wirecolor, wirecross, arrowcolor
            arrowcolor (list [str, ...]): The color of each arrow that appears below the wires. CAUTION arrowcolor must be in sync with wirecolor, wirecross, arrowdirection
            wires (list [dict, ...]): The wires that appears on the bomb, each wire must be in dict where it contain the following key: 'wirecolor', 'wirecross', 'star', 'indexstar', 'arrowdirection', 'arrowcolor'. Values for 'wirecolor', 'arrowdirection', 'arrowcolor' must be in str; while 'star' in boolean; and 'indexstar' must be in int.
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__led = self.__check(led)
        if wires is not None:
            self.__wires = self.__check2(wires)
        elif wirecolor is not None and wirecross is not None and star is not None and starfromindexwire is not None and arrowdirection is not None and arrowcolor is not None:
            self.__wires = self.__check3(wirecolor, wirecross, star, starfromindexwire, arrowdirection, arrowcolor)
        else:
            raise TypeError("perplexingwires.__init__() missing 1 or 5 required positional arguments: 'wirecolor', 'wirecross', 'star', 'arrowdirection', 'arrowcolor | 'wires'")
    
    def __calculate(self):
        table = [
            [
                [
                    [[lambda p,c,a: p==len(self.ind)-1, lambda p,c,a: True], [lambda p,c,a: [z['wirecolor'] for z in self.__wires].count(c)==1, lambda p,c,a: p==self.batt-1]],
                    [[lambda p,c,a: a=='u' or a=='d', lambda p,c,a: True], [lambda p,c,a: self.__led.count(True)>self.__led.count(False), lambda p,c,a: p==len([x for y in self.ports for x in y])-1]],
                ],[
                    [[lambda p,c,a: 0, lambda p,c,a: len([self.__wires[z]['indexstar'] for z in range(len(self.__wires)) if z!=p])>0], [lambda p,c,a: True if self.__wires[p+1]['wirecolor'] in ['purple', 'orange'] and p+1 < len(self.__wires) or self.__wires[p-1]['wirecolor'] in ['purple', 'orange'] and p-1 > -1 else False, lambda p,c,a: [x['wirecolor'] for x in self.__wires].count(c)==1]],
                    [[lambda p,c,a: [x['arrowdirection'] for x in self.__wires].count(a)==1, lambda p,c,a: len([self.__wires[z]['indexstar'] for z in range(len(self.__wires)) if z!=p])>0], [lambda p,c,a: self.__led[0], lambda p,c,a: False]]
                ]
            ],[
                [
                    [[lambda p,c,a: -1, lambda p,c,a: p==len(self.ind)-1],[lambda p,c,a: self.__led[0], lambda p,c,a: self.__wires[p]['arrowdirection']=='d']],
                    [[lambda p,c,a: self.__led.count(True)>self.__led.count(False), lambda p,c,a: p==len([x for y in self.ports for x in y])-1],[lambda p,c,a: any([x in ['A','I','U','E','O'] for x in self._snletter]), lambda p,c,a: False]],
                ],[
                    [[lambda p,c,a: a in ['d','r'], lambda p,c,a: p==len(self.ind)-1],[lambda p,c,a: -1, lambda p,c,a: True if self.__wires[p+1]['wirecolor'] in ['purple', 'orange'] and p+1 < len(self.__wires) or self.__wires[p-1]['wirecolor'] in ['purple', 'orange'] and p-1 > -1 else False]],
                    [[lambda p,c,a: any([x in ['A','I','U','E','O'] for x in self._snletter]), lambda p,c,a: 0],[lambda p,c,a: [x['arrowdirection'] for x in self.__wires].count(a)==1, lambda p,c,a: p==(self.batt)-1]]
                ]
            ]
        ]
        ans = [False for a in range(len(self.__wires))]
        for a in range(len(self.__wires)):
            maintable = 0 if self.__wires[a]['wirecolor'] in ['red','yellow','white','blue'] else 1
            col1 = 1 if self.__wires[a]['wirecolor']==self.__wires[a]['arrowcolor'] else 0; col2 = 0 if self.__wires[a]['star'] else 1
            row1 = 0 if (a+1)%2==1 else 1; row2 = 1 if self.__wires[a]['wirecross'] else 0
            ans[a] = table[maintable][row1][row2][col1][col2](a, self.__wires[a]['wirecolor'], self.__wires[a]['arrowdirection'])
        return ans

    def solve(self):
        '''
        Solve the Perplexing Wire module

        Returns:
            tuple (tuple, tuple, tuple): Index 0 contains the list the order of wire cutting, starting from 0. Index 1 is similar to index 0 but starts with 1 instead. Index 2 are the color of the wire to be cut, refer to index 0 or 1 if a color exist in multiple wires.
        '''
        ans = self.__calculate()
        order = []; begin=[]; mid=[]; last=[]
        for a in range(len(ans)):
            if isinstance(ans[a], bool):
                if ans[a]: mid.append(a)
            else:
                if ans[a]==0: begin.append(a)
                elif ans[a]==1: last.append(a)
        order.append(begin); order.append(mid); order.append(last)
        return tuple([tuple([x for y in order for x in y]), tuple([x+1 for y in order for x in y]), tuple([self.__wires[x]['wirecolor'] for y in order for x in y])])