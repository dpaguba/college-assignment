# Boolean functions

| Topic | |
|---|---|
| [normal-forms](normal-forms/) | truth vectors, DNF and CNF |
| [minimisation](minimisation/) | Quine and McCluskey, primes and covers |
| [obdd](obdd/) | a canonical form that is usually small |

Three representations of the same object, and they differ in what is cheap.
A truth vector makes evaluation trivial and equality expensive in space. A
minimal cover makes the circuit small and equality undecidable by inspection.
An OBDD makes equality a structural comparison and satisfiability a walk, at
the cost of a variable order that can ruin it.
