# Modal equivalences

The box and the diamond are duals, `[]phi` is `!<>!phi`, exactly as the two
quantifiers are. Every law follows from that plus the propositional ones, and
so does every non-law.

## The catalogue, checked

| law | holds |
|---|---|
| `[]A = !<>!A` | yes |
| `<>A = ![]!A` | yes |
| `![]A = <>!A` | yes |
| `!<>A = []!A` | yes |
| `[](A & B) = []A & []B` | **yes** |
| `[](A \| B) = []A \| []B` | **no** |
| `<>(A \| B) = <>A \| <>B` | **yes** |
| `<>(A & B) = <>A & <>B` | **no** |

The two asymmetries are where the mistakes happen, and each has a small
counterexample. For `[](A | B)` against `[]A | []B`: one world seeing itself
and a world labelled `B`, with `A` true only at the first. Every successor
satisfies `A | B`, no successor set satisfies `A` throughout, and none
satisfies `B` throughout.

A table of laws in a lecture is exactly the kind of thing that gets
misremembered, so `check_catalogue` verifies the whole table in a second rather
than leaving it as prose.

## What equivalence checking can and cannot do

Modal equivalence means agreement in every world of every structure, which
cannot be enumerated. The search here goes up to three worlds: finding a
disagreement settles the question, finding none only says no small
counterexample exists. That asymmetry is stated rather than hidden, because it
is the difference between a refutation procedure and a decision procedure.

## Correspondence

Each frame axiom holds exactly on the frames with a matching property:
`[]A -> A` on reflexive frames, `[]A -> [][]A` on transitive ones, `[]A -> <>A`
on serial ones, `A -> []<>A` on symmetric ones. That correspondence is why
modal logic is used to describe transition systems: choosing axioms is choosing
what the transitions may look like.
