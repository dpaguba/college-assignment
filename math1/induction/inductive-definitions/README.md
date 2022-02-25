# Inductive definitions

An inductive definition names some elements and gives rules that make new
ones. The set defined is the smallest one closed under the rules, and that
phrase is a computation: apply the rules until nothing new appears.

Terms over a signature are the example the course returns to. Two constants
and one binary operation give

| nesting | 0 | 1 | 2 |
|---|---:|---:|---:|
| terms | 2 | 6 | 38 |

The recurrence is t(n+1) = c + t(n)², since a term of the next depth is a
constant or the operation applied to two terms of the current one. Writing 6 +
36 = 42 instead is the natural mistake, and it counts the four terms of depth
one twice.

## Two definitions of the same numbers

The Fibonacci numbers are defined by their recursion and computed here in two
ways: by iterating the recursion, and from the closed form. The closed form
uses the golden ratio, which is irrational, so evaluating it in floating point
loses the value within twenty terms. Doing the arithmetic in the ring where
phi squared is phi plus one keeps everything exact, and the two definitions
then agree exactly rather than approximately, which is what the equality
claims.
