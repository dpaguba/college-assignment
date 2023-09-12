# The branch target buffer

A direction predictor says **whether** a branch is taken. It does not say
where to fetch from, and computing the target needs the instruction decoded,
which is at least one cycle after the fetch that needs it.

A branch target buffer caches the target, indexed by the branch's own address,
so a hit lets the very next fetch go to the right place.

## Two failure modes with different costs

    penalty = (1 - hit rate) * miss penalty
            + hit rate * (1 - accuracy) * misprediction penalty

A buffer miss is cheap: the target is merely late. A wrong direction is
expensive: work was done and must be discarded. Once the hit rate is high, the
second term dominates, which is why effort goes into direction accuracy rather
than buffer size.

## Direct mapping has the usual consequence

Two branches whose addresses map to the same entry evict each other on every
execution, so a loop containing two branches can perform worse than one
containing three. Measured directly: with four entries, addresses `0x100` and
`0x110` collide and neither is ever found; with eight, both stay.
