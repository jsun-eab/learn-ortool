# https://developers.google.com/optimization/cp/cryptarithmetic
from ortools.constraint_solver import pywrapcp


def main():
    # Constraint programming engine
    solver = pywrapcp.Solver('CP is fun!')

    kBase = 10

    # Decision variables.
    digits = list(range(0, kBase))
    digits_without_zero = list(range(1, kBase))
    c = solver.IntVar(digits_without_zero, 'C')
    p = solver.IntVar(digits, 'P')
    i = solver.IntVar(digits_without_zero, 'I')
    s = solver.IntVar(digits, 'S')
    f = solver.IntVar(digits_without_zero, 'F')
    u = solver.IntVar(digits, 'U')
    n = solver.IntVar(digits, 'N')
    t = solver.IntVar(digits_without_zero, 'T')
    r = solver.IntVar(digits, 'R')
    e = solver.IntVar(digits, 'E')

    # We need to group variables in a list to use the constraint AllDifferent.
    letters = [c, p, i, s, f, u, n, t, r, e]

    # Verify that we have enough digits.
    assert kBase >= len(letters)

    # Define constraints.
    solver.Add(solver.AllDifferent(letters))

    # CP + IS + FUN = TRUE
    solver.Add(p + s + n + kBase * (c + i + u) + kBase * kBase * f ==
               e + kBase * u + kBase * kBase * r + kBase * kBase * kBase * t)

    db = solver.Phase(letters, solver.INT_VAR_DEFAULT,
                      solver.INT_VALUE_DEFAULT)
    solver.NewSearch(db)

    while solver.NextSolution():
        print(letters)
        # Is CP + IS + FUN = TRUE?
        assert (kBase * c.Value() + p.Value() + kBase * i.Value() + s.Value() +
                kBase * kBase * f.Value() + kBase * u.Value() + n.Value() ==
                kBase * kBase * kBase * t.Value() + kBase * kBase * r.Value() +
                kBase * u.Value() + e.Value())

    solver.EndSearch()


if __name__ == '__main__':
    main()
