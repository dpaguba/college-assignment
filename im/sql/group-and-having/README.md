# Grouping and HAVING

Exercise 4 of tutorial seven and exercise 1 of tutorial eight.

## The free space

The occupied space per warehouse is the sum of quantity times capacity
requirement. A warehouse holding nothing does not appear in `liegt_in` at all
and would drop out of an inner join, although it would be the warehouse with
the most free space. Hence the left join and `COALESCE(..., 0)`.

| Warehouse | Capacity | Free |
|---|---:|---:|
| Bochum | 75 | 5 |
| Dortmund | 150 | 64 |
| Dortmund Wambel | 100 | 67 |
| Witten | 250 | 136 |
| Essen | 300 | 169 |

## WHERE against HAVING

WHERE selects rows before grouping and therefore cannot contain an aggregate:
the sum does not exist yet. HAVING selects groups after grouping and sensibly
contains nothing else. A row condition written in HAVING gives the same
answer and more work, because the rows are grouped first and thrown away
afterwards.

Part 1d is the case that needs HAVING: only customers whose 2007 turnover
exceeds 1000 €.

## The word "different"

Part 4b asks how many **different** articles each seller has served. Without
DISTINCT the query counts the servings; with it, the article kinds. The same
article on two receipts is two servings and one article.
