# Entities and attributes

An entity type collects all entities of one kind: the type `Kunde` all
customers, the type `Vorlesung` all courses. It is a rectangle in the diagram,
its attributes are ellipses, and the chosen key attribute is underlined.

## Candidates and the choice

A **candidate key** is a property of the data: an attribute whose values
happen to be distinct across the whole table. The **key attribute** is a
decision: which candidate the modeller picks. `key_candidates` finds the
first, `choose_key` records the second and refuses a choice that is not a
candidate.

`composite_keys` goes further and looks for the smallest combinations that
are unique when no single column is. It returns only minimal ones: a set that
contains a smaller unique set is not a candidate but a candidate with
luggage.

## Why the name is never the key

The table from the sheet has two students called Thomas Wagner with different
Matrikelnummern. That is not a corner case, it is the normal state of names,
and it is why keys in practice are meaningless numbers rather than telling
attributes. A telling attribute is one somebody may want to change later.
