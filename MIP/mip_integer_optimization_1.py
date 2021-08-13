# https://developers.google.com/optimization/mip/integer_opt
from ortools.linear_solver import pywraplp
from ortools.linear_solver.pywraplp import Solver, Variable, Constraint, Objective


def main():
    # Create the mip solver with the SCIP backend.
    solver: Solver = pywraplp.Solver.CreateSolver('SCIP')

    # Create the variables x and y.
    infinity: int = solver.infinity()
    x: Variable = solver.IntVar(0, solver.infinity(), 'x')
    y: Variable = solver.IntVar(0, solver.infinity(), 'y')
    print('Number of variables =', solver.NumVariables())

    # x + 7 * y <= 17.5
    solver.Add(x + 7 * y <= 17.5, 'x + 7 * y <= 17.5')
    # x <= 3.5
    solver.Add(x <= 3.5, 'x <= 3.5')
    print('Number of constraints =', solver.NumConstraints())

    # Maximize x + 10 * y
    solver.Maximize(x + 10 * y)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        print('   Objective value =', int(solver.Objective().Value()))
        print('   Variable x =', int(x.solution_value()))
        print('   Variable y =', int(y.solution_value()))
    else:
        print('The problem does not have an optimal solution.')


if __name__ == '__main__':
    main()
