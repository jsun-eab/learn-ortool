# https://developers.google.com/optimization/cp/integer_opt_cp
from ortools.sat.python import cp_model


def main():
    # Declare the model
    model: cp_model.CpModel = cp_model.CpModel()

    # define the variables
    var_upper_bound = max(50, 45, 37)
    x: Variable = model.NewIntVar(0, var_upper_bound, 'x')
    y: Variable = model.NewIntVar(0, var_upper_bound, 'y')
    z: Variable = model.NewIntVar(0, var_upper_bound, 'z')

    # define the constraints
    model.Add(2 * x + 7 * y + 3 * z <= 50)
    model.Add(3 * x - 5 * y + 7 * z <= 45)
    model.Add(5 * x + 2 * y - 6 * z <= 37)

    # define the objective function
    model.Maximize(2 * x + 2 * y + 3 * z)

    # Create a solver and solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status == cp_model.OPTIMAL:
        print('Maximum of objective function: %i' % solver.ObjectiveValue())
        print('   x value: ', solver.Value(x))
        print('   y value: ', solver.Value(y))
        print('   z value: ', solver.Value(z))
    else:
        print('The problem does not have a solution.')


if __name__ == '__main__':
    main()
