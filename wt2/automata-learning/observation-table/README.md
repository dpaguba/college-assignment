# The observation table

Rows are labelled with words, columns with suffixes, and each cell holds the
oracle's answer for the concatenation. Two rows with the same contents stand
for the same state, which is the Myhill-Nerode idea used as a data structure.

## Closed and consistent

The table is closed when every one-letter extension of a row looks like some
row already present. An extension that looks like nothing known is a state
that has been discovered and has no name yet, so it becomes a row.

The table is consistent when two rows that look the same still look the same
after appending any letter. If they do not, some suffix separates them and it
becomes a column.

Making the table closed and consistent, then reading off the automaton, is
the whole construction. The start state is the row of the empty word; a state
accepts when its answer to the empty suffix is yes.

Every membership query is asked once and cached; the count is the measure the
whole method is judged by. The parity language needs 5 queries.
