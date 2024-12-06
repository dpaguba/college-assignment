# Mesh structures

A triangle list draws a mesh and cannot edit one: nothing in it answers "which
faces touch this edge". The half-edge structure splits every edge into two
directed halves, one per adjacent face, each knowing its next, its twin and its
face. Walking around a face or around a vertex is then a pointer chase rather
than a search.

Boundary edges get a half-edge with no face, so walking around a boundary
vertex terminates. A mesh where an edge has more than two incident faces is not
a surface and is rejected at construction: `edge 0->1 used twice, mesh is not
orientable`.

## Euler characteristic as a free check

`V - E + F` depends only on the topology, so it catches holes and duplicated
vertices that no amount of looking at the geometry would show.

| mesh | V | E | F | V-E+F | genus |
|---|---|---|---|---|---|
| cube | 8 | 12 | 6 | 2 | 0 |
| tetrahedron | 4 | 6 | 4 | 2 | 0 |
| torus, 12 x 8 | 96 | 192 | 96 | 0 | 1 |
| two quads (a disc) | 6 | 7 | 2 | 1 | boundary |

Areas and volumes come out exact where they can be checked: 6.0 and 1.0 for the
unit cube, 1/6 for the tetrahedron, 4/3 for the octahedron. The volume is
computed by the divergence theorem and is independent of where the origin sits,
verified at shifts of 0, 5 and -100.

## Vertex normal weighting is not obvious

Three ways to average the incident face normals, measured against the exact
radial normals of a UV sphere, in worst-case degrees:

| mesh | angle | plain mean | area |
|---|---|---|---|
| 8 x 24 | **0.852** | 2.421 | 3.840 |
| 4 x 40 | **0.760** | 4.796 | 6.285 |
| 6 x 60 | **0.425** | 3.094 | 4.676 |
| 16 x 16 | **0.686** | 1.306 | 2.154 |

Angle weighting wins everywhere, and area weighting, the intuitive choice, is
the worst of the three: the thin triangles near the poles have tiny areas but
still represent real surface direction. On an evenly triangulated icosahedron
all three agree to 1e-6 degrees, which is why the choice only shows up on the
meshes that were already hard to shade.

## Loop subdivision approximates, it does not interpolate

Applied to an octahedron with unit-length vertices:

| step | V | F | Euler | area | volume | worst dihedral angle |
|---|---|---|---|---|---|---|
| 0 | 6 | 8 | 2 | 6.928 | 1.333 | 70.53° |
| 1 | 18 | 32 | 2 | 3.294 | 0.492 | 58.03° |
| 2 | 66 | 128 | 2 | 2.631 | 0.382 | 44.21° |
| 4 | 1026 | 2048 | 2 | 2.456 | 0.353 | **21.93°** |

The surface does not inflate towards the sphere through the vertices; it
converges to a smooth limit surface strictly inside the original. Successive
changes shrink by a factor of about 0.22 each step, and the Euler
characteristic stays 2 throughout, which is what says the topology survived.
