from ..edgework import edgework
from ..images.zoo.image_loader import _loadimage

class zoo(edgework):
    __startinglist = {
        'gazelle': ['bear','v'],
        'caracal': ['spider','v'],
        'cheetah': ['pig','v'],
        'ocelot': ['cat','v'],
        'sheep': ['cow','v'],
        'caterpillar': ['tyrannosaurus rex','v'],
        'groundhog': ['rabbit','v'],
        'armadillo': ['horse','v'],
        'orca': ['flamingo','v'],
        'plesiosaur': ['flamingo','d'],
        'penguin': ['hyena','d'],
        'baboon': ['dimetrodon','d'],
        'whale': ['dromedary','d'],
        'squid': ['warthog','d'],
        'coyote': ['swallow','d'],
        'ram': ['starfish','d'],
        'deer': ['gorilla','d'],
        'crocodile': ['salamander','d']
    }
    __board = [
        ['','','','','cow','','','',''],
        ['','','','cat','','tyrannosaurus rex','','',''],
        ['','','pig','','bat','','rabbit','',''],
        ['','spider','','owl','','ant','','horse',''],
        ['bear','','goose','','rhinoceros','','fly','','flamingo'],
        ['','dragonfly','','snail','','tortoise','','llama',''],
        ['ferret','','butterfly','','monkey','','sea horse','','hyena'],
        ['','lion','','fox','','wolf','','camel',''],
        ['stegosaurus','','squirrel','','dolphin','','kangaroo','','dimetrodon'],
        ['','pterodactyl','','giraffle','','eagle','','lobster',''],
        ['elephant','','cobra','','koala','','porcupine','','dromedary'],
        ['','rooster','','hippopotamus','','crab','','otter',''],
        ['mouse','','woodpecker','','triceratops','','frog','','warthog'],
        ['','seal','','apatosaurus','','duck','','swallow',''],
        ['','','skunk','','beaver','','starfish','',''],
        ['','','','viper','','gorilla','','',''],
        ['','','','','salamander','','','','']
    ]
    
    def __check(self, a):
        if not isinstance(a, list): raise TypeError("animals must be in list")
        elif not all([isinstance(x, str) for x in a]): raise TypeError("Element of animals must be in str")
        elif len(a)!=2: raise IndexError("Length of animals must be 2")
        elif any([x.lower() not in self.__startinglist.keys() for x in a]): raise ValueError(f"One of the animals is invalid. Use showNames() to get the list of accepted animal names {[x for x in a if x.lower() not in self.__startinglist.keys()]}")
        return [b.lower() for b in a]
    
    def __init__(self, edgework:edgework, animals:list[str]|None=None):
        '''
        Initialize a new zoo instance

        Args:
            edgework (edgework): The edgework of the bomb
            animals (list [str]|None): List of animals in any order. This parameter can be None to get the list of accepted animal names first.
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        if animals is None: self.__animals = None
        else: self.__animals = self.__check(animals)
    
    def __calculate(self):
        starting_animals = {a:self.__startinglist.get(a)[0] for a in self.__animals}
        directions = {a:self.__startinglist.get(a)[1] for a in self.__animals}
        xy = {a:[] for a in self.__animals}

        for a in starting_animals:
            for x in self.__board:
                if starting_animals[a] in x:
                    xy[a] = ([self.__board.index(x), x.index(starting_animals[a])])
                    break
        
        for a in self.__animals:
            if directions[a] == 'v':
                starting_animals[a] = [self.__board[b][xy[a][1]] for b in range(len(self.__board)) if self.__board[b][xy[a][1]]!='']
            elif directions[a] == 'd':
                temp = []
                for b in range(len(self.__board)):
                    if self.__board[xy[a][0]-b][xy[a][1]-b]!='': temp.append(self.__board[xy[a][0]-b][xy[a][1]-b])
                    else: break
                starting_animals[a] = temp

        midpoint_animal = list(set(starting_animals[self.__animals[0]]).intersection(set(starting_animals[self.__animals[1]])))[0]
        midpoint_coord = []
        midpoint_direction = ''

        for a in self.__board:
            if midpoint_animal in a: midpoint_coord = [self.__board.index(a), a.index(midpoint_animal)]
        
        score = [[x for y in self.ports for x in y].count(a) for a in ['DVI-D','STEREO RCA','SERIAL','PS/2','RJ-45','PARALLEL']]
        dir_list = ['N','NE','SE','S','SW','NW']

        validity = ['','','','','','']
        for a in range(len(dir_list)):
            if dir_list[a]=='N' and midpoint_coord[0]-8>=0:
                midpoint_direction = 'N'; validity[a] = 'v'
            elif dir_list[a]=='S' and midpoint_coord[0]+8<len(self.__board):
                midpoint_direction = 'S'; validity[a] = 'v'
            elif dir_list[a]=='NE' and midpoint_coord[0]-4>=0 and midpoint_coord[1]+4<len(self.__board[0]): 
                midpoint_direction = 'NE'; validity[a] = 'v'
            elif dir_list[a]=='SE' and midpoint_coord[0]+4<len(self.__board) and midpoint_coord[1]+4<len(self.__board[0]): 
                midpoint_direction = 'SE'; validity[a] = 'v'
            elif dir_list[a]=='SW' and midpoint_coord[0]+4<len(self.__board) and midpoint_coord[1]-4>=0: 
                midpoint_direction = 'SW'; validity[a] = 'v'
            elif dir_list[a]=='NW' and midpoint_coord[0]-4>=0 and midpoint_coord[1]-4>=0: 
                midpoint_direction = 'NW'; validity[a] = 'v'
            else:
                validity[a] = 'd'
        
        score = [score[a] for a in range(len(dir_list)) if validity[a]=='v']
        dir_list = [dir_list[a] for a in range(len(dir_list)) if validity[a]=='v']
        flag = False

        for a in range(len(score)):
            if score.count(score[a])>=2: continue
            midpoint_direction = dir_list[a]
            flag = True

        if flag:
            all_coord = []
            for a in range(5):
                if midpoint_direction=='N': all_coord.append([midpoint_coord[0]-a,midpoint_coord[1]])
                elif midpoint_direction=='S': all_coord.append([midpoint_coord[0]+a,midpoint_coord[1]])
                elif midpoint_direction=='NE': all_coord.append([midpoint_coord[0]-a,midpoint_coord[1]+a])
                elif midpoint_direction=='SE': all_coord.append([midpoint_coord[0]+a,midpoint_coord[1]+a])
                elif midpoint_direction=='SW': all_coord.append([midpoint_coord[0]+a,midpoint_coord[1]-a])
                elif midpoint_direction=='NW': all_coord.append([midpoint_coord[0]-a,midpoint_coord[1]-a])
            all_animals = [self.__board[a[0]][a[1]] for a in all_coord]
            return all_animals
        else:
            all_coord = []; special_direction = ''
            if midpoint_coord[0]-8>=4 and midpoint_coord[1]+8<=8:
                special_direction = 'NE'
            elif midpoint_coord[0]+8<=12 and midpoint_coord[1]+8<=8: 
                special_direction = 'SE'
            elif midpoint_coord[0]+8<=12 and midpoint_coord[1]-8>=0:
                special_direction = 'SW'
            elif midpoint_coord[0]-8>=4 and midpoint_coord[1]-8>=0:
                special_direction = 'NW'
            elif midpoint_coord[0]-8>=4:
                special_direction = 'N'
            elif midpoint_coord[0]+8<=12:
                special_direction = 'S'
            
            for a in range(5):
                if special_direction=='N': all_coord.append([midpoint_coord[0]-(a*2),midpoint_coord[1]])
                elif special_direction=='S': all_coord.append([midpoint_coord[0]+(a*2),midpoint_coord[1]])
                elif special_direction=='NE': all_coord.append([midpoint_coord[0]-(a*2),midpoint_coord[1]+(a*2)])
                elif special_direction=='SE': all_coord.append([midpoint_coord[0]+(a*2),midpoint_coord[1]+(a*2)])
                elif special_direction=='SW': all_coord.append([midpoint_coord[0]+(a*2),midpoint_coord[1]-(a*2)])
                elif special_direction=='NW': all_coord.append([midpoint_coord[0]-(a*2),midpoint_coord[1]-(a*2)])
            
            all_animals = [self.__board[a[0]][a[1]] for a in all_coord]
            return all_animals
            

    def solve(self, showImages:bool=False):
        '''
        Solve the zoo module

        Args:
            showImages (bool): State if you want to show the images of the animals given by the answer
        
        Returns:
            tuple (str): The valid animals to press
        '''
        if self.__animals is None: raise TypeError("The 2 animals on the module has not bee set yet!")
        result = self.__calculate()
        if showImages:
            _loadimage(result)
        return result
    
    def showNames(self, images:bool=True):
        if images:
            _loadimage([a for a in self.__startinglist.keys()])
        else:
            return [a for a in self.__startinglist.keys()]