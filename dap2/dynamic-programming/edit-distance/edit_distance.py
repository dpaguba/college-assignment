"""Edit distance: the fewest single-character edits turning one string into another."""

from __future__ import annotations

def edit_distance(left, right):
    """The Levenshtein distance between two sequences.

    Three operations are allowed, each costing one: insert a character, delete
    one, replace one. The recurrence considers the last character of each:

        equal, so nothing to pay, take the diagonal
        otherwise, one plus the cheapest of insert, delete or replace

    The three neighbours in the grid are exactly the three operations, which is
    the clearest correspondence between a table and a decision in this folder.

    It is a genuine metric: zero only for identical strings, symmetric, and it
    obeys the triangle inequality. The tests check the last two on random
    input, because those properties are what let it be used as a distance in
    clustering and nearest-neighbour search rather than merely as a score.

    Same grid as LCS, different weights. Where LCS asks how much is shared,
    this asks how much must change, and the two answers are related but not
    interchangeable.
    """
    rows, columns = len(left), len(right)
    table = [[0] * (columns + 1) for _ in range(rows + 1)]

    for row in range(rows + 1):
        table[row][0] = row
    for column in range(columns + 1):
        table[0][column] = column

    for row in range(1, rows + 1):
        for column in range(1, columns + 1):
            if left[row - 1] == right[column - 1]:
                table[row][column] = table[row - 1][column - 1]
            else:
                table[row][column] = 1 + min(
                    table[row - 1][column],      # delete
                    table[row][column - 1],      # insert
                    table[row - 1][column - 1],  # replace
                )

    return table[rows][columns]

def edit_operations(left, right):
    """The actual edits, as (kind, position, character), latest position first.

    Walking the table backwards recovers which of the three neighbours each
    cell came from, and that is the operation. The list comes out in reverse
    order of position, which is what lets it be applied to a mutable copy of
    the string without the positions shifting under it.
    """
    rows, columns = len(left), len(right)
    table = [[0] * (columns + 1) for _ in range(rows + 1)]
    for row in range(rows + 1):
        table[row][0] = row
    for column in range(columns + 1):
        table[0][column] = column
    for row in range(1, rows + 1):
        for column in range(1, columns + 1):
            if left[row - 1] == right[column - 1]:
                table[row][column] = table[row - 1][column - 1]
            else:
                table[row][column] = 1 + min(
                    table[row - 1][column], table[row][column - 1], table[row - 1][column - 1]
                )

    operations = []
    row, column = rows, columns
    while row > 0 or column > 0:
        if row > 0 and column > 0 and left[row - 1] == right[column - 1]:
            row, column = row - 1, column - 1
        elif row > 0 and column > 0 and table[row][column] == table[row - 1][column - 1] + 1:
            operations.append(("replace", row - 1, right[column - 1]))
            row, column = row - 1, column - 1
        elif column > 0 and table[row][column] == table[row][column - 1] + 1:
            operations.append(("insert", row, right[column - 1]))
            column -= 1
        else:
            operations.append(("delete", row - 1, left[row - 1]))
            row -= 1

    return operations
