from ..edgework import edgework

class maintenance(edgework):
    __model = {
      'HN': 2, 'AD': 7,
      'RN': 3, 'BN': 8,
      'FD': 4, 'PC': 9,
      'MA': 5, 'FR': 10,
      'BM': 6
    }
    __jobs = {
        0: [5, 1, 9, 11], 8: [1, 7, 6, 11],
        1: [2, 12, 8, 10], 4: [7, 11, 1, 2],
        2: [3, 2, 1, 6], 15: [1, 10, 11, 12],
        9: [4, 10, 6, 1], 10: [7, 3, 5, 8],
        6: [6, 4, 10, 2], 5: [2, 9, 11, 3],
        3: [8, 4, 5, 12], 14: [1, 2, 3, 4],
        11: [1, 7, 3, 6], 13: [11, 9, 2, 5],
        7: [12, 5, 3, 8], 12: [8, 7, 5, 3]
    }
    __jobdef = {
        1: ['Wash', 3], 2: ['Headlight bulb', 6],
        3: ['Wiper replacement', 10], 4: ['Oil change', 15],
        5: ['Brake fluid change', 25], 6: ['Windscreen chip', 40],
        7: ['One tyre', 80], 8: ['Windscreen replacement [H]', 150],
        9: ['Two tyres', 160], 10: ['Four tyres', 320],
        11: ['Exhaust welding [H]', 500], 12: ['Head gasket replacement [H]', 750]
    }
    __coverage = {
        'Hastings Direct': ['Oil change'],
        'Swift': ['Oil change', 'One tyre'],
        'AA': ['Oil change', 'Windscreen chip', 'Brake fluid change'],
        'Aviva': ['One tyre', 'Two tyres'],
        'Axa': ['Windscreen chip'],
        'Swinton': ['Windscreen chip'],
        'RAC': ['Windscreen chip', "Windscreen replacement [H]"],
        'Admiral': ['Brake fluid change']
    }
    
    def __check(self, p, n):
        if not isinstance(p, str): raise TypeError("plate must be in str")
        elif not isinstance(n, int): raise TypeError("nofjobs must be in int")
        elif n not in range(1,5): raise ValueError("nofjobs must be in range of 1-4")
        p = p.replace(" ",""); p = p.upper()
        return p,n
    
    def __init__(self, edgework:edgework, plate:str, nofjobs:int):
        '''
        Initialize a new maintenance instance

        Args:
            edgework (edgework): The edgework of the bomb
            plate (str): The plate number that appears on the module
            nofjobs (int): The number of jobs need to be done. Can only be in range of 1-4
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__plate, self.__nofjobs = self.__check(plate, nofjobs)
    
    def __calculate(self):
        insurance_dict = {'C': 'Admiral', 'F': 'Swift', 'J': 'Axa', 'M': 'Swinton','R': 'Aviva', 'U': 'RAC', 'W': 'AA', 'Y': 'Hastings Direct'}
        platref = int(self.__plate[2:4])
        model = self.__model[self.__plate[0:2]]; manufactured = ("Sept " if platref>=50 else "Mar ")+("20"+self.__late[2:4] if platref>=50 else str(platref-50)); platref -= 50 if platref>=50 else 0
        multiplier = (platref*10)+40 if platref in range(1,6) else (platref*25)-50 if platref in range(6,10) else 200 if platref==10 else 250 if platref in range(11,12) else (platref-9)*100

        for a in insurance_dict:
            if self.__plate[-1] < a:
                insurance = insurance_dict[a]
                break

        job_list = [self.__jobdef[a] for a in self.__jobs[int(''.join(['1' if insurance[0] == 'A' else '0', '1' if "Sept" in manufactured else '0', '1' if 'M' in self.__plate else '0', '1' if self.__plate[0:2] in ['BN', 'PC', 'FR'] else '0']), 2)][0:self.__nofjobs]]
        total_price = sum([a[-1] for a in job_list])
        value = model*multiplier

        if (total_price > value) and (sum([a[-1] for a in job_list if a not in self.__coverage[insurance]]) > value):
            return -1
        else: job_list = [a[0] for a in sorted(job_list, key=lambda x: x[-1])]

        if 'Oil change' in job_list: l = job_list.pop(job_list.index('Oil change')); job_list.append(l)
        if 'Wash' in job_list: l = job_list.pop(job_list.index('Wash')); job_list.append(l)
        if 'Brake fluid change' in job_list: f = job_list.pop(job_list.index('Brake fluid change')); job_list.insert(0, f)
        if 'Windscreen chip' in job_list: f = job_list.pop(job_list.index('Windscreen chip')); job_list.insert(0, f)

        if any([a in b for a in ['One tyre', 'Two tyres', 'Four tyres'] for b in job_list]):
            idx = job_list.index([a for a in job_list if a in ['One tyre', 'Two tyres', 'Four tyres']][0])
            t = job_list.pop(idx); job_list.insert(-2 if 'Wash' in job_list and 'Oil change' in job_list else -1, t)
        if any(['[H]' in a for a in job_list]):
            heavy_jobs = [a for a in job_list if '[H]' in a]
            for a in range(len(heavy_jobs)):
              h = job_list.pop(job_list.index(heavy_jobs[a]))
              idx = job_list.index([a for a in job_list if a in ['One tyre', 'Two tyres', 'Four tyres']][0])
              job_list.insert(idx, h)
        
        return [a.replace(" [H]", "").lower() for a in job_list]
    
    def solve(self):
        '''
        Solve the Maintenance module

        Returns:
            tuple (str, ...): The list of jobs need to be done
        '''
        return tuple(self.__calculate())