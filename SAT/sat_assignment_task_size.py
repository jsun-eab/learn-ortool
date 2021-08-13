# https://developers.google.com/optimization/assignment/assignment_cp
from ortools.sat.python import cp_model


def main():
    # Model
    model = cp_model.CpModel()

    # Create data
    # each work is in a row and each task is in a column
    costs = [[90, 76, 75, 70, 50, 74, 12, 68],
             [35, 85, 55, 65, 48, 101, 70, 83],
             [125, 95, 90, 105, 59, 120, 36, 73],
             [45, 110, 95, 115, 104, 83, 37, 71],
             [60, 105, 80, 75, 59, 62, 93, 88],
             [45, 65, 110, 95, 47, 31, 81, 34],
             [38, 51, 107, 41, 69, 99, 115, 48],
             [47, 85, 57, 71, 92, 77, 109, 36],
             [39, 63, 97, 49, 118, 56, 92, 61],
             [47, 101, 71, 60, 88, 109, 52, 90]]
    # The size of each task
    sizes = [10, 7, 3, 12, 15, 4, 11, 5]
    # total_size_max is the upper bound on the total size of the tasks performed by any single worker
    total_size_max = 15
    num_workers = len(costs)
    num_tasks = len(costs[0])

    # Create the variables
    x = {}
    for i in range(num_workers):
        for j in range(num_tasks):
            x[i, j] = model.NewBoolVar(f'x[{i},{j}]')

    # Create a linear constraint
    # Total size of tasks for each worker is at most total_size_max.
    for i in range(num_workers):
        model.Add(sum(sizes[j] * x[i, j] for j in range(num_tasks)) <= total_size_max)

    # Each task is assigned to exactly one worker.
    for j in range(num_tasks):
        model.Add(sum(x[i, j] for i in range(num_workers)) >= 1)

    # Create the objective function
    objective_terms = []
    for i in range(num_workers):
        for j in range(num_tasks):
            objective_terms.append(costs[i][j] * x[i, j])
    model.Minimize(sum(objective_terms))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        print(f'Total cost = {solver.ObjectiveValue()}')
        for i in range(num_workers):
            for j in range(num_tasks):
                if solver.BooleanValue(x[i, j]):
                    print(f'   Worker {i} assigned to task {j}. Cost = {costs[i][j]}')
    else:
        print('No solution found.')


if __name__ == '__main__':
    main()
