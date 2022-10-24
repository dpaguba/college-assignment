# Worst case execution time

The analysis walks the control flow graph and takes the most expensive path.
A loop without a bound makes the longest path infinite, so the question has
no answer, and the module raises rather than guessing. Loop bounds are the
information a tool cannot infer and a programmer has to supply.

## Measuring is not analysing

A measured maximum is a lower bound on the worst case: the worst input may
not have been among the ones tried. An analysed bound is an upper bound and
is pessimistic. The module reports both on the same program and the gap
between them, which is the price of soundness and the number a certification
process argues about.

## Why a cache makes it harder

A safe analysis assumes a miss whenever it cannot prove a hit, so the bound
grows with everything the analysis cannot see. A cache therefore makes the
average case faster and the provable worst case worse, which is why embedded
designs often prefer a scratchpad whose behaviour is fixed at compile time.
