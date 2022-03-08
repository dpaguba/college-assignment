# Relation properties

Five properties, and the counts that describe how restrictive each one is.

Relations on a three-element set:

| | count |
|---|---:|
| all | 512 |
| reflexive | 64 |
| symmetric | 64 |
| antisymmetric | 216 |
| transitive | 171 |
| equivalence relations | 5 |
| partial orders | 19 |

Every number here comes from generating all 512 relations and testing each
one, which settles several questions the definitions leave open. Symmetry and
antisymmetry are not opposites: the identity relation has both, and 24
relations on three elements have both. The empty relation is symmetric,
antisymmetric and transitive, and fails only reflexivity, which is why
reflexivity is stated separately rather than derived.

Transitivity is the expensive condition. It removes two thirds of the
relations on its own, and it is the one whose check is quadratic in the
relation rather than linear, which is the practical reason the transitive
closure gets its own module.
