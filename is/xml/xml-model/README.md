# The XML model

A document is an ordered tree; a relation is an unordered set. That single
difference drives the rest of the block: `<a><b/><c/></a>` and
`<a><c/><b/></a>` are different documents and would be the same relation.

A document is irregular when elements of the same name have different
structure, which the relational model does not allow at all: every row of a
table has every column.

## Well-formed against valid

Well-formed is a question about syntax: one root, properly nested and closed
elements, legal names. Valid is a question about a schema: does this document
have the elements a DTD or an XML Schema demands, in the order it demands.
`is_well_formed` answers only the first, and `<a></b>` fails it.
