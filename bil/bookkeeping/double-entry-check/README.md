# The double-entry check

Every entry touches two accounts with the same amount, so the accounting
equation survives each one. The module applies a sequence of entries to an
opening balance sheet and checks the equation after every step, not only at
the end.

## The sign error the check caught

Expense and revenue accounts do not appear in the balance sheet: they move
equity. The first version debited equity for an expense and also debited it
for a revenue, which made the two sides come out at 181 000 against 151 000
after five entries. Both now use one formula with the sign of the side:

```python
for account, sign in ((debit, 1), (credit, -1)):
    ...
    changed["Eigenkapital"] -= sign * amount
```

An expense on the debit side lowers equity, a revenue on the credit side
raises it. With the fix, the five example entries take equity from 120 000 to
123 000, which is 15 000 revenue less 2 000 rent less 10 000 depreciation, and
both sides come out at 181 000.

## What the check is worth

Two thousand random sequences of eight entries each over every account in the
chart keep the equation. That is what the check guarantees and all it
guarantees.

## What it never catches

A booking to the wrong account of the right kind, a booking that was never
made at all, a booking made twice, and a wrong amount used on both sides. All
four leave the equation intact. A one-sided entry does break it, and the
difference is exactly the missing counter-entry: adding 3 000 € to the bank
account alone leaves the two sides 3 000 € apart.
