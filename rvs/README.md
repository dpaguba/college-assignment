# Rechnernetze und verteilte Systeme

Fifteen modules in five blocks, one per layer plus security.

| Block | |
|---|---|
| [application-layer](application-layer/) | HTTP, DNS, client-server against peer-to-peer |
| [transport-layer](transport-layer/) | reliable transfer, TCP connections, congestion control |
| [network-layer](network-layer/) | addressing, routing, forwarding |
| [link-layer](link-layer/) | error detection, medium access, switching |
| [security](security/) | ciphers, hashes, certificates |

The Java client and server from the practical are in
[rvs-practice](../rvs-practice/).

## The two published solutions, reproduced

The course publishes solutions for two homework tasks and both come out:

**Subnetting.** `9.23.96.0/20` split among eleven networks gives the published
prefixes for all seven host subnets, `9.23.96.0/21` through `9.23.110.64/27`,
and four `/30` links. The block ends up 90.2% used.

**Distance vector.** The five-node network converges to the published table,
and every entry agrees with Dijkstra run on the same graph, which is the check
that matters: the two algorithms compute the same thing by completely different
means.

## Numbers worth keeping

| | |
|---|---|
| ten objects over HTTP at 100 ms round trip | 2000 ms non-persistent, **200 ms** pipelined |
| peer-to-peer overtakes client-server at | **3** peers |
| stop and wait on a 30 ms link | **0.03%** utilisation |
| window needed for 1 Gbit/s at 30 ms | **3.75 MB** |
| slotted ALOHA against pure | 0.368 against **0.184** |
| Ethernet minimum frame at 10 Mbit/s | **512 bits**, which is the 64-byte rule |
| symmetric keys for 10 parties | **45**, against 20 asymmetric |

## One thing found while building this

The Java sources in the practical would not compile: a trailing
`# Modified 2025-08-11` line had been appended to each file, which is not valid
Java. Removing it from the three files made them compile. The same line appears
in roughly two hundred other files across the repository.
