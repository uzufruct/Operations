import heapq


def column(A, j):
    return [row[j] for row in A]


def transpose(A):
    return [column(A, j) for j in range(len(A[0]))]


def isPivotCol(col):
    return (len([c for c in col if c == 0]) == len(col) - 1) and sum(col) == 1


def variableValueForPivotColumn(tableau, column):
    pivotRow = [i for (i, x) in enumerate(column) if x == 1][0]
    return tableau[pivotRow][-1]


# assume the last m columns of A are the slack variables; the initial basis is
# the set of slack variables
def initialTableau(c, A, b):
    tableau = [row[:] + [x] for row, x in zip(A, b)]
    tableau.append([ci for ci in c] + [0])
    return tableau


def primalSolution(tableau):
    # the pivot columns denote which variables are used
    columns = transpose(tableau)
    indices = [j for j, col in enumerate(columns[:-1]) if isPivotCol(col)]
    return [(colIndex, variableValueForPivotColumn(tableau, columns[colIndex]))
            for colIndex in indices]


def objectiveValue(tableau):
    return -(tableau[-1][-1])


def canImprove(tableau):
    lastRow = tableau[-1]
    return any(x > 0 for x in lastRow[:-1])


# this can be slightly faster
def moreThanOneMin(L):
    if len(L) <= 1:
        return False

    x, y = heapq.nsmallest(2, L, key=lambda x: x[1])
    return x == y


def findPivotIndex(tableau):
    # pick minimum positive index of the last row
    column_choices = [(i, x) for (i, x) in enumerate(tableau[-1][:-1]) if x > 0]
    column = min(column_choices, key=lambda a: a[1])[0]

    # check if unbounded
    if all(row[column] <= 0 for row in tableau):
        raise Exception('Linear program is unbounded.')

    # check for degeneracy: more than one minimizer of the quotient
    quotients = [(i, r[-1] / r[column])
                 for i, r in enumerate(tableau[:-1]) if r[column] > 0]

    if moreThanOneMin(quotients):
        raise Exception('Linear program is degenerate.')

    # pick row index minimizing the quotient
    row = min(quotients, key=lambda x: x[1])[0]

    return row, column


def pivotAbout(tableau, pivot):
    i, j = pivot

    pivotDenom = tableau[i][j]
    tableau[i] = [x / pivotDenom for x in tableau[i]]

    for k, row in enumerate(tableau):
        if k != i:
            pivotRowMultiple = [y * tableau[k][j] for y in tableau[i]]
            tableau[k] = [x - y for x, y in zip(tableau[k], pivotRowMultiple)]


'''
   simplex: [float], [[float]], [float] -> [float], float
   Solve the given standard-form linear program:
      max <c,x>
      s.t. Ax = b
           x >= 0
   providing the optimal solution x* and the value of the objective function
'''


def simplex(c, A, b):
    tableau = initialTableau(c, A, b)
    print("Initial tableau:")
    for row in tableau:
        print(row)
    print()

    while canImprove(tableau):
        pivot = findPivotIndex(tableau)
        print("Next pivot index is=%d,%d \n" % pivot)
        pivotAbout(tableau, pivot)
        print("Tableau after pivot:")
        for row in tableau:
            print(row)
        print()

    return tableau, primalSolution(tableau), objectiveValue(tableau)


if __name__ == "__main__":

    # maximization function
    c = [1, 2]

    # variables
    A = [[1, 2], [2, 1], [0, 1]]

    # constraints
    b = [6, 8, 2]

    # slack variables
    A[0] += [1, 0, 0]
    A[1] += [0, 1, 0]
    A[2] += [0, 0, 1]
    c += [0, 0, 0]

    t, s, v = simplex(c, A, b)
    # print(t)
    print(s)
    print(v)
