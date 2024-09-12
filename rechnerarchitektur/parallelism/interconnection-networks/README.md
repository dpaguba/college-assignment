# Interconnection networks

Three numbers decide a topology: the **diameter** bounds latency, the
**bisection bandwidth** bounds throughput, and the **link count** is the price.
No topology wins all three.

At 64 nodes:

| topology | diameter | bisection | links | degree |
|---|---|---|---|---|
| bus | 1 | 1 | 1 | 1 |
| ring | 32 | 2 | 64 | 2 |
| mesh | 14 | 8 | 112 | 4 |
| hypercube | 6 | 32 | 192 | 6 |
| full | 1 | 1024 | 2016 | 63 |

The bus has the best diameter and the worst bandwidth, which is why it works
for four processors and not for forty. The full crossbar is quadratic in links
and cannot be built at scale.

## Degree is the constraint that decides real designs

A hypercube's degree grows with the logarithm of its size, so every doubling of
the machine changes the node. A mesh has degree four whatever its size, which
is why meshes are what actually get built and hypercubes are what get analysed.

## Routing a hypercube is trivial

The addresses encode the topology: the bits where source and target differ are
the dimensions to cross, in any order. That is why the diameter equals the
number of address bits, and the route is verified to flip exactly one bit per
hop.
