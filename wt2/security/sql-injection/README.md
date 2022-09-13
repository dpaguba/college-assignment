# SQL injection

Demonstrated against a real sqlite3 database rather than described.

## The payload has to go in the right field

`' OR '1'='1` in the **name** field builds

```
SELECT * FROM users WHERE name = '' OR '1'='1' AND password = 'x'
```

and returns nothing. AND binds tighter than OR, so the password check
survives inside the second operand and no row has the password `x`. The
textbook payload in the textbook place fails.

The same string in the **password** field builds

```
SELECT * FROM users WHERE name = 'ada' AND password = '' OR '1'='1'
```

where the disjunction covers the whole condition, and all 2 rows come back.
`ada' --` in the name field works too, by commenting the password check away.

The parameterised query returns 0 rows for every one of these, because the
value reaches the database separately from the text of the statement and
cannot become part of it.

## Escaping by hand does not close it

Doubling the quotes leaves the numeric field open: `id = 1 OR 1=1` carries no
quotes to escape and the module measures 2 rows where 1 was asked for.

The one rule that holds: parameterised statements, always. Everything else,
least privilege for the database account and validation of the input, is a
second net.
