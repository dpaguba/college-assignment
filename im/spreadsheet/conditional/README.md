# WENN, UND, ODER

The jubilee gift exercise of tutorial nine. A postcard goes to customers
registered since 2014 **and** with at most five purchases; a bouquet to
customers of more than four years **or** with more than five purchases this
year.

## The two rules partition the cases exactly

Read as one number of purchases, the second rule is the exact negation of the
first: `since >= 2014 and purchases <= 5` against `since < 2014 or purchases
> 5`. Checked over 132 combinations of year and purchase count, no customer
falls into both rules and none into neither. The case distinction in the
formula is then unnecessary, and a single WENN with the first condition does
the whole job.

## Unless they are two numbers

The sheet says "bisher nicht mehr als fünf Käufe" for the postcard and "mehr
als fünf Käufe in diesem Jahr" for the bouquet. Whether that is the same
number it does not say, and everything hangs on it. As two numbers the clean
partition breaks: a customer registered in 2016 with eight purchases in total
and two this year satisfies neither rule and gets nothing.

`readings` computes both and returns the difference rather than picking one.
The ambiguity is in the exercise, and hiding it in a choice of implementation
would be the wrong kind of tidiness.
