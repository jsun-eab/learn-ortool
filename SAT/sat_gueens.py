# https://developers.google.com/optimization/cp/queens
from ortools.sat.python import cp_model


class DiagramPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def OnSolutionCallback(self):
        self.__solution_count += 1

        print(f'Solution {self.__solution_count}:')
        for v in self.__variables:
            print('   ', end='')
            queen_col = int(self.Value(v))
            board_size = len(self.__variables)
            # Print row with queen.
            for j in range(board_size):
                if j == queen_col:
                    # There is a queen in column j, row i.
                    print("Q", end=" ")
                else:
                    print("_", end=" ")
            print()
        print()

    def solution_count(self):
        return self.__solution_count


def main(board_size: int = 8):
    # Declare the model
    model: cp_model.CpModel = cp_model.CpModel()

    # define the variables
    # queens[j] = i means there is a queen in row i and column j
    queens: List = [model.NewIntVar(0, board_size - 1, f'queen-{i}') for i in range(board_size)]

    # define the constraints
    # The following sets the constraint that all queens are in different rows.
    # Note: all queens must be in different columns because the indices of queens are all different.
    model.AddAllDifferent(queens)

    # The following sets the constraint that no two queens can be on the same diagonal.
    for i in range(board_size):
        # Note: is not used in the inner loop.
        diag1 = []
        diag2 = []
        for j in range(board_size):
            # Create variable array for queens(j) + j.
            q1 = model.NewIntVar(0, 2 * board_size, 'diag1_%i' % i)
            diag1.append(q1)
            model.Add(q1 == queens[j] + j)
            # Create variable array for queens(j) - j.
            q2 = model.NewIntVar(-board_size, board_size, 'diag2_%i' % i)
            diag2.append(q2)
            model.Add(q2 == queens[j] - j)
        model.AddAllDifferent(diag1)
        model.AddAllDifferent(diag2)

    # Create a solver and solve
    solver = cp_model.CpSolver()
    solution_printer = DiagramPrinter(queens)
    status = solver.SearchForAllSolutions(model, solution_printer)
    print('Solutions found : %i' % solution_printer.solution_count())


if __name__ == '__main__':
    main(5)
