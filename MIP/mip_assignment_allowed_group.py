# https://developers.google.com/optimization/assignment/assignment_groups
from ortools.linear_solver import pywraplp


def main():
    cost = [[90, 76, 75, 70, 50, 74],
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
    num_tasks = len(cost[1])

    # Allowed groups of workers:
    group1 = [[2, 3],  # Subgroups of workers 0 - 3
              [1, 3],
              [1, 2],
              [0, 1],
              [0, 2]]

    group2 = [[6, 7],  # Subgroups of workers 4 - 7
              [5, 7],
              [5, 6],
              [4, 5],
              [4, 7]]

    group3 = [[10, 11],  # Subgroups of workers 8 - 11
              [9, 11],
              [9, 10],
              [8, 10],
              [8, 11]]

    allowed_groups = []

    for i in range(len(group1)):
        for j in range(len(group2)):
            for k in range(len(group3)):
                allowed_groups.append(group1[i] + group2[j] + group3[k])
    min_val = 1e6
    min_group = 0
    min_x = 0
    for i in range(len(allowed_groups)):
        group = allowed_groups[i]
        res = assignment(cost, group)
        solver_tmp = res[0]
        x_tmp = res[1]

        if solver_tmp.Objective().Value() < min_val:
            min_val = solver_tmp.Objective().Value()
            min_index = i
            min_solver = solver_tmp
            min_x = x_tmp
            min_group = group

    print('Minimum cost = ', min_val)
    for i in min_group:
        for j in range(num_tasks):
            if min_x[i, j].solution_value() > 0:
                print('Worker', i, ' assigned to task', j, '  Cost = ', cost[i][j])


def assignment(cost, group):
    # Solve assignment problem for given group of workers.
    num_tasks = len(cost[0])

    # Instantiate a mixed-integer solver
    solver = pywraplp.Solver('AssignmentProblemGroups', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    x = {}
    for i in group:
        for j in range(num_tasks):
            x[i, j] = solver.IntVar(0, 1, 'x[%i,%i]' % (i, j))

    # Each worker is assigned to exactly one task.
    for i in group:
        solver.Add(solver.Sum([x[i, j] for j in range(num_tasks)]) <= 1)

    # Each task is assigned to at least one worker.
    for j in range(num_tasks):
        solver.Add(solver.Sum([x[i, j] for i in group]) >= 1)

    # Objective
    solver.Minimize(solver.Sum([cost[i][j] * x[i, j] for i in group for j in range(num_tasks)]))
    solver.Solve()
    return [solver, x]


if __name__ == '__main__':
    main()
