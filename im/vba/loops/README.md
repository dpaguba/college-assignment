# Loops

## The empty loop

`For i = 5 To 1` does not run at all: the condition is already violated
before the first pass. It needs `Step -1` to run backwards. Forgetting the
step gives no error message, just a loop that does nothing, and that is hard
to see in a listing.

## The variable after the loop

In VBA the loop variable lives on and holds the first value that violated the
condition. After `For i = 1 To 10` it is eleven, not ten. Computing with i
afterwards means computing with a value the loop never processed.

## Leading and trailing test

`Do While ... Loop` tests first, `Do ... Loop While` tests last. The
difference shows in exactly one case, and in that case always: if the
condition is false from the start, the first form runs zero times and the
second once.

## Until against While

`Do Until x > 5` runs as long as `Do While x <= 5`. The two are equivalent,
and the choice is about readability: write the one whose condition needs no
negation.
