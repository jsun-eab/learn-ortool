# https://developers.google.com/optimization/cp/cp_solver
from ortools.sat.python import cp_model


def main():
    # Declare the model
    model: cp_model.CpModel = cp_model.CpModel()

    # define the variables
    num_vals: int = 3
    x = model.NewIntVar(0, num_vals - 1, 'x')
    y = model.NewIntVar(0, num_vals - 1, 'y')
    z = model.NewIntVar(0, num_vals - 1, 'z')

    # define the constraints
    model.Add(x != y)

    # Create a solver and solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
        print('x = %i' % solver.Value(x))
        print('y = %i' % solver.Value(y))
        print('z = %i' % solver.Value(z))
    else:
        print('The problem does not have a solution.')


if __name__ == '__main__':
    main()
