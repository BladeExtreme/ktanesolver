import copy
from ..edgework import edgework

class mazematics(edgework):
    __maze = [
        [['hexagon', 1], ['star', 1], ['dt', 2], ['square', 2], ['circle', 1], ['diamond', 1], ['ut', 2], ['heart', 2]],
        [['ut', 2], ['heart', 1], ['diamond', 2], ['circle', 2], ['dt', 1], ['square', 1], ['hexagon', 2], ['star', 1]],
        [['star', 1], ['ut', 2], ['square', 1], ['dt', 1], ['diamond', 2], ['circle', 2], ['heart', 1], ['hexagon', 2]],
        [['heart', 1], ['hexagon', 2], ['circle', 2], ['diamond', 1], ['star', 2], ['dt', 1], ['square', 1], ['ut', 2]],
        [['dt', 2], ['square', 1], ['star', 1], ['heart', 2], ['ut', 1], ['hexagon', 2], ['diamond', 2], ['circle', 1]],
        [['diamond', 2], ['circle', 1], ['hexagon', 2], ['ut', 1], ['heart', 2], ['star', 2], ['dt', 1], ['square', 1]],
        [['circle', 1], ['diamond', 2], ['heart', 1], ['hexagon', 1], ['square', 2], ['ut', 1], ['star', 2], ['dt', 2]],
        [['square', 2], ['dt', 2], ['ut', 1], ['star', 2], ['hexagon', 1], ['heart', 2], ['circle', 1], ['diamond', 1]]
    ]
    
    def __check(self,i,c,v,d):
        shapes = ["circle", "diamond", "down triangle", "dt", "heart", "hexagon", "square", "star", "up triangle", "ut"]
        if not isinstance(i,int): raise TypeError("initial_value must be in int")
        elif not isinstance(c, list): raise TypeError("cycle must be in list")
        elif not all([isinstance(a, (int, str)) for a in c]): raise TypeError("Element of cycle must be in int or str")
        elif len([a for a in c if isinstance(a, int)])!=2: raise IndexError("Length of cycle whose type is int must be 2. To represent, goal and modified")
        elif not isinstance(c[0], int): raise TypeError("Element of cycle must be in int on index 0, since it represents the goal")
        elif not isinstance(v, int): raise TypeError("value_after_move must be in int")
        elif abs(v-i)<1 or abs(v-i)>9: raise ValueError("value_after_move must be in range 1-9 subtracted from or added to initial_value")
        elif not isinstance(d, str): raise TypeError("direction_move must be in str")
        elif d.lower() not in ["up", "down", "left", "right", "u", "d", "l", "r"]: raise ValueError("direction_move must be in ['up', 'down', 'left', 'right', 'u', 'd', 'l', 'r']")

        s = [a for a in c if isinstance(a, str)]; target = c[0]; modified = [c[a] for a in range(len(c)) if isinstance(c[a], int) and a!=0][0]
        if not all([a.lower() in shapes for a in s]): raise ValueError(f"Element of cycle must be in shapes. Accepted shapes are: {shapes}")
        
        d = d[0].lower()

        s_d = {}
        for a in range(len(c)):
            if isinstance(c[a], str):
                if c[a].lower()=="down triangle": c[a] = "dt"
                elif c[a].lower()=="up triangle": c[a] = "ut"
                s_d[c[a].lower()] = a
        
        return i, s_d, target, modified, v, d

    
    def __init__(self, edgework:edgework, initial_value:int, cycle:list[int|str], value_after_move:int, direction_move:str):
        '''
        Initialize a new mazematics instance

        Args:
            edgework (edgework): The edgework of the bomb
            initial_value (int): The initial value that appears on the screen before the cycle starts
            cycle (list [int|str]): The list of shapes and numbers that appears on the module. Shapes must be in str, while numbers must be int. Accepted shapes are: ["circle", "diamond", "down triangle", "dt", "heart", "hexagon", "square", "star", "up triangle", "ut"]. NOTE: This module assumes index 0 is the item that displayed when the timer's second is 0. (Meaning: index 1 = item when second is 1, index 2 = item when second is 2 and so on.)
            value_after_move (int): The new value of the modified number after moving
            direction_move (str): The direction you move for the very first time. NOTE: This parameter only accepts ["up", "down", "left", "right", "u", "d", "l", "r"]
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__value, self.__shapes, self.__target, self.__modified, self.__modified2, self.__direction = self.__check(initial_value, cycle, value_after_move, direction_move)

    def __find_final_coord(self, grid, initial_coord):
        move_col = 1 if self.__direction=='r' else -1 if self.__direction=='l' else 0
        move_row = 1 if self.__direction=='d' else -1 if self.__direction=='u' else 0

        for a in initial_coord:
            if grid[(a[0]+move_row)%8 if a[0]+move_row>=8 else a[0]+move_row][(a[1]+move_col)%8 if a[1]+move_col>=8 else a[1]+move_col]+self.__modified == self.__modified2:
                return [a[0], a[1]], [(a[0]+move_row)%8 if a[0]+move_row>=8 else a[0]+move_row, (a[1]+move_col)%8 if a[1]+move_col>=8 else a[1]+move_col]
        
    def __restriction(self, initial_coord):
        if self.__maze[initial_coord[0]][initial_coord[1]][0] in ["square", "diamond"]:
            def triangular(n): return n in [1, 3, 6, 10, 15, 21, 28, 36, 45]
            return triangular
        elif self.__value%3==0:
            def multipleof7(n): return n%7==0
            return multipleof7
        elif self.__maze[initial_coord[0]][initial_coord[1]][1]==1:
            def primenumber(n): return n in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
            return primenumber
        else:
            def is_fibonacci(n): return n in [1, 2, 3, 5, 8, 13, 21, 34]
            return is_fibonacci

    def __calculate(self, threshold):
        grid = copy.deepcopy(self.__maze)
        for a in range(len(grid)):
            for b in range(len(grid[a])):
                grid[a][b] = self.__shapes.get(grid[a][b][0])*(1 if grid[a][b][1]==1 else -1)
        
        initial_coord = []
        for a in range(len(grid)):
            for b in range(len(grid[a])):
                if (self.__value+grid[a][b])==self.__modified:
                    initial_coord.append([a,b])
        initial_coord, current_coord = self.__find_final_coord(grid, initial_coord)

        restriction = self.__restriction(initial_coord)
        return self.__bfs(grid, [[current_coord, [], self.__modified2]], restriction, threshold)

    def __bfs(self, grid, queue, restriction, threshold):
        while queue:
            current_coord, path, current_value = queue.pop(0)
            neighbors = [a for a in 'urdl']
            evaluate = []

            if current_value==self.__target: return path
    
            for a in neighbors:
                new_coord = []; new_path = copy.deepcopy(path); new_path.append(a)
                if a=='u': new_coord = [current_coord[0]-1, current_coord[1]]
                elif a=='r': new_coord = [current_coord[0], (current_coord[1]+1)%8]
                elif a=='d': new_coord = [(current_coord[0]+1)%8, current_coord[1]]
                elif a=='l': new_coord = [current_coord[0], current_coord[1]-1]
                new_value = current_value+grid[new_coord[0]][new_coord[1]]
                if (restriction(new_value) and self.__target!=new_value) or new_value>49 or new_value<0:
                    continue
                else:
                    evaluate.append([new_coord, new_path, new_value])
            for a in [a for a in sorted(evaluate, key=lambda x: x[-1]) if abs(a[-1]-self.__target)<=threshold]:
                queue.append(a)

    def solve(self, threshold:int=10):
        '''
        Solve the Mazematics module

        Args:
            threshold (int): This parameter is used as a threshold to take all neighbors whose gap between the current value and the value if the neighbor's operation is taken is below or equal to thershold. By default, this value is 10.

        Returns:
            list [str]: The direction should be taken from the current value (the value AFTER the first move)
        '''
        if not isinstance(threshold, int): raise TypeError("Threshold must be int")
        elif threshold<=0: raise ValueError("Threshold value must be above 0")
        result = self.__calculate(threshold); result_dir = []
        for a in result:
            result_dir.append("UP" if a=='u' else "DOWN" if a=='d' else "LEFT" if a=='l' else "RIGHT")
        return result_dir