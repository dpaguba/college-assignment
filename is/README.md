# Informationssysteme

Twenty-three modules in five blocks: the relational model and its algebra,
database design and normalisation, SQL against sqlite3, transactions, and
XML.

The exercise sheets' published answers are the reference where they exist.
The last sheet's `R ÷ π(B←A,C)(S)` gives `A = 1` and `(S − R) ⋈ T` gives
`(4, 3, y)`; both are reproduced here, the first by two independent methods
and by a doubly nested `NOT EXISTS` in sqlite3.

Where no published answer exists, something else checks the work: sqlite3 for
the algebra and the three-valued logic, a derivation from Armstrong's axioms
for the attribute closure, an actual join of projections for the tableau test
of losslessness, and a simulated lock manager for the guarantee of two-phase
locking.

## What the measurements showed

- `NOT IN` over a list containing a null returns nothing where the equivalent
  `NOT EXISTS` returns two rows.
- A row with a null value satisfies neither `value = 1` nor `value <> 1`.
- `COUNT(*)` counts 5 where `COUNT(value)` counts 3, and `AVG` returns 20.0
  where treating the nulls as zero returns 12.0.
- Of the six interleavings of two crosswise transactions, four are not
  conflict serialisable, and two-phase locking produces neither.
- Boyce-Codd decomposition of student-subject-teacher loses
  `{student, subject} → teacher`; the synthesis leaves the schema alone,
  because it is already in third normal form.
