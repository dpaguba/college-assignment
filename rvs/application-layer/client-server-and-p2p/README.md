# Client-server and peer-to-peer

Distributing a file to `n` clients from one server takes at least `n` copies
out of the server's uplink, which is linear in `n`. In a peer-to-peer
distribution every peer uploads what it has, so the capacity grows with the
demand.

With a file of size 1, a server rate of 2 and a peer rate of 1:

| peers | client-server | peer-to-peer |
|---|---|---|
| 1 | 1.0 | 1.0 |
| 10 | 5.0 | 1.0 |
| 100 | 50.0 | 1.0 |
| 1000 | **500.0** | **1.0** |

The crossover is at **3** peers, which is much lower than intuition suggests
and is why the architecture is a function of scale rather than of taste.

## Three bounds instead of one

The client-server time is the larger of two bounds and the peer-to-peer time
the largest of three: the server must send one copy, the slowest peer must
receive one, and the total upload capacity must carry `n` copies. The third
grows in both numerator and denominator, which is why the curve flattens
instead of rising.
