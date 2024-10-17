# From the ER model to tables

Four rules, and the code applies them:

| In the diagram | In the schema |
|---|---|
| entity type | one table, its key becomes the primary key |
| n:m relation | its own table with both foreign keys as the key |
| 1:n relation | a foreign key on the n side, no new table |
| 1:1 relation | a foreign key on either side |
| attributes of a relation | into the relation's table |

The last row is the one that gets forgotten. An n:m relation with attributes,
such as the grade in `Besuch`, has nowhere else to go: the grade belongs to
the pair, not to the student and not to the course, so dropping the relation
table loses it.

`map_model` takes the two examples: Studierende and Vorlesung joined by an
n:m `Besuch`, which produces three tables; and Betreuer and Arbeit joined by
a 1:n `Betreuung`, which produces two, because the supervisor becomes a
column of the thesis.
