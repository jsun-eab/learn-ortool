# https://developers.google.com/optimization/introduction/python
from ortools.linear_solver import pywraplp
from ortools.linear_solver.pywraplp import Solver, Variable, Constraint, Objective


def main():
    # Create the linear solver with the GLOP backend.
    solver: Solver = pywraplp.Solver.CreateSolver('GLOP')

    # Create the variables x and y.
    x: Variable = solver.NumVar(0, 1, 'x')
    y = solver.NumVar(0, 2, 'y')
    print('Number of variables =', solver.NumVariables())

    # Create a linear constraint, 0 <= x + y <= 2.
    ct: Constraint = solver.Constraint(0, 2, 'ct')
    ct.SetCoefficient(x, 1)
    ct.SetCoefficient(y, 1)
    print('Number of constraints =', solver.NumConstraints())

    # Create the objective function, 3 * x + y.
    objective: Objective = solver.Objective()
    objective.SetCoefficient(x, 3)
    objective.SetCoefficient(y, 1)
    objective.SetMaximization()

    solver.Solve()
    print('Solution:')
    print('Objective value =', objective.Value())
    print('x =', x.solution_value())
    print('y =', y.solution_value())


if __name__ == '__main__':
    main()
