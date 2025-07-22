# Linear programming

The tenth sheet's production problem:

```
max  3x₁ + 4x₂
     3x₁ + 2x₂ ≤ 1200   (machine hours)
     5x₁ + 10x₂ ≤ 3000  (raw material)
            x₂ ≤ 250    (market)
     x₁, x₂ ≥ 0
```

The published optimum is 300 and 150 for a profit of 1500, and the module
reproduces it. The first two constraints are binding and the third is not,
which the module also reports and which the duality module then explains.

The optimum is at a vertex because the region is convex and the objective is
linear, so enumerating the vertices solves the problem. That is exponential
and exact, and for the two-variable problems of the lecture it is the right
trade. The simplex method is the refinement that walks between vertices along
improving edges instead of visiting them all.

An unbounded problem has vertices too, so vertex enumeration alone cannot
detect one. The module adds a large box and checks whether the optimum sits
on it, which is the practical test.
