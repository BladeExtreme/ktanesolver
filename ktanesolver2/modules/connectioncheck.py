from ..edgework import edgework

class connectioncheck(edgework):
    def __check(self, n):
        if not isinstance(n, list): raise TypeError("numbers must be a list")
        elif not all(isinstance(a, list) for a in n): raise TypeError("Element of numbers must be a list")
        elif not all([isinstance(a, int) for b in n for a in b]): raise TypeError("Element of numbers' sub-lists must be int")
        elif len(n)!=4: raise IndexError("Length of numbers must be 4")
        elif not all(len(a)==2 for a in n): raise IndexError("Length of numbers' sub-lists must be 2")
        elif any([True if a<1 or a>8 else False for b in n for a in b]): raise ValueError("Numbers must be in range of 1-8")
        return n
    
    def __init__(self, edgework:edgework, numbers:list[list[int]]):
        '''
        Initialize a new connectioncheck instance

        Args:
            edgework (edgework): The edgework of the bomb
            numbers (list [list [int]]): The numbers that appears on the module. Each list represents a single connection. Therefore, there must be 4 sub-lists with each sub-lists only having 2 numbers
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__numbers = self.__check(numbers)
    
    def __calculate(self):
        table = [
            ['23','13','12','67','67','45','45',''],
            ['246','134','2','127','6','1578','468','67'],
            ['236','16','146','35678','467','12345','458','47'],
            ['27','17','48','38','67','57','1256','34'],
            ['23','147','157','2678','367','458','2345','46'],
            ['2368','146','14678','23567','478','1234','3458','1357'],
            ['248','1367','2467','135','468','2357','2368','157'],
            ['267','1378','2568','578','3467','1357','124568','2347']
        ]
        rowbook = ['7HPJ','34XYZ','SLIM','15BRO','20DGT','8CAKE','9QVN','6WUF']
        sn_char = ""
        open_numbers = [a for b in self.__numbers for a in b]

        if len(set([a for b in self.__numbers for a in b]))==len(self.__numbers): sn_char = self.sn[-1]
        elif open_numbers.count(1)>=2: sn_char = self.sn[0]
        elif open_numbers.count(7)>=2: sn_char = self.sn[-1]
        elif open_numbers.count(2)>=3: sn_char = self.sn[1]
        elif open_numbers.count(5)==0: sn_char = self.sn[4]
        elif open_numbers.count(8)==2: sn_char = self.sn[2]
        elif self.batt in range(1,6): sn_char = self.sn[self.batt-1]
        else: sn_char = self.sn[-1]
        row = rowbook.index([a for a in rowbook if sn_char in a][0])

        result = []
        for a in self.__numbers:
            if str(a[1]) in table[row][int(a[0])-1]: result.append(True)
            else: result.append(False)
        return result


    def solve(self):
        '''
        Solve the Connection Check module

        Returns:
            tuple [bool]: The state whether each connection is conencted or not. Index 0 represents the first connection corresponds to the numbers parameter list given during the initiliazation
        '''
        return tuple(self.__calculate())