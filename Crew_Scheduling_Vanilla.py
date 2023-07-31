# Vanilla Crew Scheduling

# Step 1: Define the flights and crew members, along with the flight times and max work hours.

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

# Step 2: Define the decision variables

from pulp import LpVariable, LpBinary, lpSum 

x = LpVariable.dicts("x", ((i, j) for i in flight_times for j in max_work_hours), cat='Binary')

# Step 3: Define the objective

from pulp import LpProblem, LpMinimize

# Define the problem
prob = LpProblem("Crew_Scheduling", LpMinimize)

# Add the objective
prob += lpSum(x[(i, j)] * flight_times[i] for i in flight_times for j in max_work_hours)

# Step 4: Define the constraints

# Each flight must be covered by exactly one crew member
for i in flight_times:
    prob += lpSum(x[(i, j)] for j in max_work_hours) == 1   

# Each crew member cannot work more than their maximum hours
for j in max_work_hours:
    prob += lpSum(x[(i, j)] * flight_times[i] for i in flight_times) <= max_work_hours[j]

# Step 5: Solve the problem

from pulp import LpStatus, value

# Solve the problem
prob.solve()

# Print the status of the solution
print("Status:", LpStatus[prob.status])

# Print the optimal assignments
for i in flight_times:
    for j in max_work_hours:
        print(f"Crew {j} assigned to flight {i}: {x[(i, j)].varValue}")