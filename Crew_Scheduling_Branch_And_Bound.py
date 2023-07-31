# Crew Scheduling via Branch & Bound

from pulp import LpVariable, LpProblem, LpMinimize, lpSum, value

# Flight times in hours
flight_times = {
    "flight_1": 5,
    "flight_2": 3,
    "flight_3": 4,
}

# Max work hours for each crew member
max_work_hours = {
    "crew_1": 7,
    "crew_2": 6,
}

# Define a function to solve a linear program
def solve_lp(flight_times, max_work_hours, x_bounds):
    # Define the decision variables
    x = LpVariable.dicts("x", ((i, j) for i in flight_times for j in max_work_hours), lowBound=x_bounds[0], upBound=x_bounds[1], cat='Continuous')

    # Define the problem
    prob = LpProblem("Crew_Scheduling", LpMinimize)

    # Add the objective
    prob += lpSum(x[(i, j)] * flight_times[i] for i in flight_times for j in max_work_hours)

    # Add the constraints
    for i in flight_times:
        prob += lpSum(x[(i, j)] for j in max_work_hours) == 1
    for j in max_work_hours:
        prob += lpSum(x[(i, j)] * flight_times[i] for i in flight_times) <= max_work_hours[j]

    # Solve the problem and return the solution and objective value
    prob.solve()
    return {v.name: v.varValue for v in prob.variables()}, value(prob.objective)

# Define a function to implement the Branch and Bound method
def branch_and_bound(flight_times, max_work_hours):
    # Initialize the best solution and objective value
    best_solution = None
    best_obj = float('inf')

    # Initialize the problem queue with the bounds for the decision variables
    problem_queue = [(0, 1)]

    # While there are still problems to solve
    while problem_queue:
        # Pop a problem from the queue
        x_bounds = problem_queue.pop(0)

        # Solve the LP relaxation of the problem
        solution, obj = solve_lp(flight_times, max_work_hours, x_bounds)

        # If the solution is better than the best found so far
        if obj < best_obj:
            # If the solution is integer, update the best solution and objective value
            if all(val.is_integer() for val in solution.values()):
                best_solution = solution
                best_obj = obj
            else:
                # Branch on a variable that is not integer in the solution and add the new problems to the queue
                for var, val in solution.items():
                    if not val.is_integer():
                        problem_queue.append((x_bounds[0], val))
                        problem_queue.append((val, x_bounds[1]))
                        break

    # Return the best integer solution found
    return best_solution

# Call the branch_and_bound function to solve the problem
best_solution = branch_and_bound(flight_times, max_work_hours)
print(best_solution)