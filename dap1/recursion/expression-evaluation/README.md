# Completing an expression

The fifth sheet: given a sequence of values, can plus and minus signs be
placed so that it evaluates to zero?

```
5, 3, 2, 4, 1, 0, 3   ->   5+3-2-4+1+0-3
5, 5, 5               ->   calculation impossible
```

The signature the sheet prescribes carries the state in parameters:
`addCalcExists(int[] values, int position, int result)`, both extra arguments
starting at zero. The recursion holds nothing of its own, so every call is
answerable on its terms, and the two branches are the two signs.

The extension asks for the expression rather than a yes or no, and the change
is one parameter: the text built so far. The decision procedure becomes a
constructive one without any change to the search, which is worth noticing,
because the usual way to produce a witness is to run the search twice.

Verification uses three independent things: a brute force over all sign
patterns as the oracle for the answer, an evaluator for the produced
expression, and the requirement that the evaluated value be zero whenever an
expression is claimed to exist. Sixty random sequences pass all three.
