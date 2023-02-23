# Contingency tables

The pizza data of the second sheet: three countries, five kinds, 340 thousand
sales a week. The same table answers three different questions depending on
what it is divided by.

| Divided by | Gives |
|---|---|
| the total | the joint distribution |
| the row total | the kinds within each country |
| the column total | the countries within each kind |

The numbers differ enough that using the wrong one is a visible error.
Germany's share of all Hawaii sales is 0.573; Hawaii's share of all German
sales is 0.145. Both are correct answers to different questions, and the
published solution computes both.

## Reproducing the published numbers

The solution divides the **rounded** relative frequencies by the **rounded**
margins. Doing the same division exactly gives 0.382 where the solution
prints 0.383, and the rounded rows no longer sum to one: Italy's conditional
row sums to 1.0034.

The module computes both paths and the tests check both, because reproducing
a published table means reproducing where it rounded, and knowing the exact
answer means not rounding at all.

## Expected counts

Row total times column total over the grand total is what independence would
predict, and it is the joint distribution obtained by multiplying the two
margins. Every measure of association in the next module reads the difference
between these and the observed counts.
