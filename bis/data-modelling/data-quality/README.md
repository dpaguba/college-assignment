# Data quality

Five dimensions: completeness, consistency, accuracy, timeliness,
uniqueness. Only two of them can be checked without leaving the table, and
those are the two this module checks.

## Consistency, checked by functional dependency

A functional dependency holds when each value of one column goes with only
one value of another. It needs no knowledge of the world: if the same project
carries two different strategic fits, the table contradicts itself, whatever
the truth is.

That is exactly what happens in the project table. `Projekt` should determine
`Strategischer Fit`, because the fit is a property of the project. For four
of the five projects it does. **P5 IoT Produkt** has 8 in the rows for
technical and organisational risk and 9 in the row for market risk.

The right response is the boring one: record the contradiction, ask the
source which value holds, and only then add the rule as a constraint. A
correction without the constraint comes back next quarter.

## Completeness

Three projects have both quarters, two have only Q4. The cube is 80 % full,
and the missing cells are not errors: those projects did not exist in Q3. It
becomes an error the moment somebody computes an average per quarter without
noticing that the denominators differ.
