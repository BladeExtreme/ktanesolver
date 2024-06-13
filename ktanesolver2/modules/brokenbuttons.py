from ..edgework import edgework

class brokenbuttons(edgework):
    def __check(self, b):
        if not isinstance(b, list): raise TypeError("buttonlist must be in list")
        elif len(b)!=4: raise IndexError("Length of buttonlist must be 4")
        elif not all([isinstance(a, list) for a in b]): raise TypeError("Element of buttonlist must be in list")
        elif not all([len(a)==3 for a in b]): raise IndexError("Length of buttonlist elements must be 3")
        elif not all([isinstance(a, str) for c in b for a in c]): raise TypeError("Each element of buttonlist must consists of str")
        return [x.lower() for y in b for x in y]

    def __init__(self, edgework:edgework, buttonlist:list):
        '''
        Initialize a new brokenbuttons instance

        Args:
            edgework (edgework): The edgework of the bomb
            buttonlist (list [str, ...]): The list of buttons in the initial stage
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__buttonlist = self.__check(buttonlist)
        self.__submit = 0
        self.__pressedlist = []; self.__coord = None

    def __calculate(self):
        func = lambda x: ((int((self.__buttonlist.index(x)-(self.__buttonlist.index(x)%3))/3), int(self.__buttonlist.index(x)%3)), x)
        if len(self.__pressedlist)==5:
            return self.__submit, 'left' if self.__submit==0 else 'right'
        if 'sea' in self.__buttonlist: return func('sea')
        elif any(['t' == a[0] for a in self.__buttonlist[0:3]]) or any(['t'==a[0] for a in self.__buttonlist[6:9]]):
            for a in [0,1,2,6,7,8]:
                if 't'==self.__buttonlist[a][0]:
                    return (int((a-(a%3))/3), a%3), self.__buttonlist[a]
        elif 'one' in self.__buttonlist and 'submit' in self.__buttonlist: self.__submit = 0; return func('one')
        elif "" in self.__buttonlist: return func('')
        elif 'other' in self.__buttonlist: self.__submit = (self.__submit+1)%2; return func('other')
        elif len(self.__buttonlist)!=len(set(self.__buttonlist)): duplicate = [a for a in self.__buttonlist if self.__buttonlist.count(a)>1][0]; return func(duplicate)
        elif ('port' in self.__buttonlist or 'module' in self.__buttonlist) and any([a in self.__buttonlist for a in ['rca','parallel','serial','dvi-d','ps/2','rj']]): portname = [a for a in self.__buttonlist if a in ['rca','parallel','serial','dvi-d','ps/2','rj']][0]; return func(portname)
        elif any([len(a)<3 for a in self.__buttonlist]): word = [a for a in self.__buttonlist if len(a)<3][0]; return func(word)
        elif 'boom' in self.__buttonlist and 'bomb' in self.__buttonlist: return func('boom')
        elif 'submit' in self.__buttonlist and 'button' in self.__buttonlist:
            return self.__submit, 'left' if self.__submit==0 else 'right'
        elif 'column' in self.__buttonlist and ('seven' in self.__buttonlist or 'two' in self.__buttonlist): return func('column')
        elif len(self.__pressedlist)==0: return func(self.__buttonlist[5])
        elif 'e' in self.__pressedlist[0]: return 1, 'right'

    def solve(self, newlabel:str|None=None):
        '''
        Solve the Broken Buttons module

        Args:
            newlabel (str): The label of the recently pressed button
        Returns:
            tuple (tuple(int, int), str): The position of a required button press (index 0 is row, index 1 is column. Starting from 0), and the label of that button.
            tuple (int, str): The correct submit button to press. Index 0 is the position of the submit button (0 being left, 1 being right), index 1 is the direction of submit button (only 'left' or 'right')
        '''
        if newlabel is not None:
            if not isinstance(newlabel, str): raise TypeError("newlabel must be str")
            self.__buttonlist[self.__coord] = newlabel
        ans = self.__calculate(); self.__pressedlist.append(ans[-1])
        if isinstance(ans[0], tuple): self.__coord = (ans[0][0]*3+ans[0][1])
        return tuple(ans)