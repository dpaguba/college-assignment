# DML

The population and the three exercises that change it.

## UPDATE

The customer moving house changes four columns in one statement, not four
statements. The price rise is computed **in** the database, `preis = preis +
?`, rather than read, added and written back: between the read and the write
another transaction can get in.

The most common mistake with UPDATE is the missing WHERE. `UPDATE artikel SET
preis = 0` is syntactically perfect and moves every price to zero without a
warning. The habit that prevents it: run a SELECT with the same WHERE first,
look at the rows, then change the verb.

## DELETE

Retiring a seller is where referential integrity becomes concrete. `betreut`
points at the seller; deleting the seller leaves those references pointing at
nothing. `retire_seller` deletes the referencing rows first and reports how
many there were, which is the manual version of ON DELETE CASCADE.

Removing an article touches three tables, removing a warehouse two. In both
cases the function returns how many rows went with it, because a delete that
silently takes twelve other rows is worth knowing about before it runs.

## The population

The schema comes from the tutorial; the data does not. The sheets show a few
rows and the rest lived on the course platform, while the exercises reference
receipt 23, customers 10 and 11, article 6 and turnover for 2007. The
population here is extended to cover them: eleven customers, six articles,
five warehouses, three sellers, twenty-five receipts across 2006 and 2007,
thirty-five receipt positions.
