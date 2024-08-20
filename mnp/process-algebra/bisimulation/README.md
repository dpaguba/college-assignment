# Bisimulation

Two notions of "the same behaviour", and the pair that separates them.

```
P = a.(b.0 + c.0)        Q = a.b.0 + a.c.0
```

Both have exactly the same four traces of length up to three. They are not
bisimilar, and the witness is the trace `a`: after it, P still offers both `b`
and `c`, while Q has already committed to one of them. Trace equivalence
cannot see the moment of commitment, and bisimulation is defined so that it
can.

| Question | Trace equivalence | Bisimulation |
|---|---|---|
| same sequences possible | yes | yes |
| same choices at every point | not asked | required |
| P and Q above | equivalent | distinguished |

## Why the stronger notion is the useful one

A vending machine that takes your coin and then decides whether it sells tea
or coffee has the same traces as one that lets you choose after paying. As a
customer the difference is the whole product. Any property that depends on
what remains available after a partial run needs bisimulation, and that covers
deadlock freedom, since a trace that ends says nothing about whether it had to
end.

## Weak bisimulation

`a.0` and `tau.a.0` are not strongly bisimilar, because one can do a `tau` and
the other cannot. They are weakly bisimilar, which is the version that treats
internal steps as unobservable. That is the equivalence a specification
actually wants: an implementation is allowed to take internal steps a
specification never mentions, as long as what an observer sees is unchanged.

Unobservable does not mean ignorable. `tau.a.0 + tau.b.0` and `a.0 + b.0` have
the same observable traces and are not weakly bisimilar, because the first
commits internally before anyone can choose. The definition catches this only
if a `tau` move must still be answered, by zero or more `tau` moves on the
other side; dropping that clause makes the two look equal and erases the
distinction between an internal decision and an offered choice.

Seven pairs check out against the textbook, including the expansion law:

| | | |
|---|---|---|
| `a.0` | `tau.a.0` | weakly bisimilar |
| `a.tau.b.0` | `a.b.0` | weakly bisimilar |
| `tau.tau.a.0` | `a.0` | weakly bisimilar |
| `a.0 \| b.0` | `a.b.0 + b.a.0` | weakly bisimilar |
| `tau.a.0 + tau.b.0` | `a.0 + b.0` | distinguished |
| `tau.0 + a.0` | `a.0` | distinguished |
| `a.(b.0 + c.0)` | `a.b.0 + a.c.0` | distinguished |
