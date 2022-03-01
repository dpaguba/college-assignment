"""Gaussian elimination in exact arithmetic, and what the ranks decide.

Every entry is a fraction, so the elimination is exact and a pivot is zero
only when it really is zero. In floating point the same computation has to
guess whether a small number is a rounding error or a genuine value, and that
guess is what separates numerical linear algebra from the version the lecture
proves theorems about.

The main theorem on linear systems is a statement about two ranks: the system
is solvable exactly when the coefficient matrix and the augmented matrix have
the same rank, and the solution is unique exactly when that rank equals the
number of unknowns.
"""

from fractions import Fraction


def to_fractions(matrix):
    """The matrix with every entry as an exact fraction."""
    return [[Fraction(entry) for entry in row] for row in matrix]


def row_echelon(matrix):
    """The matrix in row echelon form, with the pivots as they fall."""
    rows = to_fractions(matrix)
    pivot_row = 0
    for column in range(len(rows[0]) if rows else 0):
        pivot = None
        for index in range(pivot_row, len(rows)):
            if rows[index][column] != 0:
                pivot = index
                break
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        for index in range(pivot_row + 1, len(rows)):
            factor = rows[index][column] / rows[pivot_row][column]
            if factor:
                rows[index] = [entry - factor * other
                               for entry, other in zip(rows[index], rows[pivot_row])]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return rows


def reduced_row_echelon(matrix):
    """The reduced form, where each pivot is one and alone in its column.

    Unlike the echelon form, this one is unique: two matrices with the same
    row space have the same reduced form, which is why it can be used to
    decide whether two systems describe the same solution set.
    """
    rows = row_echelon(matrix)
    pivots = []
    for index, row in enumerate(rows):
        column = next((position for position, entry in enumerate(row) if entry != 0),
                      None)
        if column is None:
            continue
        pivots.append((index, column))
        rows[index] = [entry / row[column] for entry in row]
        for other in range(len(rows)):
            if other == index or rows[other][column] == 0:
                continue
            factor = rows[other][column]
            rows[other] = [entry - factor * pivot_entry
                           for entry, pivot_entry in zip(rows[other], rows[index])]
    return rows


def rank(matrix):
    """How many rows of the echelon form are not zero."""
    return sum(1 for row in row_echelon(matrix) if any(entry != 0 for entry in row))


def rank_augmented(matrix, right):
    """The rank of the matrix with the right-hand side attached."""
    return rank([row + [value] for row, value in zip(matrix, right)])


def solvable(matrix, right):
    """Whether the system has a solution, by the rank criterion."""
    return rank(matrix) == rank_augmented(matrix, right)


def solve(matrix, right):
    """The solution set: none, one point, or a point and a kernel basis."""
    if not solvable(matrix, right):
        return {"kind": "none", "particular": None, "kernel": []}
    columns = len(matrix[0])
    reduced = reduced_row_echelon([row + [value] for row, value
                                   in zip(matrix, right)])
    pivots = {}
    for row in reduced:
        column = next((position for position, entry in enumerate(row[:columns])
                       if entry != 0), None)
        if column is not None:
            pivots[column] = row
    particular = [Fraction(0)] * columns
    for column, row in pivots.items():
        particular[column] = row[columns]
    free = [column for column in range(columns) if column not in pivots]
    kernel = []
    for column in free:
        vector = [Fraction(0)] * columns
        vector[column] = Fraction(1)
        for pivot_column, row in pivots.items():
            vector[pivot_column] = -row[column]
        kernel.append(vector)
    kind = "unique" if not free else "many"
    return {"kind": kind, "particular": particular, "kernel": kernel}


def satisfies(matrix, right, vector):
    """Whether the vector solves the system."""
    for row, value in zip(to_fractions(matrix), right):
        if sum(entry * unknown for entry, unknown in zip(row, vector)) \
                != Fraction(value):
            return False
    return True
