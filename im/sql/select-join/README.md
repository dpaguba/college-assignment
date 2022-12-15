# Queries over several tables

Exercise 2 of tutorial seven, plus the two cases the exercise does not ask
for and that decide whether joins are understood.

## The rows without a partner

An inner join returns only rows that have a partner. `articles_never_sold`
asks the opposite question: which articles are on no receipt. That needs a
left join and a test for NULL, or a NOT IN.

On this population the answer is empty: every article has been sold at least
once. An empty result is a result, and this is the query where that is worth
saying out loud, because the same query on a real catalogue is how dead stock
gets found.

## The forgotten join condition

`the_missing_join_condition` runs `SELECT COUNT(*) FROM kunde, lager` and
gets 55: every customer paired with every warehouse. The result looks like
data and is not. On eleven and five rows it is obvious; on a million and a
thousand it appears first as a query that does not finish, and only then as a
mistake.
