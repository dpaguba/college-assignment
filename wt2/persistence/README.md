# Persistence

Objects onto rows: what identity means, how a relationship becomes a column,
when the children are loaded, when the changes are written, and what happens
when two transactions write the same row.

Two measurements carry the block. The n+1 problem shows up as 4 queries where
1 would do, and the lost update shows up as a change that vanishes without
any error being raised.
