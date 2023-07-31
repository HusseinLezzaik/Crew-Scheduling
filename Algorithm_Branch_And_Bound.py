# Branch and Bound Algorithm

import numpy as np
from scipy.optimize import linprog

def branch_and_bound(c, A, b):
    # Step 1: Solve the LP relaxation
    result = linprog(c, A_ub=A, b_ub=b, method='simplex')
    if not result.success:
        return None  # problem is infeasible

    # Step 2: Check if the solution is integer
    x = result.x
    if np.allclose(x, np.round(x)):
        return x  # solution is integer, problem is solved

    # Step 3: Branch on a fractional variable
    i = np.where(~np.isclose(x, np.round(x)))[0][0]
    A1 = np.vstack([A, np.eye(len(c))[i]])
    A2 = np.vstack([A, -np.eye(len(c))[i]])
    b1 = np.hstack([b, np.floor(x[i])])
    b2 = np.hstack([b, -np.ceil(x[i])])

    # Step 4: Recursively solve the two subproblems
    x1 = branch_and_bound(c, A1, b1)
    x2 = branch_and_bound(c, A2, b2)

    # Step 5: Return the best integer solution found
    if x1 is None:
        return x2
    elif x2 is None:
        return x1
    elif c @ x1 <= c @ x2:
        return x1
    else:
        return x2
