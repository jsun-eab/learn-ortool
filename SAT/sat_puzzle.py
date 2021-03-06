# https://developers.google.com/optimization/cp/cryptarithmetic
from ortools.sat.python import cp_model


class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def OnSolutionCallback(self):
        self.__solution_count += 1
        for v in self.__variables:
            print('%s=%i' % (v, self.Value(v)), end=' ')
        print()

    def solution_count(self):
        return self.__solution_count


def main():
    # Declare the model
    model: cp_model.CpModel = cp_model.CpModel()

    # define the variables
    # Each of the ten letters must be a different digit.
    # C, I, F, and T can't be zero
    base = 10
    c = model.NewIntVar(1, base - 1, 'C')
    p = model.NewIntVar(0, base - 1, 'P')
    i = model.NewIntVar(1, base - 1, 'I')
    s = model.NewIntVar(0, base - 1, 'S')
    f = model.NewIntVar(1, base - 1, 'F')
    u = model.NewIntVar(0, base - 1, 'U')
    n = model.NewIntVar(0, base - 1, 'N')
    t = model.NewIntVar(1, base - 1, 'T')
    r = model.NewIntVar(0, base - 1, 'R')
    e = model.NewIntVar(0, base - 1, 'E')

    # We need to group variables in a list to use the constraint AllDifferent.
    letters = [c, p, i, s, f, u, n, t, r, e]
    # Verify that we have enough digits.
    assert base >= len(letters)

    # Define constraints.
    model.AddAllDifferent(letters)

    # CP + IS + FUN = TRUE
    model.Add(c * base + p + i * base + s + f * base * base + u * base +
              n == t * base * base * base + r * base * base + u * base + e)

    # Solve model.
    solver = cp_model.CpSolver()
    solution_printer = VarArraySolutionPrinter(letters)
    status = solver.SearchForAllSolutions(model, solution_printer)

    print('Statistics')
    print('  - status          : %s' % solver.StatusName(status))
    print('  - conflicts       : %i' % solver.NumConflicts())
    print('  - branches        : %i' % solver.NumBranches())
    print('  - wall time       : %f s' % solver.WallTime())
    print('  - solutions found : %i' % solution_printer.solution_count())


if __name__ == '__main__':
    main()
