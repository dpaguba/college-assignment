# Polygon triangulation

A d-simplex is the simplest body of its dimension and has d + 1 vertices: a
point, a segment, a triangle, a tetrahedron.

The exercise's ten points read as a closed polygon enclose an area of exactly
5, and the vertices are given clockwise.

## Ear clipping

An ear is a convex corner whose triangle contains no other vertex of the
polygon. Cutting ears one at a time turns an n-gon into n − 2 triangles, here
8, and their areas sum to exactly the area of the polygon. That is checked on
the exercise polygon and on 40 random convex polygons.

## It is not a Delaunay triangulation

The triangles produced contain circumcircles with other vertices inside, so
the answer to the exercise's follow-up question is no. Ear clipping only asks
whether a corner can be cut, never whether the resulting triangle is
well-shaped, and it takes whichever ear it finds first.
