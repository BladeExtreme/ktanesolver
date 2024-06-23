from ..edgework import edgework

class icecream(edgework):
    __allergytable = {
        'adam': [[3,4,1],[3,6,2],[0,2,1],[2,4,7],[8,5,6]],
        'ashley': [[6,2,5],[4,1,7],[0,8,2],[1,2,6],[3,6,7]],
        'bob': [[5,6,8],[2,1,0],[4,8,2],[4,2,5],[0,5,1]],
        'cheryl': [[1,6,3],[7,5,2],[1,4,5],[4,2,0],[3,7,5]],
        'dave': [[2,6,7],[0,1,4],[8,2,3],[7,8,1],[5,7,3]],
        'gary': [[1,2,5],[6,8,0],[3,2,1],[7,4,5],[1,8,4]],
        'george': [[8,1,2],[6,4,8],[0,4,3],[1,6,4],[3,2,5]],
        'jacob': [[7,3,2],[1,5,6],[5,4,7],[3,4,0],[6,2,1]],
        'jade': [[3,7,1],[0,8,2],[7,1,3],[6,7,8],[4,5,1]],
        'jessica': [[4,2,6],[1,2,3],[0,3,4],[6,5,0],[4,7,8]],
        'mike': [[1,5,0],[6,8,3],[0,7,1],[4,3,2],[3,6,1]],
        'pat': [[5,6,2],[1,3,6],[3,4,7],[2,0,5],[8,1,3]],
        'sally': [[4,6,3],[1,0,2],[6,7,4],[2,5,8],[0,3,1]],
        'sam': [[2,4,1],[7,8,0],[3,4,6],[1,0,3],[6,5,2]],
        'sean': [[4,6,1],[2,3,6],[1,5,7],[6,8,2],[2,7,4]],
        'simon': [[0,3,5],[1,6,4],[5,4,8],[2,0,7],[7,3,6]],
        'taylor': [[6,3,5],[5,1,2],[4,2,6],[7,1,0],[3,7,2]],
        'tim': [[0,8,3],[2,1,4],[4,3,5],[2,6,7],[1,4,3]],
        'tom': [[8,4,5],[1,6,7],[2,5,6],[3,7,5],[3,6,1]],
        'victor': [[0,3,1],[2,5,7],[3,4,6],[6,7,1],[5,3,0]]
    }    
    __flavors = {
        tuple(sorted(['fruit','tutti','frutti','tutti frutti'])): 'tutti frutti',
        tuple(sorted(['rocky','rock','rocky road'])): 'rocky road',
        tuple(sorted(['rasp','raspberry','raspberry ripple'])): 'raspberry ripple',
        tuple(sorted(['choc', 'chocolate', 'double chocolate'])): 'doublel chocolate',
        tuple(sorted(['straw', 'strawberry', 'double strawberry'])): 'double strawberry',
        tuple(sorted(['c&c', 'cnc', 'cookie', 'cookies and cream'])): 'cookies and cream',
        tuple(sorted(['nea', 'neapolitan'])): 'neapolitan',
        tuple(sorted(['mint', 'mint choc', 'mint chocolate chip'])): 'mint chocolate chip',
        tuple(sorted(['classic', 'the classic'])): 'the classic',
        tuple(sorted(['vanilla'])): 'vanilla'
    }
    __recipes = {
        'tutti frutti': [1,2,7], 'rocky road': [0,3,8], 'raspberry ripple': [2,9], 'double chocolate': [0,9], 'double strawberry': [1,9], 'cookies and cream': [4,9], 'neapolitan': [1,0,9], 'mint chocolate chip': [5,0,9], 'the classic': [0,7,9], 'vanilla': []
    }
    __priorityrow = [
        [5, 6, 0, 8, 1, 3, 7, 4, 2, 9],
        [3, 7, 6, 1, 0, 4, 5, 2, 8, 9],
        [6, 0, 5, 2, 4, 7, 3, 8, 1, 9],
        [4, 5, 1, 8, 6, 3, 0, 2, 7, 9]
    ]
    
    def __check(self, c, m):
        if not isinstance(c, str): raise TypeError("customer must be in str")
        elif not isinstance(m, list): raise TypeError("menulist must be in list")
        elif not all([isinstance(a, str) for a in m]): raise TypeError("Element of menulist must be in str")
        elif len([a for a in m if a.lower()!='vanilla'])!=4: raise IndexError("Length of menulist must be 4 (or 5 if you include 'vanilla')")
        for a in range(len(m)):
            for b in self.__flavors:
                if m[a].lower() in b: m[a] = self.__flavors[b]
        if 'vanilla' not in m: m.append('vanilla')
        return c.lower(), m
    
    def __init__(self, edgework:edgework, customer:str, menulist:list[str]):
        '''
        Initialize a new icecream instance

        Args:
            edgework (edgework): The edgework of the bomb
            
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__customer, self.__menu = self.__check(customer, menulist)
    
    def __calculate(self):
        priorityrow = 0 if len(self._litind) > len(self._unlitind) else 1 if '' in self.ports else 2 if self.batt >= 3 else 4
        allergy = self.__allergytable[self.__customer][int(int(self._sndigit[-1])/2) if int(self._sndigit[-1])%2==0 else int((int(self._sndigit[-1])-1)/2)]
        goodcream = [a for a in self.__menu if not any([b in self.__recipes[a] for b in allergy])]
        if len(goodcream)>=2:
            for a in self.__priorityrow[priorityrow]:
                if list(self.__recipes)[a] in goodcream: goodcream = list(self.__recipes)[a]; break
        else: goodcream = goodcream[0]
        return goodcream

    def solve(self, customer:str|None=None, menulist:list[str]|None=None):
        '''
        Solve the Ice Cream modue

        Args:
            customer (str|None): The name of the customer. By default is None
            menulist (list [str]|None): The list of all ice creams that is an option to the customer. By defualt is None
        Returns:
            str: The correct ice cream to be given
        '''
        return self.__calculate()