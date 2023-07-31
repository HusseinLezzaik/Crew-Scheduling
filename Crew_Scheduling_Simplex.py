# Crew Scheduling using Simplex

from pulp import LpVariable, LpBinary, lpSum, LpProblem, LpMinimize, LpContinuous

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

# Define the problem
prob = LpProblem("Crew_Scheduling", LpMinimize)

# Define the decision variables
x = LpVariable.dicts("x", ((i, j) for i in flight_times for j in max_work_hours), lowBound=0, upBound=1, cat=LpContinuous)

# Add the objective
prob += lpSum(x[(i, j)] * flight_times[i] for i in flight_times for j in max_work_hours)

# Each flight must be covered by exactly one crew member
for i in flight_times:
    prob += lpSum(x[(i, j)] for j in max_work_hours) == 1

# Each crew member cannot work more than their maximum hours
for j in max_work_hours:
    prob += lpSum(x[(i, j)] * flight_times[i] for i in flight_times) <= max_work_hours[j]

# Solve the problem
prob.solve()

# Print the values of the decision variables
for i in flight_times:
    for j in max_work_hours:
        print(f"Crew {j} assigned to flight {i}: {x[(i, j)].varValue}")