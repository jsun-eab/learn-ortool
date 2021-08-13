# https://developers.google.com/optimization/assignment/assignment_groups
from ortools.sat.python import cp_model


def main():
    # Model
    model = cp_model.CpModel()

    # Create data
    # each work is in a row and each task is in a column
    costs = [[90, 76, 75, 70, 50, 74],
             [35, 85, 55, 65, 48, 101],
             [125, 95, 90, 105, 59, 120],
             [45, 110, 95, 115, 104, 83],
             [60, 105, 80, 75, 59, 62],
             [45, 65, 110, 95, 47, 31],
             [38, 51, 107, 41, 69, 99],
             [47, 85, 57, 71, 92, 77],
             [39, 63, 97, 49, 118, 56],
             [47, 101, 71, 60, 88, 109],
             [17, 39, 103, 64, 61, 92],
             [101, 45, 83, 59, 92, 27]]
    num_workers = len(costs)
    num_tasks = len(costs[0])

    group1 = [[0, 0, 1, 1],  # Workers 2, 3
              [0, 1, 0, 1],  # Workers 1, 3
              [0, 1, 1, 0],  # Workers 1, 2
              [1, 1, 0, 0],  # Workers 0, 1
              [1, 0, 1, 0]]  # Workers 0, 2

    group2 = [[0, 0, 1, 1],  # Workers 6, 7
              [0, 1, 0, 1],  # Workers 5, 7
              [0, 1, 1, 0],  # Workers 5, 6
              [1, 1, 0, 0],  # Workers 4, 5
              [1, 0, 0, 1]]  # Workers 4, 7

    group3 = [[0, 0, 1, 1],  # Workers 10, 11
              [0, 1, 0, 1],  # Workers 9, 11
              [0, 1, 1, 0],  # Workers 9, 10
              [1, 0, 1, 0],  # Workers 8, 10
              [1, 0, 0, 1]]  # Workers 8, 11

    # Create the variables
    x = {}
    for i in range(num_workers):
        for j in range(num_tasks):
            x[i, j] = model.NewBoolVar(f'x[{i},{j}]')

    # Create a linear constraint
    # Each worker is assigned to at most one task.
    [model.Add(sum(x[i, j] for j in range(num_tasks)) <= 1) for i in range(num_workers)]

    # Each task is assigned to at least one worker.
    [model.Add(sum(x[i, j] for i in range(num_workers)) == 1) for j in range(num_tasks)]

    # Create variables for each worker, indicating whether they work on some task.
    workers = []
    for i in range(num_workers):
        workers.append(model.NewBoolVar(f'worker{i}'))

    for i in range(num_workers):
        model.Add(workers[i] == sum(x[i, j] for j in range(num_tasks)))

    # Define the allowed groups of worders
    model.AddAllowedAssignments([workers[0], workers[1], workers[2], workers[3]], group1)
    model.AddAllowedAssignments([workers[4], workers[5], workers[6], workers[7]], group2)
    model.AddAllowedAssignments([workers[8], workers[9], workers[10], workers[11]], group3)

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
