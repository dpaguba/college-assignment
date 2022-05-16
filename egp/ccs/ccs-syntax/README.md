# Syntax

Six operators, and the whole calculus is built from them.

| | |
|---|---|
| `0` | does nothing |
| `α.P` | offers α and becomes P |
| `P + Q` | behaves as one of them, and the other is discarded |
| `P \| Q` | both run, and they may react with each other |
| `(νa)P` | the name a is private inside P |
| `A⟨a⟩` | a call, which is how repetition is expressed |

## Scope, and a bug it caused

`visible_names` computes which names a process can react over from outside.
The first version subtracted every restricted name from every occurring name,
which is wrong, because a restriction only binds inside its own scope. In
`((νa)a.b.0 + c.0) | ā.0` the name a is bound on the left and free on the
right; it is visible, and the restriction only stops the two sides from using
it *with each other*.

That distinction is the whole content of exercise 4e, so getting it wrong in
the module that explains it would have been unfortunate. The function now
recurses and removes each bound name from its own subterm only.

## Sum against parallel

The pair most easily confused. `a.0 + b.0` offers a or b, and taking one
loses the other. `a.0 | b.0` offers both and keeps the second after the
first. The difference appears only at the second step, which is why the
language cannot see it and the transition graph can.
