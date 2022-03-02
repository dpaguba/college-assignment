# The dimension theorem

What a map collapses and what it reaches add up to where it started:

```
dim ker + dim im = dim source
```

Checked here for several matrices by computing both bases explicitly, and the
kernel basis is verified by applying the matrix to each vector and getting
zero.

## The consequences are the useful part

A map between spaces of equal dimension is injective exactly when it is
surjective, which is false without the dimension condition and is the reason
a square matrix is invertible as soon as its kernel is trivial.

A map into a space of smaller dimension is never injective, which is the
pigeonhole principle from the first block in a linear setting: three columns
in a two-dimensional target must have a dependency.

This is the vector space version of the homomorphism theorem from the algebra
block. The quotient by the kernel is isomorphic to the image, and for finite
dimensions that is exactly the statement that the dimensions add up, so the
two theorems are one theorem in two vocabularies.
