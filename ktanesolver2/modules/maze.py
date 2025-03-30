from ..edgework import edgework #type: ignore

class maze(edgework):
    __mazes = [
        [['14', '13', '12', '14', '13', '123'],
         ['24', '14', '23', '34', '13', '12'],
         ['24', '34', '12', '14', '13', '2'],
         ['24', '134', '3', '23', '134', '2'],
         ['4', '13', '12', '14', '123', '24'],
         ['34', '123', '34', '23', '134', '23']
        ],
        [['134', '1', '123', '14', '1', '123'],
         ['14', '23', '14', '23', '34', '12'],
         ['24', '14', '23', '14', '13', '2'],
         ['4', '23', '14', '23', '124', '24'],
         ['24', '124', '24', '14', '23', '24'],
         ['234', '34', '23', '34', '13', '23']
        ],
        [['14', '13', '12', '124', '14', '12'],
         ['234', '124', '24', '34', '23', '24'],
         ['14', '2', '24', '14', '12', '24'],
         ['24', '24', '24', '24', '24', '24'],
         ['24', '34', '23', '24', '24', '24'],
         ['34', '13', '13', '23', '34', '23']
        ],
        [['14', '12', '134', '13', '13', '12'],
         ['24', '24', '14', '13', '13', '2'],
         ['24', '34', '23', '14', '123', '24'],
         ['24', '134', '13', '3', '13', '2'],
         ['4', '13', '13', '13', '12', '24'],
         ['34', '13', '123', '134', '23', '234']
        ],
        [['134', '13', '13', '13', '1', '12'],
         ['14', '13', '13', '1', '23', '234'],
         ['4', '12', '134', '23', '14', '12'],
         ['24', '34', '13', '12', '234', '24'],
         ['24', '14', '13', '3', '123', '24'],
         ['234', '34', '13', '13', '13', '23']
        ],
        [['124', '14', '12', '134', '1', '12'],
         ['24', '24', '24', '14', '23', '24'],
         ['4', '23', '234', '24', '14', '23'],
         ['34', '12', '14', '2', '24', '124'],
         ['14', '23', '234', '24', '34', '2'],
         ['34', '13', '13', '23', '134', '23']
        ],
        [['14', '13', '13', '12', '14', '12'],
         ['24', '14', '123', '34', '23', '24'],
         ['34', '23', '14', '123', '14', '23'],
         ['14', '12', '4', '13', '23', '124'],
         ['24', '234', '34', '13', '12', '24'],
         ['34', '13', '13', '13', '3', '23']
        ],
        [['124', '14', '13', '12', '14', '12'],
         ['4', '3', '123', '34', '23', '24'],
         ['24', '14', '13', '13', '12', '24'],
         ['24', '34', '12', '134', '3', '23'],
         ['24', '124', '34', '13', '13', '123'],
         ['34', '3', '13', '13', '13', '123']
        ],
        [['124', '14', '13', '13', '1', '12'],
         ['24', '24', '14', '123', '24', '24'],
         ['4', '3', '23', '14', '23', '24'],
         ['24', '124', '14', '23', '134', '2'],
         ['24', '24', '24', '14', '12', '24'],
         ['34', '23', '34', '23', '34', '23']
        ]
    ]
    
    def __init__(self, edgework, maze: tuple[str], player: str, target: str):
        '''
        Initialize a new maze instance

        Args:
            edgework (edgework): The edgework of the bomb
            maze (tuple [str]): The coordinate of the maze indicator. The tuple must have 2 index. Column is the letters (A-F) and the rows are the numbers (1-6)
            player (str): The coordinate of the player. Column is the letters (A-F) and the rows are the numbers (1-6)
            target (str): The coordinate of the target. Column is the letters (A-F) and the rows are the numbers (1-6)
        '''
        super().__init__(edgework.batt, edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__maze, self.__player, self.__target = self.__check(tuple([a.upper() for a in maze]), player.upper(), target.upper())
    
    def __check(self, m, p, t):
        if not isinstance(m, tuple): raise TypeError("Maze's coordinaate is not in the correct type")
        elif not isinstance(p, str): raise TypeError("Player's coordinate is not in the correct type")
        elif not isinstance(t, str): raise TypeError("Target's coordinate is not in the correct type")
        elif len(m) != 2 and all([True if len(a)==2 else False for a in m]): raise IndexError("Maze's coordinate is incomplete")
        elif len(p) != 2 and p[0] not in "ABCDEF" and p[1] not in "123456": raise IndexError("Player's coordinate is incomplete")
        elif len(t) != 2 and t[0] not in "ABCDEF" and p[1] not in "123456": raise IndexError("Target's coordinate is incomplete")
        elif not p[0].isalpha() or not t[0].isalpha(): raise ValueError("Coordinaation must be column first (letters) then rows (numbers)")
        else: return m,p,t
    
    def showModule(self):
        return 'Maze'

    def __calculatecoord(self):
        coords = [
            ['A2', 'F3'],
            ['B4', 'E2'],
            ['D4', 'F4'],
            ['A1', 'A4'],
            ['D6', 'E3'],
            ['C5', 'E1'],
            ['B1', 'B6'],
            ['C4', 'D1'],
            ['A5', 'C2']
        ]
        c=-1
        for a in range(len(coords)):
            if all([b in self.__maze for b in coords[a]]): c=a; break
        xp, yp = ord(self.__player[0]) - ord('A'), int(self.__player[1])-1
        xt, yt = ord(self.__target[0]) - ord('A'), int(self.__target[1])-1
        return c, [xp, yp], [xt, yt]

    def __calculate(self, maze, p, t):
        def queue(q, x, y, vis, o, d):
            if '1' not in maze[y][x] and [x,y-1] not in vis: q.append([x,y-1]), o.append([x, y]), d.append('UP')
            if '2' not in maze[y][x] and [x+1,y] not in vis: q.append([x+1,y]), o.append([x, y]), d.append('RIGHT')
            if '3' not in maze[y][x] and [x,y+1] not in vis: q.append([x,y+1]), o.append([x, y]), d.append('DOWN')
            if '4' not in maze[y][x] and [x-1,y] not in vis: q.append([x-1,y]), o.append([x, y]), d.append('LEFT')
            return q, o, d
        
        q = []; vis = [p]; o = []; d = []
        x = p[0]; y = p[1]
        q, o, d = queue(q, x, y, vis, o, d)
        qdx = 0

        while q:
            x = q[qdx][0]; y = q[qdx][1]; vis.append([x, y])
            q, o, d = queue(q, x, y, vis, o, d)
            if t in vis: break
            qdx += 1

        idx = [[t, '']]
        while idx[0][0] != p:
            idx.insert(0, [o[q.index(idx[0][0])], d[q.index(idx[0][0])]])
        
        return [a[1] for a in idx][0:-1]

    def solve(self):
        c, p, t = self.__calculatecoord()
        arr = self.__calculate(self.__mazes[c], p, t)
        return arr
