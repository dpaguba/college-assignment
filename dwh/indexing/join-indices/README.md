# Join indices

Store the result of the join rather than computing it. A join becomes a
lookup, and the price is space and maintenance: every load updates the index
as well as the tables.

The saving grows with the fact table, because the join it replaces does, and
the maintenance grows with the load rather than with the table. That is why
the trade favours a warehouse: a large table, loaded once a night, queried
all day.

It is also why the same index is a poor choice in an operational database,
where the table is smaller and the writes are constant.
