# Specialisation and generalisation

A general entity is split into more specific ones, which may carry extra
attributes. The triangle is labelled with a pair:

- **T** total: every entity belongs to at least one special case.
- **P** partial: an entity may belong, but need not.
- **D** disjoint: at most one special case per entity.
- **N** not disjoint: any number of special cases per entity.

`check` tests a population against both letters, which is where the labels
stop being decoration: T means a query over the special cases loses nobody,
D means an entity cannot be counted twice.

## The example from the sheet

Mitarbeiter split into Verwaltungskraft and Werkstudent, labelled (P, D).
Partial because a university also employs academic staff, who are neither.
Disjoint because the two roles exclude each other.

All four combinations occur. (T, D) is a strict partition, such as a person
being either a minor or an adult. (T, N) covers vehicles, each of which has
at least one drive and a hybrid has two. (P, N) covers customers who may
subscribe to the newsletter, may have complained, may have done both, and
usually have done neither.
