# State elimination

From an automaton back to a regular expression: the other half of Kleene's
theorem.

Remove states one at a time. Deleting a state `q` with self-loop `s` turns each
pair of an incoming edge `x` and an outgoing edge `y` into a direct edge

```
x s* y
```

added to whatever label that pair already had. A fresh start and a fresh
accepting state are added first, so exactly those two survive and the final
read-off has one shape instead of four.

## The result is correct and ugly

```
a(a|b)*b   ->   (((a(a)*)b)((b|((a(a)*)b)))*)
(ab)*      ->   (eps|((a((ba))*)b))
```

Both describe the right language, and neither is what a human would write. The
size depends on the elimination order, and finding the order that gives the
shortest expression is itself a hard problem, which is why the module takes the
order as a parameter and defaults to a stable one rather than pretending to
optimise.

## Round trip

`round_trip` runs expression → automaton → determinise → minimise → expression
and compares the two languages. The expression that comes back is almost never
the one that went in; the language always is. On 120 random expressions the
round trip held every time.
