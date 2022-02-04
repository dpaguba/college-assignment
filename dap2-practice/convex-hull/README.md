# Convex hull

The naive O(n³) hull. Practical sheet 4, task 4.2.

```
java SimpleConvexHull 5 678
Neue Aussenkante gefunden: (34.56, 60.49) -- (69.35, 11.01)
Neue Aussenkante gefunden: (69.35, 11.01) -- (20.47, 18.48)
Neue Aussenkante gefunden: (2.17, 54.35) -- (34.56, 60.49)
Neue Aussenkante gefunden: (20.47, 18.48) -- (2.17, 54.35)
(69.35, 11.01) -- (20.47, 18.48) -- (2.17, 54.35) -- (34.56, 60.49)
```

Needs the previous task:

```
javac -sourcepath ../points-and-lines -d out SimpleConvexHull.java
java -cp out SimpleConvexHull 5 678
```

## The algorithm

Every pair of points spans a candidate edge, and the pair is a hull edge exactly
when all the other points lie on one side of it. Testing one pair costs O(n) and
there are O(n²) pairs, so O(n³).

This is the definition of a hull edge, written out. Graham scan and the divide
and conquer hull both manage O(n log n), and one of them is in the
[dap2 library](../../dap2/divide-and-conquer/convex-hull/). The value of the
cubic version is that its correctness needs no argument.

## Collinear points

A point exactly on the candidate line is allowed, but only if it lies between
the two endpoints. A collinear point outside the segment means an endpoint is
not extreme, so the edge is interior to a longer hull edge and is rejected.
That single rule is the whole handling of collinear input, and it is what keeps
only the outermost points of a shared line. The second example on the sheet is
built to test exactly this: (1,1) and (2,2) sit inside the edge from (3,3) to
(0,0).

## Verification

Both examples match exactly, including the order in which the edges are
discovered and the point the final chain starts from. Reproducing that order
pinned down two things the prose leaves implicit: pairs are visited with i < j,
and the printed chain starts at the destination of the first edge found.
