# Transformations

Three ways to turn uniform numbers into anything else.

**Inverse transform.** Apply the inverse distribution function. Exact,
one uniform per value, and needs the inverse to exist. For the exponential
distribution it is one logarithm.

**Rejection.** Draw in a box and throw away what falls outside the density.
Needs no inverse, and wastes a share of the draws equal to the empty part of
the box: for a triangular density under a box of height two the acceptance
rate is exactly one half, which the module measures.

**Convolution.** Add simpler variables. An Erlang variable of shape three is
three exponentials, which is why the shape parameter of an Erlang is a count
and not a number.

The Box-Muller transform is the case that fits none of the three tidily: two
uniforms become two normal values through a coordinate change, and there is
no inverse distribution function anywhere in it.
