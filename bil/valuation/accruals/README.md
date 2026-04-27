# Accruals and provisions

Payment and result fall in different periods. Which item arises depends on
which comes first and in which direction, and the table is small and still
regularly confused.

| | Payment first | Result first |
|---|---|---|
| we pay | aktiver RAP | liability or provision |
| we receive | passiver RAP | receivable |

300 € paid for three months with one month falling in the old year splits into
100 € expense this year and 200 € carried forward. Expense follows time, not
payment.

## The parameter that did nothing

The first version took a `months_in_year` argument, ignored it, and hard-coded
one month into the current year. The name was also misleading. It is now
`months_this_year`, it is used, and a value above the months paid for is
rejected.

## When a provision is booked

An obligation towards a third party, probable, and measurable. Take away the
probability and it belongs in the notes as a contingent liability; take away
the measurability and the same. Both tests have to hold.

## Why they are the soft spot

The estimate comes from the company. Whoever wants to dampen the result
estimates cautiously; whoever wants to lift it releases the provision next
year. Both stay within what is arguable, both are hard to audit, and that is
why provisions are read as a development over several years rather than as a
figure at one date.
