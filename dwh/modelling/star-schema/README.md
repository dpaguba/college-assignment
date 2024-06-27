# The star schema

One fact table, dimensions around it, no dimension joining another. A query
touches the fact table and the dimensions it filters on, and the number of
joins is the number of filters.

The shape exists because of the sizes. In the example the fact table has ten
million rows and every dimension together has fewer than fifteen thousand, so
the fact table is a thousand times the rest and every design decision is
about it.

That asymmetry is why the star is denormalised on purpose. Repeating a
category name across ten thousand product rows costs a fraction of a percent
of the schema and saves a join on every query that filters by category.
