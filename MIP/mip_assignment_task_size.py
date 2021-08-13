# https://developers.google.com/optimization/assignment/assignment_teams
from ortools.linear_solver import pywraplp


def main():
    solver = pywraplp.Solver('SolveAssignmentProblem',
                             pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

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
    sizes = [10, 7, 3, 12, 15, 4, 11, 5]
    total_size_max = 15
    num_workers = len(costs)
    num_tasks = len(costs[1])

    # Create the variables
    # x[i, j] is an array of boolean variables, which will be True / 1 if worker i is assigned to task j.
    x = {}
    for i in range(num_workers):
        for j in range(num_tasks):
            x[i, j] = solver.BoolVar(f'x[{i},{j}]')

    # Create a linear constraint
    # Total size of tasks for each worker is at most total_size_max.
    for i in range(num_workers):
        solver.Add(sum(sizes[j] * x[i, j] for j in range(num_tasks)) <= total_size_max)

    # Each task is assigned to exactly one worker.
    for j in range(num_tasks):
        solver.Add(solver.Sum([x[i, j] for i in range(num_workers)]) == 1, f'task{j}-workers')

    # Create the objective function
    solver.Minimize(solver.Sum([costs[i][j] * x[i, j] for i in range(num_workers) for j in range(num_tasks)]))

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print(f'Total cost = {round(solver.Objective().Value())}')
        print(f'Time = {solver.WallTime()} milliseconds')
        for i in range(num_workers):
            for j in range(num_tasks):
                if x[i, j].solution_value():
                    print(f'   Worker {i} is assigned to task {j}. Cost = {costs[i][j]}')


if __name__ == '__main__':
    main()
