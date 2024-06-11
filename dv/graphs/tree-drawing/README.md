# Tree drawing

The simple level algorithm places the vertices of each depth side by side.
The width then grows with the number of vertices on the widest level, whether
or not the tree needs it.

Reingold and Tilford draw the subtrees separately and push them together as
far as their contours allow, then centre each parent over its children.

## The properties, checked

On 60 random trees: no two vertices of a level are closer than the minimum
spacing, and every parent sits exactly at the midpoint of its outermost
children. Two subtrees of the same shape get the same relative coordinates,
so the drawing does not depend on where in the tree the shape occurs. A
symmetric tree comes out symmetric.

On a narrow tree the width comparison shows the difference: the simple
algorithm spends the width of the widest level, Reingold-Tilford only what
the contours require.
