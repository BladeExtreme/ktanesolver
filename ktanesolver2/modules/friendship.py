from ..edgework import edgework

class friendship(edgework):
    __coldesc = {
        'amethyst star': 0, 'apple cinnamon': 1, 'apple fritter': 2, 'babs seed': 3, 'berryshine': 4, 'big mcintosh': 5, 'bulk biceps': 6, 'candace': 7, 'golden harvest': 8, 'celestia': 9, 'cheerilee': 10, 'cheese sandwich': 11, 'cherry jubilee': 12, 'coco pommel': 13,
        'starlight glimmer': 0, 'spoiled rich': 1, 'silverstar': 2, 'silver spoon': 3, 'silver shill': 4, 'shining armor': 5, 'screwball': 6, 'rose': 7, 'octavia melody': 8, 'nurse redheart': 9, 'night light': 10, 'ms. harshwhinny': 11, 'moon dancer': 12, 'mayor mare': 13
    }
    __rowdesc = {
        'coloratura': 0, 'daisy': 1, 'daring do': 2, 'derpy': 3, 'diamond tiara': 4, 'double diamond': 5, 'filty rich': 6, 'granny smith': 7, 'hoity toity': 8, 'lightning dust': 9, 'lily': 10, 'luna': 11, 'lyra': 12, 'maud pie': 13,
        'vinyl scratch': 0, 'twist': 1, 'twilight velvet': 2, 'trouble shoes': 3, 'trixie': 4, 'trenderhoof': 5, 'tree hugger': 6, 'toe tapper': 7, 'time turner': 8, 'thunderlane': 9, 'sweetie drops': 10, 'suri polomare': 11, 'sunset shimmer': 12, 'sunburst': 13
    }
    __colexplanation = {
        'amethyst star': '3 diamonds, magenta background', 'apple cinnamon': 'green apple and a cinnamon, dark red background', 'apple fritter': '3 cracker/fritters, yellow background', 'babs seed': 'scissor with red handle', 'berryshine': 'grape and apple', 'big mcintosh': 'half green apple, red background', 'bulk biceps': 'dumbell', 'candace': 'blue diamond heart, magenta background', 'golden harvest': 'three carrots, yellow background', 'celestia': 'orange sun with 8 spiral rays', 'cheerilee': 'three flower with white petals', 'cheese sandwich': 'bread being half torned in the middle, with cheese in the middle', 'cherry jubilee': 'two cherry', 'coco pommel': 'purple hat with red feather on its back',
        'starlight glimmer': 'purple diamond with two turquoise tails, magenta background', 'spoiled rich': 'yellow ring with diamond on top, pink background', 'silverstar': 'a silver star', 'silver spoon': 'silver spoon, heading down', 'silver shill': 'two circular silver object with a white line going down in the middle of those objects', 'shining armor': 'black and magenta shield wwith three blue starts above it', 'screwball': 'a purple screw with white baseball, magenta background', 'rose': 'a rose flower', 'octavia melody': 'purple music clef with gray background', 'nurse redheart': 'giant red cross with hearts on each diagonal sides', 'night light': 'white crescent moon inside a yellow crescent moon', 'ms. harshwhinny': 'a golden trophy', 'moon dancer': 'dark purple moon with 3 purple stars around it', 'mayor mare': 'a rolled-up scroll, tied with a dark blue ribbon'
    }
    __rowexplanation = {
        'coloratura': '5 colorful music notes (orange, red, purple, dark turquoise, green) with a golden star on the middle', 'daisy': '2 flowers with 5 white round petals', 'daring do': 'a golden 4-point star shaped like a compass', 'derpy': '7 white bubbles with 2 of them larger than the average, gray background', 'diamond tiara': 'a purple crown, magenta background', 'double diamond': '3 blue snowflakes, white background', 'filty rich': '3 money bags with $ sign in the bags', 'granny smith': 'an apple pie, lime background', 'hoity toity': 'a yellow handheld folding fan, on a pale blue background', 'lightning dust': 'white lightning with 3 yellow stars below it, light turquoise background', 'lily': '3 flower with 5 white sharp petals', 'luna': 'white crescent moon, taking massive portion of the image', 'lyra': 'golden harp, light turquoise background', 'maud pie': 'a rock that is shaped somewhat like a diamond and a lighter side is on the upper side of the rock, gray background',
        'vinyl scratch': 'a black beamed eight note (2 music notes being connected with a line above)', 'twist': '2 pink candy canes forming a heart-like shape', 'twilight velvet': '3 dark purple star', 'trouble shoes': 'a green horse shoe, brown background', 'trixie': 'a blue crescent-like shape behind a light blue star on a stick', 'trenderhoof': '2 orange diamonds behind 2 crossing lines making an X shape on each diamond and forming a third diamond on the middle', 'tree hugger': 'a tree with dark brown wood and red leaves with the leaves making a heart shape', 'toe tapper': '5 white music notes making a star shape', 'time turner': 'a yellow sand hourglass', 'thunderlane': 'a gray cloud with a yellow lightning below the cloud', 'sweetie drops': '3 light blue and yellow candies', 'suri polomare': '3 clothing buttons with 4 circles inside it, topmost is pale yellow, then light blue, then purple', 'sunset shimmer': 'a sun with 8 swirly rays. The sun has two colors, red and yellow forming like a yin-yang orb', 'sunburst': 'a sun with 4 rays and 6 stars. 4 stars are dark turquoise and the other 2 is light cyan'
    }
    
    def __check(self, g):
        if not isinstance(g, list): raise TypeError("grid must be in list")
        elif not all([isinstance(a, list) for a in g]): raise TypeError("Each element of grid must contain a list")
        elif not all([len(a)==min([len(b) for b in g]) for a in g]): raise IndexError("Length of sublists' columns must be consistent")
        elif not all([all([isinstance(b, str) if b!=0 and b!=None else b==0 if b!=None else b==None for b in a] for a in g)]): raise TypeError("Type of each element in sublists must be str for non-empty spaces. Empty space can use '', 0 or None")
        elif not all([all([(b in self.__coldesc or b in self.__rowdesc) for b in a if b!=0 and b!=None and b!='']) for a in g]): raise ValueError("This name cannot be found in the stored list. Use showNames() for names")
        return [[b.lower() if b!=0 and b!=None else '' for b in a] for a in g]
    
    def __init__(self, edgework:edgework, grid:list[list]|None=None):
        '''
        Initialize a new friendship instance

        Args:
            edgework (edgework): The edgework of the bomb
            grid (list (list (str))): The approximate grid that appears on the module. Empty space can be filled with None, 0 or ''.
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        if grid is not None:
            self.__grid = self.__check(grid)
    
    def showNames(self):
        '''
        Show the names of the symbols along with its description of the symbols

        Return:
            list (dict): The keys are the name of the symbols, while the values are the description of that said symbols
        '''
        return sorted([{a: b} for a,b in self.__colexplanation.items()]+[{a: b} for a,b in self.__rowexplanation.items()], key=lambda x: x.keys())

    def __rotate(self, n):
        return [list(a)[::-1] for a in list(zip(*n[::-1]))]

    def __calculate(self):
        table = [
            ['J', 'G', 'U', 'K', 'V', '8', 'L', 'C', 'H', '4', 'W', 'P', 'M', 'R'],
            ['7', 'S', '8', 'U', 'N', 'J', '9', 'Y', 'F', 'P', 'Q', 'C', 'R', '4'],
            ['Q', 'R', 'H', '4', 'F', '7', 'J', 'E', '8', 'T', 'N', '9', 'A', 'X'],
            ['D', '3', 'S', 'H', 'U', 'E', 'T', 'P', 'V', 'J', 'L', 'A', '4', '7'],
            ['A', 'F', '3', 'T', 'M', 'P', 'R', 'W', 'S', 'X', 'U', 'N', 'G', 'B'],
            ['V', 'K', 'G', 'P', 'Q', 'D', 'U', 'L', '3', 'H', 'M', 'R', 'E', 'C'],
            ['4', '9', 'T', 'F', 'B', 'X', 'D', 'U', 'Y', '3', 'R', 'L', 'H', 'M'],
            ['G', '4', '9', 'J', '8', '3', 'X', 'K', 'A', 'Y', 'S', 'W', '7', 'D'],
            ['K', 'T', 'F', 'B', 'J', 'Q', '3', 'S', 'E', 'C', 'P', 'U', 'W', 'L'],
            ['S', 'M', 'A', 'C', '7', 'H', 'E', 'B', 'G', 'F', 'V', 'X', 'L', 'N'],
            ['8', '7', 'V', 'L', '9', 'R', 'K', 'D', 'T', 'Q', 'B', 'Y', 'X', 'A'],
            ['W', '8', '4', 'Q', 'G', 'Y', 'V', 'T', '7', 'N', '3', 'B', 'C', 'P'],
            ['M', 'A', 'W', '9', 'H', 'K', 'Y', 'J', 'N', 'D', 'X', 'E', '8', 'F'],
            ['Y', 'N', 'B', 'G', 'W', 'S', 'M', 'Q', 'K', '9', 'C', 'V', 'D', 'E']
        ]
        definition = {
            'A': 'Altruism', 'B': 'Amicability', 'C': 'Authenticity', 'D': 'Benevolence', 'E': 'Caring', 'F': 'Charitableness',
            'G': 'Compassion', 'H': 'Conscientiousness', 'J': 'Consideration', 'K': 'Courage', 'L': 'Fairness', 'M': 'Flexibility',
            'N': 'Generosity', 'P': 'Helpfulness', 'Q': 'Honesty', 'R': 'Inspiration', 'S': 'Kindness', 'T': 'Laughter',
            'U': 'Loyalty', 'V': 'Open-mindedness', 'W': 'Patience', 'X': 'Resoluteness', 'Y': 'Selflessness', '3': 'Sincerity',
            '4': 'Solidarity', '7': 'Support', '8': 'Sympathy', '9': 'Thoughtfulness'
        }
        row = [a for b in self.__grid for a in b if a!='' and a in self.__rowdesc]; col = [a for b in self.__grid for a in b if a!='' and a in self.__coldesc]
        colonlygrid = self.__rotate([[b if b not in row else '' for b in a] for a in self.__grid])
        rowonlygrid = [[b if b not in col else '' for b in a] for a in self.__grid]

        for a in colonlygrid:
            if len([b for b in a if b!=''])==1:
                self.__grid = [[x if x!=[b for b in a if b!=''][0] else '' for x in y] for y in self.__grid]
                break
        for a in rowonlygrid:
            if len([b for b in a if b!=''])==1:
                self.__grid = [[x if x!=[b for b in a if b!=''][0] else '' for x in y] for y in self.__grid]
                break
        row = [self.__rowdesc[a] for b in self.__grid for a in b if a!='' and a in self.__rowdesc]; col = [self.__coldesc[a] for b in self.__grid for a in b if a!='' and a in self.__coldesc]
        validnumbers = []
        for a in row:
            for b in col:
                validnumbers.append(definition[table[a][b]])
        return validnumbers

    def solve(self):
        '''
        Solve the Friendship module

        Returns:
            tuple (str): The possible words to be submitted onto the module.
        '''
        return tuple(self.__calculate())