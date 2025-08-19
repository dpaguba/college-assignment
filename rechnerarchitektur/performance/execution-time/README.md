# Execution time and CPI

    time = instructions * CPI / clock rate

Every architectural change moves one factor at the expense of another: a richer
instruction set lowers the count and raises the CPI, a deeper pipeline raises
the clock and the branch penalty. Only the product decides.

## A machine does not have a CPI

It has one per program. The average is weighted by the instruction mix, so
speeding up loads by a factor of two moves the CPI from 1.7 to 1.4 for a mix
that is 30% loads, and not at all for one that has none.

## MIPS can rank two machines the wrong way

2 MIPS at 1.0 seconds against 1.11 MIPS at 0.9 seconds: the second machine is
slower by the metric and finishes first. MIPS counts instructions, and
instructions are not work.

## Which mean

| quantity | mean |
|---|---|
| times | arithmetic |
| rates | harmonic |
| normalised ratios | **geometric** |

The geometric mean of 1 and 4 is 2, not 2.5. It is the only one of the three
that does not change the ranking when the baseline machine changes, which is
why SPEC uses it and why an arithmetic mean of speedups is a reporting error
rather than a rounding one.
