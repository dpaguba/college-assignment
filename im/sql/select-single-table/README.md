# Queries over one table

The seven parts of exercise 1 in tutorial seven. Two of them are about
something other than syntax.

## DISTINCT

Part e asks for the customers' first and last names without duplicates. Two
customers in the table are called Otto Bachmann with different customer
numbers. Without DISTINCT the name appears twice, with it once, and which is
correct is settled by what the question asks for: it asks for names, not for
customers.

## The AND that means OR

Part g asks "which customers live in Dortmund and Bochum". Read literally
that is `ort = 'Dortmund' AND ort = 'Bochum'`, and it returns nothing,
because a column holds one value per row and no customer lives in two places.
The question means the union, and in SQL that is OR or IN.

`the_and_trap` runs both: zero rows against eight. It is worth running once,
because the empty result is the kind of answer that gets reported as "there
are none" rather than as "the query is wrong".
