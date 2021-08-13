# https://developers.google.com/optimization/assignment/assignment_teams
from ortools.linear_solver import pywraplp


def main():
    solver = pywraplp.Solver('SolveAssignmentProblemMIP',
                             pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    # Create data
    # each work is in a row and each task is in a column
    costs = [[90, 76, 75, 70],
             [35, 85, 55, 65],
             [125, 95, 90, 105],
             [45, 110, 95, 115],
             [60, 105, 80, 75],
             [45, 65, 110, 95]]
    team1 = [0, 2, 4]
    team2 = [1, 3, 5]
    team_max = 2
    num_workers = len(costs)
    num_tasks = len(costs[0])

    # Create the variables
    # x[i, j] is an array of boolean variables, which will be True / 1 if worker i is assigned to task j.
    x = {}
    for i in range(num_workers):
        for j in range(num_tasks):
            x[i, j] = solver.BoolVar(f'x[{i},{j}]')

    # Create a linear constraint
    # Each worker is assigned to at most 1 task.
    for i in range(num_workers):
        solver.Add(solver.Sum([x[i, j] for j in range(num_tasks)]) <= 1, f'worker{i}-tasks')

    # Each task is assigned to exactly one worker.
    for j in range(num_tasks):
        solver.Add(solver.Sum([x[i, j] for i in range(num_workers)]) == 1, f'task{j}-workers')

    # Each team takes on two tasks.
    solver.Add(solver.Sum([x[i, j] for i in team1 for j in range(num_tasks)]) <= team_max)
    solver.Add(solver.Sum([x[i, j] for i in team2 for j in range(num_tasks)]) <= team_max)

    # Create the objective function
    solver.Minimize(solver.Sum([costs[i][j] * x[i, j] for i in range(num_workers) for j in range(num_tasks)]))

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print(f'Total cost = {round(solver.Objective().Value())}')
        print(f'Time = {solver.WallTime()} milliseconds')
        for i in range(num_workers):
            for j in range(num_tasks):
                if x[i, j].solution_value() > 0.5:
                    print(f'   Worker {i} is assigned to task {j}. Cost = {costs[i][j]}')


if __name__ == '__main__':
    main()
