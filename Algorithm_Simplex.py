# Simplex.py
import numpy as np

def simplex(c, A, b):
    # Step 0: initialization
    n, m = A.shape  # n constraints, m variables
    N = list(range(m))  # nonbasic variables
    B = list(range(m, m+n))  # basic variables
    A = np.hstack([A, np.eye(n)])  # add slack variables
    c = np.hstack([c, np.zeros(n)])  # zero costs for slack variables
    
    # Iterations
    while True:
        # Step 1: compute coefficients of objective function in terms of basic variables
        cB = c[B]
        cN = c[N]
        AB = A[:, B]
        AN = A[:, N]
        cb_ = np.linalg.inv(AB).T @ cB
        zN = cN - AN.T @ cb_
        
        # Step 2: optimality test
        if np.all(zN <= 0):
            # current solution is optimal
            xB = np.linalg.inv(AB) @ b
            solution = np.zeros(m+n)
            for i, xi in zip(B, xB):
                solution[i] = xi
            return solution[:m]  # return solution for original variables
        
        # Step 3: select entering variable
        enter = N[np.argmax(zN)]
        
        # Step 4: compute direction of search
        dB = -np.linalg.inv(AB) @ A[:, enter]
        
        # Step 5: compute maximum step length
        steps = -b / dB
        steps[steps < 0] = np.inf  # ignore negative steps
        leave = B[np.argmin(steps)]  # select leaving variable
        
        # Step 6: update basic and nonbasic variables
        B.remove(leave)
        N.append(leave)
        N.remove(enter)
        B.append(enter)
        
        # Step 7: update b
        b = b + steps[np.argmin(steps)] * dB

# Define c, A, b for your problem
c = np.array([-5, -3, -4, 0, 0])  # negative costs because we want to minimize
A = np.array([
    [5, 3, 4, 0, 0],  # constraints for crew 1
    [0, 0, 0, 5, 3],  # constraints for crew 2
    [1, 0, 0, 1, 0],  # each flight must be covered by exactly one crew member
    [0, 1, 0, 0, 1],  # each flight must be covered by exactly one crew member
    [0, 0, 1, 0, 0],  # each flight must be covered by exactly one crew member
])
b = np.array([7, 6, 1, 1, 1])  # right-hand side of constraints

# Solve using the simplex method
solution = simplex(c, A, b)
print(solution)
