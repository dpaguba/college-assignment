# Kripke structures

Propositional logic evaluates a formula against an assignment. Modal logic
evaluates it against a **world** inside a structure, and the two operators
quantify over the worlds that world can see: `[]phi` holds when `phi` holds at
every successor, `<>phi` when it holds at some successor.

## The published table

Sheet 3 gives a four-world structure and asks which worlds satisfy
`<>(A | []B) -> <>[]!B`. Reproduced exactly:

| | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| A | | + | | + |
| B | + | + | | |
| `[]B` | | + | + | |
| `A \| []B` | | + | + | + |
| `<>(A \| []B)` | + | | + | + |
| `[]!B` | | + | | + |
| `<>[]!B` | | | + | + |
| the formula | | **+** | **+** | **+** |

so the formula holds in worlds 2, 3 and 4, which is the published answer.

The accessibility relation is drawn as a picture in the sheet, so it was
**reconstructed from the table**: the rows constrain it enough to pin it down.
`[]B` false at world 1 forces a successor outside `{1,2}`; `<>` false at world 2
forces world 2 to have no successors at all; `<>[]!B` false at 1 rules out 2 and
4 as its successors. What comes out is `1 -> {1,3}`, `2 -> {}`, `3 -> {2}`,
`4 -> {4}`, and every one of the nine rows then matches.

## The dead end is the whole exercise

World 2 has no successors, so `[]phi` is **vacuously true** there for every
`phi` and `<>phi` is false for every `phi`. That is why world 2 satisfies the
implication: its antecedent `<>(A | []B)` is false.

This is not a corner case to patch around. It is how modal logic says "nothing
can happen from here", and it is why the frame condition of seriality, every
world has a successor, is stated separately and does not hold in this structure.

## Frame properties

`is_reflexive`, `is_transitive` and `is_serial` are the conditions behind
`[]A -> A`, `[]A -> [][]A` and `[]A -> <>A`. The sheet's structure has none of
them, which is why none of those three axioms holds everywhere in it.
