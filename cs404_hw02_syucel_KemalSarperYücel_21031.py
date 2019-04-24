# python-constraint package installed via Settings/Project Interpreter
from constraint import *    # python-constraint provided in the pdf
inp = [['W', 'W', 'W', 'W', 'W', 'W', 'B'],
       ['W', 'W', '4', 'W', 'W', 'W', 'W'],
       ['0', 'W', 'W', 'W', '1', 'B', 'W'],
       ['W', 'W', 'W', '1', 'W', 'W', 'W'],
       ['W', 'B', '1', 'W', 'W', 'W', 'B'],
       ['W', 'W', 'W', 'W', 'B', 'W', 'W'],
       ['1', 'W', 'W', 'W', 'W', 'W', 'W']]

row = len(inp)
col = len(inp[0])
modulus = max(row, col) + 1
variables = []
constraints = dict()
black = []
for r in range(row):    # Store the position as a matrix index
    for c in range(col):
        if inp[r][c] == 'W':
            variables.append(r * modulus + c)    # Store every white tile as a variable
        elif inp[r][c] != 'B':
            constraints[r * modulus + c] = int(inp[r][c])    # Every number as a constraint
            black.append(r * modulus + c)    # Every black tile including numbers
        else:
            black.append(r * modulus + c)


def next_to(pos):   # Returns the white tiles that are located above, below, right and left of the given black tile
    nextc = []
    temp1 = [pos + modulus, pos - modulus, pos + 1, pos - 1]
    for t in temp1:
        if t in variables:
            nextc.append(t)
    return nextc


problem = Problem()
problem.addVariables(variables, range(2))
visited_row = []
visited_col = []
for var in variables:
    visitedr = 0    # Check if the the current tile's sub row is already added to the constraints
    visitedc = 0    # Check if the the current tile's sub column is already added to the constraints
    temp_row = []   # Contains the current sub row to add to the constraints
    temp_col = []   # Contains the current sub row to add to the constraints
    if var not in visited_row:
        temp_row.append(var)
        visited_row.append(var)
    else:
        visitedr += 1
    if var not in visited_col:
        temp_col.append(var)
        visited_col.append(var)
    else:
        visitedc += 1
    if visitedr + visitedc != 2:
        for var2 in variables:
            if var != var2:
                if visitedr == 0:
                    xr = [a for a in black if ((a > var) & (a < var2)) | ((a > var2) & (a < var))]
                    # Check if they are in the same row and have no black tiles between them
                    if (var // modulus == var2 // modulus) & (xr == []):
                        temp_row.append(var2)
                        visited_row.append(var2)
                if visitedc == 0:
                    xc = [b for b in black if (((b > var) & (b < var2)) | ((b > var2) & (b < var))) & (b % modulus == var % modulus)]
                    # Check if they are in the same column and have no black tiles between them
                    if (var % modulus == var2 % modulus) & (xc == []):
                        temp_col.append(var2)
                        visited_col.append(var2)
        if visitedr == 0:
            # Each sub row can have at most 1 light bulb
            problem.addConstraint(MaxSumConstraint(1), temp_row)
        if visitedc == 0:
            # Each sub column can have at most 1 light bulb
            problem.addConstraint(MaxSumConstraint(1), temp_col)
for num in constraints.keys():
    problem.addConstraint(ExactSumConstraint(constraints[num]), next_to(num))
for v in variables:
    temp = [v]
    for v2 in variables:
        if v != v2:
            yr = [a for a in black if ((a > v) & (a < v2)) | ((a > v2) & (a < v))]
            yc = [b for b in black if (((b > v) & (b < v2)) | ((b > v2) & (b < v))) & (b % modulus == v % modulus)]
            # Check if they are in the same row\column and have no black tiles between them
            if ((v//modulus == v2//modulus) & (yr == [])) | ((v % modulus == v2 % modulus) & (yc == [])):
                temp.append(v2)
    problem.addConstraint(MinSumConstraint(1), temp)
solutions = problem.getSolutions()
counter = 0
for solution in solutions:  # print each solution as a matrix, L denotes light bulbs
    counter += 1
    print('Solution ' + str(counter) + ':')
    solMatrix = inp
    d = dict(solution)
    for k in d.keys():
        if d[k] == 1:
            solMatrix[k//modulus][k % modulus] = 'L'

    for rows in range(row):
        print(solMatrix[rows])