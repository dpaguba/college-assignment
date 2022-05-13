# Operational semantics

The rules, in the form the lecture gives them: a prefix offers its action; a
sum offers the transitions of both sides and discards the one not taken; a
parallel composition offers the transitions of both sides plus the reaction
of two matching actions as τ; a restriction lets everything through except
its own name; a call is replaced by its body with the arguments substituted.

## The five terms of sheet 4

The engine reproduces the published solution exactly. The overlines are lost
when the PDF is read as text, and the solution's prose is what says which
actions are barred; they are written that way here.

| Term | Chain |
|---|---|
| a.b.0 \| ā.0 | → b.0 |
| a.0 \| b̄.0 \| b.ā.0 | → a.0 \| ā.0 → 0 |
| (a.b.0 + b.ā.0) \| ā.a.0 | → b.0 \| a.0, stuck |
| A⟨a⟩ \| A⟨b⟩ \| ā.b̄.b̄.ā.0 | four steps → A⟨a⟩ \| A⟨b⟩ |
| ((νa)a.b.0 + c.0) \| (ā.0 + b̄.0 + c̄.0) | → 0 |

The third is the interesting one: it stops after one step because the two
sides then offer `b` and `a`, which do not match. `all_tau_endpoints` follows
every choice rather than the first, which shows that the endpoint depends on
which branch of the sum is taken.

The fifth is the point of the restriction. The bound `a` on the left cannot
react with the `ā` on the right; only the pair `c` and `c̄` remains, and after
it both sides are `0`.
