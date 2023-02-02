# DNS

No single server holds the mapping and none could. The name space is a tree,
each zone is served by its own machines, and a lookup walks down it.

| mode | queries for `cs.tu-dortmund.de` |
|---|---|
| iterative | **4**: root, `de`, `tu-dortmund.de`, the record |
| recursive | **1**, and the resolver does the walk |
| cached | **0** |

The cache is what makes the system affordable: without it the root servers
would see every lookup on the internet. Entries expire, and the simulation
shows the query count returning after the lifetime passes.

## Why UDP, and when not

A query and its answer usually fit in one datagram, so a TCP handshake would
triple the cost of the exchange. Above 512 bytes the server sets a truncation
flag and the client retries over TCP, which is also how zone transfers work.
One protocol for the common case and another for the rest is unusual and here
it is justified by the ratio between the two.
