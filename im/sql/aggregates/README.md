# Aggregate functions

Exercise 3 of tutorial seven, and three places where an aggregate quietly
answers a different question than the one asked.

## Receipts or positions

Part d asks how many purchases a customer has made. Counting `kassenbon`
gives purchases; counting `k_position` gives the number of article kinds
bought. Both are numbers and only one answers the question.

## The timestamp

Part f asks for the number of receipts per date. The column holds a
timestamp, and grouping by it puts almost every receipt in a group of its
own: 25 groups instead of 20. Grouping has to happen on the day, which means
the first ten characters.

## COUNT and NULL

`COUNT(*)` counts rows, `COUNT(column)` counts values. As long as no column
is NULL the two agree, and the moment one is, they part company:
`count_ignores_null` empties one birth date and the two counts differ by one.
That is the point at which an average silently changes its denominator.
