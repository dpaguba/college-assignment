# Syntax

Two constructs bind: the input `x(y).P` binds y in P, and the restriction
`(νx)P` binds x in P. The output `x̄⟨y⟩.P` binds nothing; it sends a name it
must already know.

## α-conversion and capture

Renaming a bound name is allowed only when the new name does not already
occur free. In `(νx)ȳ⟨x⟩.0` the name x is bound and y is free. Renaming x to
y gives `(νy)ȳ⟨y⟩.0`, in which the previously free y has become bound: the
term no longer talks to the outside world at all. `alpha_convert` refuses
that renaming and accepts a fresh one.

## The same name, free and bound

In `x(y).0 | ȳ⟨z⟩.0` the name y is bound on the left and free on the right,
and those are two different y. Whether two processes can talk to each other
depends entirely on which names they share freely, which is why `scope`
reports the three sets separately.

## Structural congruence

Six equations that reorder a term without changing it. They are not
decoration: the reaction rule only sees an output next to an input, so
without the congruence, whether a term can react would depend on how it was
written down.
