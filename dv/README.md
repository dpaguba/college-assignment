# Datenvisualisierung

Thirty-seven modules across eight blocks, covering both halves of the course:
the introduction to data visualisation and the applied part for medical
physicists.

The exercise sheets are in R, which is not installed here, so the algorithms
are implemented in Python and checked against numpy and networkx. No solution
sheets were published, so every result had to be verified against something
independent.

## The exercises, worked out

- Principal axes of (0,1), (1,1), (2,1), (3,2) through the characteristic
  polynomial λ² − (23/12)λ + 1/6: eigenvalues 1.8254 and 0.0913, with
  **95.24 %** of the variance on the first axis.
- The fifteen-vertex digraph: order 15, size 22, one source, one sink, not
  acyclic (4 → 6 → 13 → 4), not planar.
- The ten points: convex hull A, J, I, H, G, F; polygon area 5; ear clipping
  gives 8 triangles which are not a Delaunay triangulation; the α-shape at
  α = −0.5 coincides with the hull boundary and first differs at α = −1.
- Marching squares on the unit circle: every vertex within 0.056 cell widths.
- The 24-person table: total entropy 4.5016 bits, gender gain 0.8709 with
  partial entropies 2.5216 and 4.0875, hair colour the best attribute at
  2.2894, and **two pairs of people that no tree can tell apart**.
- Equivalence needs two layers; the hulls of its two classes meet at
  distance 0.
- The concentration experiment in 9 runs instead of 27; the helicopter in 8
  instead of 16, at resolution IV.

## Measurements worth keeping

- Rounding the marching-squares ratio to one decimal, as the sheet asks, puts
  a floor under the accuracy: by 21 grid points the rounded contour is 3.6
  times worse than the exact one.
- Equidistant interpolation of the Runge function has a largest error of 7.19
  against 0.047 for Chebyshev nodes.
- Douglas-Peucker keeps more points than necessary in 35 of 180 random cases.
- k-means with eight restarts still misses the exhaustive optimum in 3 of 40
  random instances.
- Runge-Kutta is 6·10⁷ times more accurate than Euler on a closed orbit at
  628 steps; measured orders 1.04 and 4.00.
- A 512 × 512 arrow plot at a readable spacing shows one value in 256.
