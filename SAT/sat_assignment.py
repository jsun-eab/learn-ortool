# https://developers.google.com/optimization/assignment/assignment_example
from ortools.sat.python import cp_model


def main():
    # Model
    model = cp_model.CpModel()

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
    x = {}
    for i in range(num_workers):
        for j in range(num_tasks):
            x[i, j] = model.NewBoolVar(f'x[{i},{j}]')

    # Create a linear constraint
    # Each worker is assigned to at most one task.
    for i in range(num_workers):
        model.Add(sum(x[i, j] for j in range(num_tasks)) <= 1)

    # Each task is assigned to exactly one worker.
    for j in range(num_tasks):
        model.Add(sum(x[i, j] for i in range(num_workers)) == 1)

    # Create the objective function
    objective_terms = []
    for i in range(num_workers):
        for j in range(num_tasks):
            objective_terms.append(costs[i][j] * x[i, j])
    model.Minimize(sum(objective_terms))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f'Total cost = {solver.ObjectiveValue()}')
        for i in range(num_workers):
            for j in range(num_tasks):
                if solver.BooleanValue(x[i, j]):
                    print(f'   Worker {i} assigned to task {j}. Cost = {costs[i][j]}')
    else:
        print('No solution found.')


if __name__ == '__main__':
    main()
