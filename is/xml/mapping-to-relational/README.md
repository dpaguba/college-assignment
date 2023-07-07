# Mapping XML to tables

Shredding turns every element of one name into a row and every child element
into a column. On a regular document that works exactly; on an irregular one
the missing children become nulls, which is the relational model's way of
saying that the structure was not uniform.

Two things are lost. The order of the siblings, because a table is a set of
rows and would need an extra column to keep it. And the nesting: each level
with repeated children needs its own table and a foreign key upwards, so a
document three levels deep needs two tables.

## The three approaches

Shredding gives a schema that SQL can query and loses the document.
Storing the document as a single value keeps it exactly and makes queries
opaque. A native store keeps the tree and gives up the relational optimiser.
Which is right depends on whether the document or the query is the thing that
matters.
