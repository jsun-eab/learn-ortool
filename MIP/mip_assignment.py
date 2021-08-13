# https://developers.google.com/optimization/assignment/assignment_example
from ortools.linear_solver import pywraplp


def main():
    # Create the mip solver with the SCIP backend.
    solver: pywraplp.Solver = pywraplp.Solver.CreateSolver('SCIP')

    # Create data
    # each work is in a row and each task is in a column
    costs = [
        [90, 80, 75, 70],
        [35, 85, 55, 65],
        [125, 95, 90, 95],
        [45, 110, 95, 115],
        [50, 100, 90, 100],
    ]
    num_workers = len(costs)
    num_tasks = len(costs[0])

    # Create the variables
    # x[i, j] is an array of boolean variables, which will be True / 1 if worker i is assigned to task j.
    x = {}
    for i in range(num_workers):
        for j in range(num_tasks):
            x[i, j] = solver.BoolVar(f'worker{i}-task{j}')

    # Create a linear constraint
    # Each worker is assigned to at most 1 task.
    for i in range(num_workers):
        solver.Add(solver.Sum([x[i, j] for j in range(num_tasks)]) <= 1, f'worker{i}-tasks')

    # Each task is assigned to exactly one worker.
    for j in range(num_tasks):
        solver.Add(solver.Sum([x[i, j] for i in range(num_workers)]) == 1, f'task{i}-workers')

    # Create the objective function
    objective_terms = []
    for i in range(num_workers):
        for j in range(num_tasks):
            objective_terms.append(costs[i][j] * x[i, j])
    solver.Minimize(solver.Sum(objective_terms))

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print(f'Total cost = {round(solver.Objective().Value())}')
        for i in range(num_workers):
            for j in range(num_tasks):
                if x[i, j].solution_value() > 0.5:
                    print(f'   Worker {i} is assigned to task {j}. Cost = {costs[i][j]}')


if __name__ == '__main__':
    main()
