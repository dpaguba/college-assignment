# The snowflake

Normalising the dimensions into chains of tables.

| | star | snowflake |
|---|---:|---:|
| bytes | 200 754 000 | 200 556 000 |
| joins for a category filter | 1 | 2 |

The saving is 0.1 percent of the schema and the cost is a join on every
query that reaches the normalised attribute. That ratio is the argument, and
it comes from the sizes: normalisation removes repetition, the repetition is
in the dimensions, and the dimensions are the small tables.

The fact table is never normalised. It has the rows and no repeating
attributes to remove, so the technique that saves space in an operational
database has nothing to work with in a warehouse.
