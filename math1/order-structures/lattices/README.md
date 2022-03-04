# Lattices

An order in which every pair has a supremum and an infimum, which is equally
a set with two operations obeying four laws.

The two descriptions are the same because of absorption. Idempotence,
commutativity and associativity say nothing about how join relates to meet;
absorption is the law that ties them, and from the two operations the order
can be recovered as "a is below b when a join b is b".

## The two smallest counterexamples

```
   diamond (M3)              pentagon (N5)
        1                          1
      / | \                      /   \
     a  b  c                    b     c
      \ | /                     |    /
        0                       a   /
                                 \ /
                                  0
```

The diamond is modular and not distributive. The pentagon is neither. Those
two facts are a complete answer to both questions: a lattice is modular
exactly when it contains no pentagon, and distributive exactly when it
contains neither. Both are checked here over every triple.

The divisor lattices show the same thing arithmetically. Divisors of 12 form
a distributive lattice with join the least common multiple and meet the
greatest common divisor, and the distributive law there is a statement about
prime exponents, one prime at a time.
