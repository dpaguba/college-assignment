# Joins

Five presidents, four elections. The inner join on the president's name
returns 4 rows; the left join returns 7, because the three presidents with no
election in the table keep their row and get nulls for the missing columns.

## The cost of a forgotten condition

`SELECT * FROM presidents, elections` returns 20 rows, the full product.
Adding `WHERE e.president = p.name` returns 4. The result is not merely
wrong, it grows with the product of the table sizes, which is how a forgotten
condition turns into a query that never finishes on real data.

A self join compares rows of one table to each other: the pair of presidents
whose terms are consecutive comes out of `presidents a, presidents b` with
`a.term = b.term + 1`. The join is commutative, and the module checks it by
running both orders and sorting the results.
