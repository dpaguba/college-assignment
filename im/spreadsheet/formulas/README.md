# Formulas

A small evaluator: numbers, cell references, ranges inside SUMME, the four
operations, brackets, and named ranges substituted before evaluation.

## The receipt

Eight food items and two non-food, a VAT rate of 19 % in D22, gross prices
computed from net prices, two subtotals and a grand total. Net 55.31 €, gross
65.82 €, food share 31.5 %.

## The three ways to the total

Part e of the exercise asks for three ways to reach the gross total, and the
interesting question is which of the three checks anything.

1. the sum of the two subtotals;
2. the sum over all gross prices;
3. the net total times one plus the rate.

The first two use the same gross values and therefore go wrong together if a
gross formula is wrong. Only the third computes past the gross block, from
the net side. It is the check; the other two are two spellings of the same
sum.

On the correct sheet all three agree to within 1.4·10⁻¹⁴, which is floating
point and not a discrepancy.
