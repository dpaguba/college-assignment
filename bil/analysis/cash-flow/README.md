# The cash flow statement

The indirect method starts at the result and takes back everything that
changed the result without moving money, and everything that moved money
without touching the result.

| Area | € |
|---|---:|
| operating | 80 000 |
| investing | −65 000 |
| financing | −2 000 |
| change in cash | **13 000** |

## The check

The three areas sum to the change in the cash balance, and that has to equal
the difference between the bank balances of two balance sheets. The module was
checked against a direct computation built from payment flows: five hundred
random sets of transactions, and in every one the indirect statement returned
the same change in cash and the same operating figure as the payments
themselves. If the two disagree, a position is missing, and the difference
says how large it is.

## Reading the three signs together

| Pattern | Usual reading |
|---|---|
| + − − | the business carries investment and repayment |
| − − + | a young company living on its investors |
| + + − | a retreat: sell what there is and repay |
| + − + | strong growth financed from both sources |

## Why it is harder to dress up

It knows no valuation options. A different depreciation method changes the
result and is added straight back, so the cash flow does not move. What can be
moved is the timing of payments, and timing can be shifted but not invented.
That is why a rising profit next to a falling operating cash flow is the best
known warning sign in balance sheet analysis, and why the answer is usually
that the profit is sitting in receivables and inventory.
