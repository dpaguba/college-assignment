# Order intake

The first exercise of tutorial one, and the part worth implementing is the
shipping table:

| Order value | New customer | Existing customer |
|---|---|---|
| < 100 € | Rechnung | Rechnung |
| >= 100 €, < 1000 € | Nachnahme | Rechnung |
| >= 1000 € | Nachnahme | Nachnahme |

Read in one sentence: below a hundred always on account, from a thousand
always cash on delivery, and in between the status decides. The new customer
pays on delivery because the company does not know them yet.

## The connectors of the process

Two of the three are AND, and both are easy to get wrong. When the documents
are not in order, the order is cancelled **and** the customer is informed:
both happen, so it is a parallel split and not an exclusive one. When they
are in order, customer status **and** order value are determined at the same
time, and both are needed before the shipping type can be looked up.

Only the check itself branches exclusively.

## The boundaries

`the_boundaries` tests the four values either side of the two thresholds. The
table says `>=100` and `>=1000`, so 100 € is already the middle row and
1000 € already the bottom one. Reading them as `>` gives the wrong shipping
type for exactly those two values, which are the two a test looks at first.
