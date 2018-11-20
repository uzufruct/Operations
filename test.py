from scipy.optimize import linprog

c = [-1, -2]
A = [[-1, -2], [-2, -1]]
b = [6, 8]
x0_bnds = (0, None)
x1_bnds = (0, 2)
res = linprog(c, A, b, bounds=(x0_bnds, x1_bnds), method='simplex')
print(res)
