# Network layer

| Topic | |
|---|---|
| [ip-addressing](ip-addressing/) | prefixes, subnetting, the two reserved addresses |
| [distance-vector](distance-vector/) | routing by gossip, and count to infinity |
| [link-state](link-state/) | routing by flooding a map |
| [forwarding](forwarding/) | longest prefix match and aggregation |

Two published solutions from the course are reproduced here: the subnet
allocation of `9.23.96.0/20` and the convergence of the distance vector tables
on the five-node network.

The split between **routing**, computing where things should go, and
**forwarding**, sending each packet there, runs through all four: the first two
modules compute, the last one looks up, and the addressing module is what makes
the lookup summarise instead of enumerate.
