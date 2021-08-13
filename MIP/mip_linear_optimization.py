# https://developers.google.com/optimization/lp/glop
from ortools.linear_solver import pywraplp
from ortools.linear_solver.pywraplp import Solver, Variable, Constraint, Objective


def main():
    # Create the linear solver with the GLOP backend.
    solver: Solver = pywraplp.Solver.CreateSolver('GLOP')
    # solver.EnableOutput()

    # Create the variables x and y.
    infinity = solver.infinity()
    x: Variable = solver.NumVar(-infinity, infinity, 'x')
    y: Variable = solver.NumVar(-infinity, infinity, 'y')
    print('Number of variables =', solver.NumVariables())

    # Constraint 0: x + 2y <= 14
    solver.Add(x + 2 * y <= 14)
    # Constraint 1: 3x - y >= 0
    solver.Add(3 * x - y >= 0)
    # Constraint 2: x - y <= 2
    solver.Add(x - y <= 2)
    print('Number of constraints =', solver.NumConstraints())

    # Objective function: 3x + 4y.
    solver.Maximize(3 * x + 4 * y)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        print('   Objective value =', solver.Objective().Value())
        print('   x =', x.solution_value())
        print('   y =', y.solution_value())
    else:
        print('The problem does not have an optimal solution.')


if __name__ == '__main__':
    main()
