# Partial orders

An order that leaves pairs incomparable, which is the normal case: divisors
of 12 under divisibility, subsets under inclusion, tasks under dependency.

The Hasse diagram is the cover relation, the pairs with nothing strictly
between them. Divisibility on the divisors of 12 relates 1 to 4, and 1 does
not cover 4, because 2 sits between them. Drawing only the covers loses
nothing, since the order is their transitive closure, and it is the reason
the diagram is readable at all.

## Counts on the subsets of a three-element set

| | |
|---|---:|
| elements | 8 |
| longest chain | 4 |
| widest antichain | 3 |
| linear extensions | 48 |

The longest chain is the empty set up to the full set, one element at a time.
The widest antichain is the three singletons, or the three pairs. The 48
linear extensions are the orders in which the subsets can be listed so that
no set comes before a subset of it, which is the number of valid topological
sorts.

That last number is why a topological sort is a choice. A total order has
exactly one linear extension; this order has 48, and any of them is a correct
answer to "in what order may these be processed".
