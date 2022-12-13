# DDL

Nine tables with their keys and foreign keys, exactly the schema of tutorial
five.

`ALTER TABLE` covers the three parts of the first exercise of tutorial six:
the customer gets a second forename, the warehouse gets an address, and the
second forename is dropped again because nobody used it. Dropping a column
was impossible in most systems for a long time, and the standard workaround
was a new table, a copy and a rename; sqlite has done it directly since 3.35.

## The order

Referential integrity decides it. A table with a foreign key can only be
created once its target exists, so the four tables without references come
first and the five that point at them come after. Dropping reverses the
dependency: removing the target first would leave references pointing at
nothing, and a database with the check switched on refuses.
