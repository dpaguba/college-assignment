# Average memory access time

    AMAT = hit time + miss rate * miss penalty

A cache with a 5% miss rate and a 100-cycle penalty spends five cycles per
access on misses and one on hits. The memory is five times more important than
the cache, which is not what "95% hit rate" suggests.

## Halving the miss rate and halving the penalty are the same thing

They are the two factors of one product, so both give exactly the same AMAT.
The hit time is what breaks the symmetry, because it is paid on every access:

| starting from hit 2, miss rate 0.10, penalty 100 | AMAT |
|---|---|
| base | 12.0 |
| half miss rate | **7.0** |
| half penalty | **7.0** |
| half hit time | 11.0 |

## A second level

One level with a 5% miss rate and a 100-cycle penalty gives 6.0. Adding a
second level with a 10-cycle hit time and a 40% local miss rate gives **3.5**,
because the penalty seen by the first level drops from 100 to 50.

The **global** miss rate is the product of the local ones: 5% times 40% is 2%.
A second-level cache missing 40% of the time sounds bad and lets only one
access in fifty reach memory.

## Accesses per instruction

Every instruction is fetched and some also load or store, so the factor is
above one and typically near 1.3. Leaving it out of the CPI contribution
understates the memory cost by a third.
