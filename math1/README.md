# Mathematik für Informatik 1

Thirty-two modules in six blocks, following the three parts of the lecture.
The course publishes no exercises and no solutions, so every claim here is
checked by enumerating a finite case or against an independent computation.

| Block | |
|---|---|
| [sets-and-logic](sets-and-logic/) | propositions, sets, countability |
| [relations-and-functions](relations-and-functions/) | properties, closures, partitions, counting |
| [induction](induction/) | inductive definitions, structural induction, well-founded orders |
| [order-structures](order-structures/) | orders, lattices, Boolean lattices, fixed points |
| [algebraic-structures](algebraic-structures/) | monoids, groups, rings, fields |
| [linear-algebra](linear-algebra/) | elimination, maps, determinants, eigenvalues |

The German conspectus is in [tex/](tex/).

## Counts worth keeping

| | |
|---|---:|
| relations on three elements | 512, of which 171 transitive, 19 partial orders, 5 equivalences |
| partitions of an n-element set | 1, 1, 2, 5, 15, 52 |
| linear extensions of the subsets of a three-element set | 48 |
| associative operations on a three-element set | 113 of 19 683 |
| groups of order eight | 5 classes |
| ideals of the residues modulo 12 | 6, one per divisor |
| terms over two constants and one binary operation | 2, 6, 38 |
| determinant of an 8×8: permutations against elimination | 282 240 against 168 multiplications |
| Kleene iteration on a 16-element lattice | 4 steps, height 5 |
| eigenfaces of eight images built from three patterns | 3 components, error 3·10⁻⁵ |

## Four results that argue with the first guess

**Normality is not a weak form of commutativity.** The quaternion group is not
abelian and all six of its subgroups are normal. The symmetric group on three
points has six subgroups of which three are normal. Whatever normality
measures, it is not distance from being abelian.

**A field with four elements exists and is not the residues modulo four.**
"Z/n is a field exactly when n is prime" says nothing about which sizes a
field may have. GF(4) is built from polynomials over the two-element field
and has characteristic 2, not 4.

**Closures do not commute.** Closing a relation symmetrically and then
transitively gives an equivalence; doing it in the other order gives a
relation that is not even transitive. The definition of the equivalence
closure fixes an order for a reason.

**The term count is 38, not 42.** Two constants and one binary operation give
2, 6, 38 terms at the first three depths, because the terms already built are
not built again. The recurrence is c + t(n)², and writing t(n) + t(n)² is the
natural mistake.

## Verification

There are no published solutions, so each module is checked against something
that does not share its reasoning. The counting results are checked against
their known values (the Bell numbers, the 171 transitive relations, the 113
associative operations, the five groups of order eight). The algebra is
checked by exhaustive search: an isomorphism is found or every bijection has
failed. The linear algebra is exact and checked against numpy on 800 random
inputs. Where a claim was checked only by enumerating a finite case, the
module says so.
