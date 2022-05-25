# Reduction

One rule. An output and an input on the same channel, side by side, both
prefixes vanish and the transmitted name is substituted for the bound name in
the body of the input.

`x̄⟨z⟩.0 | x(y).ȳ⟨w⟩.0` reduces to `z̄⟨w⟩.0`. The receiver now sends on z, a
channel it did not know before. In CCS that cannot be written down.

## Scope extrusion, and its side condition

Before the rule applies, restrictions at the top level are pulled outward, so
that an output inside a restriction and an input outside it end up next to
each other. That is `(νx)(P | Q) ≡ P | (νx)Q` read backwards, and it is what
makes the list encoding of the next module work at all.

The rule has a condition: x must not be free in the parts it is pulled over.
A first version of the engine ignored it, and then `(νx)x̄⟨z⟩.0 | x(y).0`
reacted, which is exactly what a restriction is for preventing. The bound
name is now renamed first when it clashes, and the two sides correctly stay
apart. Both cases are tested, because the fix has to preserve the first one.

## Replication does not terminate

`!x̄⟨z⟩.0 | !x(y).0` reduces for ever: every reaction leaves both replications
standing. The module reports reaching its step limit as a probable infinite
computation rather than returning the term it happened to stop at.
