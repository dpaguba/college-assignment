# Joins

Two plans, and the condition that decides between them.

A **reduce-side join** emits both sides keyed by the join attribute and pairs
them in the reducer, so both tables cross the network. A **map-side join**
broadcasts the small side to every mapper and joins there, so nothing but the
small side moves.

The condition is whether the small side fits in a mapper's memory. A star
schema is the case where it does: the dimensions are small and the fact table
is not, so the join that matters is exactly the one this plan handles.

Both produce the same pairs, which the module checks, so the choice is purely
about the network.
