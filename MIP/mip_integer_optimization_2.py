# https://developers.google.com/optimization/mip/mip_var_array
from ortools.linear_solver import pywraplp
from ortools.linear_solver.pywraplp import Solver, Variable, Constraint, Objective


def create_data_model():
    """ Stores the data for the problem. """
    data: dict = {
        'cstr_coeffs': [
            [5, 7, 9, 2, 1],
            [18, 4, -9, 10, 12],
            [4, 7, 3, 8, 5],
            [5, 13, 16, 3, -7],
        ],
        'bounds': [250, 285, 211, 315],
        'obj_coeffs': [7, 8, 2, 9, 6],
        'num_vars': 5,
        'num_constraints': 4
    }
    return data


def main():
    # Create the mip solver with the SCIP backend.
    solver: Solver = pywraplp.Solver.CreateSolver('SCIP')

    # instantiate the data
    data = create_data_model()

    # define the variables
    infinity = solver.infinity()
    x: dict = {}
    for j in range(data['num_vars']):
        x[j] = solver.IntVar(0, infinity, f'x[{j}]')
    print('Number of variables =', solver.NumVariables())

    # define the constraints
    for i in range(data['num_constraints']):
        constraint = solver.RowConstraint(0, data['bounds'][i], f'row[{i}]')
        for j in range(data['num_vars']):
            constraint.SetCoefficient(x[j], data['cstr_coeffs'][i][j])
        # constraint_expr = [data['cstr_coeffs'][i][j] * x[j] for j in range(data['num_vars'])]
        # solver.Add(sum(constraint_expr) <= data['bounds'][i])
    print('Number of constraints =', solver.NumConstraints())

    # define the objective
    objective: Objective = solver.Objective()
    for j in range(data['num_vars']):
        objective.SetCoefficient(x[j], data['obj_coeffs'][j])
    objective.SetMaximization()
    # obj_expr = [data['obj_coeffs'][j] * x[j] for j in range(data['num_vars'])]
    # solver.Maximize(solver.Sum(obj_expr))

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        print(f'   Objective value = {round(solver.Objective().Value())}')
        for j in range(data['num_vars']):
            print(f'   {x[j].name()} = {int(x[j].solution_value())}')
        print(f'   Problem solved in {solver.wall_time()} milliseconds')
        print(f'   Problem solved in {solver.iterations()} iterations')
        print(f'   Problem solved in {solver.nodes()} branch-and-bound nodes')
    else:
        print('The problem does not have an optimal solution.')


if __name__ == '__main__':
    main()
