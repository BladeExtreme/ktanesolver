import copy
from ..edgework import edgework

class mahjong(edgework):
    __tiles = [
        ["char 1", "bamboo 5", "wheel 5", "bamboo 8", "bamboo 2", "char 9", "red dragon", "bamboo 6", "bamboo 4", "wheel 4", "char 6", "char 2", "wheel 2", "char 3"],
        ["wheel 9", "wheel 1", "char 8", "wheel 7", "bamboo 9", "bamboo 7", "char 7", "white dragon", "char 4", "bamboo 3", "wheel 8", "wheel 3", "wheel 6", "char 5"]
    ]
    __counting_row = [
	    "bamboo 1","plum","orchid","chrysanthemum","bamboo","spring","summer","fall","winter","north","east","south","west","green dragon",
    ]

    def __check(self, s):
        if not isinstance(s, str): raise TypeError("shape must be in str")
        elif s.lower() not in ["bamboo", "bamboo 1", "1", "one", "green" "plum", "orchid", "chrysanthemum", "spring", "summer", "fall", "autumn", "winter", "winter", "north", "east", "south", "west", "green dragon"]: raise ValueError("This shape cannot be found in list. Use showNames()")
        return s.lower(), False

    def __init__(self, edgework:edgework, shape:str):
        '''
        Initialize a new mahjong instance

        Args:
            edgework (edgework): The edgework of the bomb
            shape (str): The shape of the tile that appears on the bottom left of the module. The accepted values can be see using '.showNames()'
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__shape, self.__flag = self.__check(shape)

    
    def __calculate(self):
        swaps = []; tiles = copy.deepcopy(self.__tiles)
        for a in range(len(self.sn)):
            if self.sn[a].isdigit():
                swaps.append(int(self.sn[a]))
            else:
                swaps.append((ord(self.sn[a].upper())-ord('A')+10)%14 if (ord(self.sn[a].upper())-ord('A')+10)>=14 else ord(self.sn[a].upper())-ord('A')+10)
            if len(swaps)==2:
                temp = tiles[0][swaps[0]]
                tiles[0][swaps[0]] = tiles[1][swaps[1]]
                tiles[1][swaps[1]] = temp
                swaps = []
        if self.__shape == "autumn": self.__shape = "fall"
        if self.__shape == "green": self.__shape = "green dragon"
        if self.__shape == "one" or self.__shape == "1": self.__shape = "bamboo 1"
        
        offset = -1*self.__counting_row.index(self.__shape)

        tiles[1] = tiles[1][offset:] + tiles[1][:offset]; temp = {}
        for a in [[tiles[0], tiles[1]], [tiles[1], tiles[0]]]:
            for b in range(len(a[0])): temp[a[0][b]] = a[1][b]
        self.__flag = True
        return temp


    def solve(self):
        '''
        Solve the Mahjong module

        Returns:
            dict (str|str): The dict of tiles with similar likeness. Keys and Values rotate each other, meaning a key will be a value once and vice versa
        '''
        if not self.__flag: result = self.__calculate()
        return result

    def showNames(self):
        '''
        Show all of the accepted names for the parameter shape.

        Returns:
            None
        '''
        text = [
            "Bamboo [1/One]: The tile with the red bird",
            "Plum: The tile with the pink flower",
            "Orchid: The tile with the purple flower",
            "Chrysanthemum: The tile with the yellow/gold flower",
            "Bamboo: The tile with the bamboo itself",
            "Spring: The tile with the green plant and an orange butterfly",
            "Summer: The tile with the big sun",
            "Fall/Autumn: The tile with two orange maple leaves",
            "Winter: The tile with two snowflakes",
            "North: The tile with the chinese character 北",
            "East: The tile with the chinese character 東",
            "South: The tile with the chinese character 南",
            "West: The tile with the chinese character 西",
            "[Green] Dragon: The tile with the green chinese character 發",
        ]
        print("Names that has the [] are names that is also possible to be submitted. In the case of 'Fall', you can also submit it as 'Autumn'")
        for a in text:
            print(a)