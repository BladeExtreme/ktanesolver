__semadict = {
    tuple(sorted({'S','SW'})): ['A','1'],
	tuple(sorted({'S','W'})): ['B', '2'],
	tuple(sorted({'S','NW'})): ['C', '3'],
	tuple(sorted({'S','N'})): ['D', '4'],
	tuple(sorted({'S','NE'})): ['E', '5'],
	tuple(sorted({'S','E'})): ['F', '6'], 
	tuple(sorted({'S','SE'})): ['G', '7'], 
	tuple(sorted({'SW','W'})): ['H', '8'],
	tuple(sorted({'SW','NW'})): ['I', '9'],
	tuple(sorted({'N','E'})): ['J'],
	tuple(sorted({'SW','N'})): ['K', '0'],
	tuple(sorted({'SW','NE'})): ['L'],
	tuple(sorted({'SW','E'})): ['M'],
	tuple(sorted({'SW','SE'})): ['N'],
	tuple(sorted({'W','NW'})): ['O'],
	tuple(sorted({'W','N'})): ['P'],
	tuple(sorted({'W','NE'})): ['Q'],
	tuple(sorted({'W','E'})): ['R'],
	tuple(sorted({'W','SE'})): ['S'],
	tuple(sorted({'NW','N'})): ['T'],
	tuple(sorted({'NW','NE'})): ['U'],
	tuple(sorted({'N','SE'})): ['V'],
	tuple(sorted({'NE','E'})): ['W'],
	tuple(sorted({'NE','SE'})): ['X'],
	tuple(sorted({'E','NW'})): ['Y'],
	tuple(sorted({'E','SE'})): ['Z']
}

def _sematranslate(a, state):
    if state>1 or state<0: raise ValueError("State must be 0-1")
    if isinstance(a, list):
        for iter in range(len(a)):
            if isinstance(a[iter], str):
                a = __semadict[tuple(sorted(set(a)))][state]
                break
            try:
                a[iter] = __semadict[tuple(sorted(set(a[iter])))][state]
            except:
                raise KeyError(f"This semaphore combination cannot be found. {a[iter]}")
    return a