# Net structure

Places hold tokens, transitions move them, and a transition fires only when
every input place has enough. Everything else in this block is a consequence
of that one rule.

```
P1 --> T1 --> P2 --> T2 --> P4
 |                            ^
 +---> T3 --> P3 --> T4 ------+
```

With one token in P1, T1 and T3 are both enabled and only one can fire. They
share an input place holding a single token, which is conflict. Two
transitions that share no input place and are both enabled are concurrent, and
nothing has to declare that: independence is read off the structure.

## Conflict needs the marking

Sharing an input place is not sufficient on its own. If that place holds two
tokens, both transitions can fire, and there is no conflict to resolve. The
check therefore consults the marking and the arc weights together, which also
makes it correct for nets where an arc consumes more than one token.

## Why empty places are dropped

A marking is stored as the places that hold tokens. Two descriptions of the
same state are then equal without normalising, which matters because markings
are used directly as nodes of the reachability graph, and a graph that
distinguishes `{P1: 1}` from `{P1: 1, P2: 0}` would never terminate on a net
that empties a place and refills it.
