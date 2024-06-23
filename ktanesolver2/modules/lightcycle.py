from ..edgework import edgework
from ..tools.colordict import _colorcheck

class lightcycle(edgework):
    __table = [
        [[5,'blue'],['blue','red'],['magenta','green'],['yellow',5],[4,1],['red','white'],[6,4],[1,6],[2,3],[3,'magenta'],['green','yellow'],['white',2]],
        [[2,'red'],[6,'magenta'],[4,3],[5,'blue'],['red',5],['yellow',2],[1,'green'],['magenta','yellow'],['white',6],[3,4],['blue','white'],['green',1]],
        [['magenta','yellow'],[2,4],['yellow','red'],[3,5],['white',2],['green','blue'],[1,'white'],['red',3],[5,'green'],[4,6],['blue','magenta'],[6,1]],
        [[5,6],[6,3],[1,4],['magenta',2],['red','yellow'],[2,'magenta'],['white','red'],['blue','green'],['yellow','white'],[3,'blue'],['green',1],[4,5]],
        [['blue','red'],['white',2],[2,3],[1,4],['magenta','blue'],[5,6],['yellow','white'],['red','magenta'],['green','yellow'],[6,'green'],[3,5],[4,1]],
        [['red','yellow'],[2,'green'],[1,'magenta'],['yellow',5],[5,'red'],['white','blue'],[6,3],['blue',1],['magenta',4],['green',6],[3,2],[4,'white']],
        [['yellow',1],[5,4],[2,'white'],['red','yellow'],[1,'red'],['blue',3],[6,'green'],['green',6],['magenta','blue'],['white',5],[4,2],[3,'magenta']],
        [[3,5],['white','yellow'],['green',2],[2,'blue'],[5,'green'],['magenta','red'],['blue',3],[1,4],[4,6],['yellow','magenta'],[6,'white'],['red',1]],
        [['red','magenta'],[4,5],[5,'white'],['blue',1],['magenta',6],[3,2],['white','blue'],['green','yellow'],['yellow','red'],[1,4],[6,'green'],[2,3]],
        [['white','blue'],['red',6],[5,'yellow'],[4,1],[2,5],['yellow',3],['magenta','white'],[3,2],['blue','green'],['green','magenta'],[1,'red'],[6,4]],
        [[6,4],['blue',2],['white','green'],['red',5],['green',1],[2,'yellow'],['yellow','red'],['magenta','blue'],[1,6],[3,'white'],[5,3],[4,'magenta']],
        [[6,4],['blue',5],['white',6],[1,'green'],['red',2],[4,'red'],['green','white'],[3,'magenta'],[2,'blue'],['yellow',3],[5,'yellow'],['magenta',1]],
        [['white',3],[3,'green'],[2,4],['yellow','magenta'],['magenta',2],['red',5],[6,'red'],['blue',6],['green','yellow'],[5,'blue'],[1,'white'],[4,1]],
        [[1,'yellow'],[6,'magenta'],[2,1],['green','red'],[3,'green'],[5,'blue'],['red',4],[4,3],['white',2],['yellow','white'],['blue',5],['magenta',6]],
        [['red',5],[3,'green'],[2,3],['white',4],['blue',2],[1,'magenta'],[5,6],['magenta',1],[4,'yellow'],['green','blue'],[6,'red'],['yellow','white']],
        [[1,4],[4,'blue'],[6,2],[3,'white'],['magenta','red'],['yellow',6],['blue','yellow'],[2,'green'],[5,'magenta'],['green',5],['red',3],['white',1]],
        [[5,'green'],['magenta','blue'],[4,'white'],['yellow',2],['red','magenta'],['white',4],[6,1],[3,6],['blue','yellow'],[1,5],['green','red'],[2,3]],
        [['magenta','green'],[5,6],['green','magenta'],['white',5],['yellow',2],['red',4],['blue',1],[1,'blue'],[2,'red'],[4,3],[6,'white'],[3,'yellow']],
        [['red','yellow'],[6,5],[5,'green'],['green','blue'],['white','magenta'],[4,3],[1,'white'],['blue',1],[3,6],[2,4],['yellow',2],['magenta','red']],
        [['green',3],['blue',2],[6,'white'],['magenta','blue'],[1,5],['yellow',4],[5,'magenta'],['white','red'],[4,6],[3,'yellow'],[2,'green'],['red',1]],
        [[5,1],['white',3],[4,5],[3,4],['yellow','white'],[1,'yellow'],['blue','green'],[6,2],['magenta',6],['green','red'],[2,'magenta'],['red','blue']],
        [['magenta',6],[6,'blue'],[1,'green'],[3,5],['white','red'],['blue',4],['green','magenta'],['red',1],[2,'white'],[5,2],[4,'yellow'],['yellow',3]],
        [['yellow','magenta'],['blue',1],[5,3],[2,'green'],[3,2],['red',5],[1,4],['white',6],[4,'white'],['green','red'],['magenta','yellow'],[6,'blue']],
        [[4,2],['red','blue'],['white',5],['yellow','magenta'],[2,'yellow'],[5,1],['blue','red'],['green',3],['magenta','green'],[3,6],[6,'white'],[1,4]],
        [['green','yellow'],[1,'red'],[5,4],[4,'green'],[3,'blue'],['magenta',6],[2,5],['yellow',2],['red',1],['white',3],['blue','white'],[6,'magenta']],
        [['green','blue'],['blue','green'],[1,5],['magenta',1],[3,'magenta'],['red',3],['yellow','white'],[6,'yellow'],[5,2],[4,6],['white','red'],[2,4]],
        [[2,'red'],['red','blue'],[5,'green'],['white',2],['yellow',1],[4,'yellow'],[3,5],[1,'magenta'],['blue','white'],['green',6],[6,4],['magenta',3]],
        [['red',4],['white',6],[3,2],[2,'white'],[4,'yellow'],[6,5],['blue','red'],[5,'green'],['yellow','blue'],['green','magenta'],['magenta',1],[1,3]],
        [[4,'blue'],['blue',3],[6,4],['white',1],['magenta','yellow'],['red',6],['green',5],['yellow','white'],[5,2],[2,'red'],[3,'green'],[1,'magenta']],
        [['blue',6],['magenta',3],[4,'blue'],[1,4],[2,5],['yellow',1],['green','yellow'],['red','white'],['white','green'],[5,2],[6,'magenta'],[3,'red']],
        [['magenta','red'],[2,'blue'],['white',5],[6,'yellow'],['blue',3],[4,2],['green',1],['yellow',6],[5,'green'],[3,'magenta'],['red','white'],[1,4]],
        [['yellow',1],[5,6],[1,'white'],['white',4],['blue','green'],['green',5],[4,'magenta'],[2,'blue'],[3,'red'],[6,3],['magenta',2],['red','yellow']],
        [[3,4],['white','blue'],['yellow','green'],[5,'magenta'],['red',1],['green','white'],[1,2],[6,'yellow'],['blue','red'],['magenta',6],[4,3],[2,5]],
        [[4,'green'],[6,5],['yellow',4],['green','blue'],[3,1],['magenta','yellow'],[5,3],[1,'magenta'],[2,'red'],['red',2],['blue','white'],['white',6]],
        [['yellow','blue'],['red',2],['white','red'],[5,3],[1,'white'],[3,5],['blue','magenta'],['green',4],[6,'yellow'],[4,'green'],[2,1],['magenta',6]],
        [['green','yellow'],[3,1],[5,'magenta'],['red',2],[6,'white'],['magenta','blue'],['yellow',6],[2,4],[4,'green'],['blue',5],[1,'red'],['white',3]]
    ]
    
    def __check(self, c):
        if not isinstance(c, list): raise TypeError("colorsequence must be in list")
        elif not all([isinstance(a, str) for a in c]): raise TypeError("Element of colorsequence must be in str")
        elif len(c)!=6: raise IndexError("Length of colorsequence must be 6")
        return [_colorcheck(a.lower()) for a in c]
    
    def __init__(self, edgework:edgework, colorsequence:list[str]):
        '''
        Initialize a new lightcycle instance

        Args:
            edgework (edgework): The edgework of the bomb
            colorsequence (list [str]): The color sequence from left to right in a list. Index 0 represents the leftmost color.
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__color = self.__check(colorsequence)
    
    def __swap(self, one, two):
        temp = self.__color[one]
        self.__color[one] = self.__color[two]
        self.__color[two] = temp

    def __calculate(self):
        snlist = [[self.sn[a], self.sn[-1-a]] for a in range(len(self.sn))]
        for a in range(len(snlist)): snlist[a] = self.__table[int(ord(snlist[a][0])-65) if snlist[a][0].isalpha() else int(snlist[a][0])+26][int(int(ord(snlist[a][1])-65)/3) if snlist[a][1].isalpha() else int((int(snlist[a][1])+26)/3)]
        for a in snlist:
            one = a[0]-1 if isinstance(a[0], int) else self.__color.index(a[0])
            two = a[1]-1 if isinstance(a[1], int) else self.__color.index(a[1])
            self.__swap(one, two)
        return tuple(self.__color)
    
    def solve(self):
        '''
        Solve the Light Cycle module

        Returns:
            tuple (str): The color sequence to submit. Index 0 represents the first to be submitted
        '''
        return self.__calculate()