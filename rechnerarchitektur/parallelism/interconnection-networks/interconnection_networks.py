"""Interconnection networks: the shapes and what each costs.

Connecting `n` processors is a trade between three numbers. The **diameter** is
the worst-case distance and bounds the latency. The **bisection bandwidth** is
how many links cross the worst cut and bounds the throughput. The **link count**
is what it costs to build.

No topology wins all three, and the table is the whole subject:

| topology | diameter | bisection | links |
|---|---|---|---|
| bus | 1 | 1 | 1 |
| ring | `n/2` | 2 | `n` |
| 2D mesh | `2(sqrt(n) - 1)` | `sqrt(n)` | `2n - 2 sqrt(n)` |
| hypercube | `log2 n` | `n/2` | `n log2(n) / 2` |
| full | 1 | `n^2/4` | `n(n-1)/2` |

The bus has the best diameter and the worst bandwidth, which is why it works
for four processors and not for forty.
"""

from __future__ import annotations

import math


def diameter(topology, nodes):
    """Worst-case hop count between two nodes."""
    if topology == "bus":
        return 1
    if topology == "full":
        return 1
    if topology == "ring":
        return nodes // 2
    if topology == "mesh":
        side = int(math.isqrt(nodes))
        return 2 * (side - 1)
    if topology == "hypercube":
        return int(math.log2(nodes))
    raise ValueError(f"unknown topology {topology}")


def bisection(topology, nodes):
    """Links crossing the worst cut of the network in half.

    The number that decides whether an all-to-all communication pattern scales.
    A bus has one link crossing any cut, so every processor added makes the
    contention worse; a hypercube has `n/2`, so it does not.
    """
    if topology == "bus":
        return 1
    if topology == "ring":
        return 2
    if topology == "mesh":
        return int(math.isqrt(nodes))
    if topology == "hypercube":
        return nodes // 2
    if topology == "full":
        return (nodes // 2) ** 2
    raise ValueError(f"unknown topology {topology}")


def links(topology, nodes):
    """How many links the topology needs."""
    if topology == "bus":
        return 1
    if topology == "ring":
        return nodes
    if topology == "mesh":
        side = int(math.isqrt(nodes))
        return 2 * side * (side - 1)
    if topology == "hypercube":
        return nodes * int(math.log2(nodes)) // 2
    if topology == "full":
        return nodes * (nodes - 1) // 2
    raise ValueError(f"unknown topology {topology}")


def degree(topology, nodes):
    """Links per node, which is what a chip's pin budget limits.

    The reason a hypercube is not used beyond a few hundred nodes: its degree
    grows with the logarithm of the size, so every doubling of the machine
    changes the node design. A mesh has degree four whatever its size, which is
    why it is what actually gets built.
    """
    if topology == "bus":
        return 1
    if topology == "ring":
        return 2
    if topology == "mesh":
        return 4
    if topology == "hypercube":
        return int(math.log2(nodes))
    if topology == "full":
        return nodes - 1
    raise ValueError(f"unknown topology {topology}")


def hypercube_route(source, target):
    """The path from one node to another, flipping one bit at a time.

    Routing in a hypercube is trivial precisely because the addresses encode
    the topology: the differing bits are the dimensions to cross, and any order
    works. That is why the diameter equals the number of address bits.
    """
    route = [source]
    current = source
    difference = source ^ target
    bit = 0

    while difference:
        if difference & 1:
            current ^= (1 << bit)
            route.append(current)
        difference >>= 1
        bit += 1

    return route


def compare(nodes):
    """The whole table for one machine size."""
    return {topology: {"diameter": diameter(topology, nodes),
                       "bisection": bisection(topology, nodes),
                       "links": links(topology, nodes),
                       "degree": degree(topology, nodes)}
            for topology in ("bus", "ring", "mesh", "hypercube", "full")}
