# Data modelling

The ER model in the notation the course uses: (min,max) on every edge, and
(T/P, D/N) on every specialisation.

| Module | Topic |
|---|---|
| [entities-and-attributes](entities-and-attributes/) | entity types, attributes, candidate keys |
| [relationships](relationships/) | relations and the (min,max) notation |
| [cardinality-check](cardinality-check/) | testing a population against the cardinalities |
| [specialisation](specialisation/) | total or partial, disjoint or not |
| [er-to-relational](er-to-relational/) | from the diagram to tables |
| [data-quality](data-quality/) | what the project table gets wrong |

The advice the course puts first is worth keeping: when unsure whether an
attribute can be a key, picture the entity type as a table and write three
rows. Thomas Wagner, Thomas Wagner, Sabrina Müller settles the question about
names faster than any rule.
