# Granularity

An activity in a conceptual model is often not cut at the size execution
needs. Two rules of thumb from the lecture, and both are about resources:

- **too abstract** when the activity needs more than one resource. It hides a
  handover, and a handover is exactly where a case stops moving.
- **too detailed** when consecutive activities belong to the same resource.
  Nothing happens between them that the system needs to know.

`assess` applies both to a list of activities and returns what to decompose
and which neighbours to merge.

## The third test

Ask whether the activity is done in one sitting. Something that is put aside
and picked up later is two activities with a wait between them, whatever the
model calls it, and modelling it as one hides the wait from every measurement
that follows.

The cost of getting it wrong runs both ways. Too coarse and the handover is
invisible and unmeasurable. Too fine and a person confirms five steps where
one would do, which they will stop doing, and then the log stops being true.
