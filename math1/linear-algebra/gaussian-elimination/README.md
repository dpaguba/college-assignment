# Gaussian elimination

Every entry is an exact fraction, so a pivot is zero only when it really is
zero. In floating point the same computation has to decide whether a small
number is a rounding error or a value, and that decision is the whole
difference between numerical linear algebra and the version the lecture
proves theorems about.

## The main theorem, as two ranks

| | |
|---|---|
| rank(A) < rank(A\|b) | no solution |
| rank(A) = rank(A\|b) < unknowns | infinitely many |
| rank(A) = rank(A\|b) = unknowns | exactly one |

The solution set is returned as a particular solution and a basis of the
kernel, which is the same information as the geometric description: a point,
plus the directions one may move without leaving the solution set. Every
returned solution is checked by substitution, and every kernel vector by
substituting into the homogeneous system.

## Two echelon forms

The plain echelon form depends on the order the rows are processed in. The
reduced form does not: two matrices with the same row space have the same
reduced form, which is checked here by eliminating the same system with its
rows in two orders and comparing. That uniqueness is why the reduced form is
the one used to decide whether two systems describe the same solutions.

Verified against numpy on 200 random systems: the same classification into
none, one and many, every time.
