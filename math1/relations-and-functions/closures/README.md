# Closures

The closure of a relation under a property is the smallest relation
containing it that has the property. It exists because the property is
preserved by intersection, so there is a least one, and the module computes
it by adding what is missing until nothing is missing.

## The order matters

On the relation `1<2, 2<3, 3<4`:

```
symmetric then transitive   ->   an equivalence relation once made reflexive
transitive then symmetric   ->   not even transitive
```

Closing symmetrically first and then transitively gives the equivalence
closure. Doing it the other way round adds the reverses of the newly derived
pairs, and those reverses compose into pairs that are not there, so the
result loses the property that was just established.

That is the reason the equivalence closure is defined as symmetric, then
transitive, then reflexive, and not as the three closures in any order. A
minimality argument alone does not tell you the order; trying both does.
