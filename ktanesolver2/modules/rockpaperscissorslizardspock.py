from ..edgework import edgework

class rpslsp(edgework):
    def __check(self, d):
        if not isinstance(d, str) and not None: raise TypeError("decoy must be in str or None")
        if d is None: return 6
        else:
            if d.lower() not in ['rock', 'paper', 'scissors', 'lizard', 'spock']: raise ValueError("decoy must be one of the following: 'rock', 'paper', 'scissors', 'lizard', 'spock'")
            return ['rock', 'paper', 'scissors', 'lizard', 'spock'].index(d.lower())
    
    def __init__(self, edgework:edgework, decoy:str|None):
        '''
        Initialize a new rockpaperscissorslizardspock instance

        Args:
            edgework (edgework): The edgework of the bomb
            decoy (str|None): The decoy piece that appears on the module. The decoy is the one that is on the middle of a 3 piece in a line
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__decoy = self.__check(decoy)
    
    def __check_winner(self, score, beat):
        if score.count(max(score))>=2 or score.index(max(score))==self.__decoy: return None    
        return set(beat.get([a for a in beat.keys()][score.index(max(score))]))

    def __check_condition(self, table, score, idx, items):
            for a in range(5):
                score[a] += 1 if any([b in items for b in table[idx][a]]) else 0
            return score

    def __calculate(self):
        beat = {
            'rock': ('paper', 'spock'),
            'paper': ('scissors', 'lizard'),
            'scissors': ('rock', 'spock'),
            'lizard': ('rock', 'scissors'),
            'spock': ('paper', 'lizard')
        }
        table = [
            ["RO","PA","SI","LZ","CK"],
            [["RJ-45"], ["PARALLEL"], ["SERIAL"], ["DVI-D"], ["STEREO RCA"]],
            [["FRK*","FRQ*"],["BOB*","IND*"],["CAR*","SIG*"],["CLR*","NSA*"],["SND*","MSA*"]],
            [["FRK","FRQ"],["BOB","IND"],["CAR","SIG"],["CLR","NSA"],["SND","MSA"]],
            ['05','36','19','28','47']
        ]
        score = [0,0,0,0,0]

        if all([a not in 'XY' for a in self._snletter]):
            score = self.__check_condition(table, score, 0, self._snletter)
            result = self.__check_winner(score, beat)
            if result is not None: return result
        if 'PS/2' not in self._uniqueports:
            score = self.__check_condition(table, score, 1, self._uniqueports)
            result = self.__check_winner(score, beat)
            if result is not None: return result
        if 'TRN*' not in self._litind:
            score = self.__check_condition(table, score, 2, self._litind)
            result = self.__check_winner(score, beat)
            if result is not None: return result
        if 'TRN' not in self._unlitind:
            score = self.__check_condition(table, score, 3, self._unlitind)
            result = self.__check_winner(score, beat)
            if result is not None: return result
        score = self.__check_condition(table, score, 4, self._sndigit)
        result = self.__check_winner(score, beat)
        if result is not None: return result
        else:
            return set([x for y in [beat.get(list(beat.keys())[a]) for a in range(len(beat.keys()))] for x in y if x!=['rock','paper','scissors','lizard','spock'][self.__decoy]])

    def solve(self):
        '''
        Solve the Rock Paper Scissors Lizard Spock module

        Returns:
            set (str): All piece buttons to press
        '''
        return self.__calculate()