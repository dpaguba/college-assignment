# Soundness

Three conditions on the reachability graph:

1. **Option to complete:** from every reachable marking, the final marking
   is still reachable. Not merely that it occurs somewhere: the condition is
   checked backwards, from the final markings along the reversed edges of
   the reachability graph, and it holds only if that walk covers every
   reachable marking.
2. **Proper completion:** when the case finishes, nothing is left over.
3. **No dead activities:** every task fires in some reachable marking.

## The two classic errors, and why they are not the same

**XOR split, AND join.** The split sends the token down one branch, the join
waits for both. It never gets both. The case stops and never finishes:
a deadlock in the ordinary sense of the word.

**AND split, XOR join.** The split lays two tokens, the join lets each
through separately. Two tokens arrive at the end event and the case finishes
twice. Nothing is stuck; something is duplicated. Downstream that means a
second invoice, a second shipment, or a second payment.

Both fail soundness, and an earlier version of this module reported both as
deadlocks, which is wrong in the way that matters: one of them leaves a case
lying in a queue, the other sends the customer two parcels. They are
reported separately now, under `deadlocks` and `finished more than once`.

## Dead activities

`dead_activity_example` puts a parallel join behind an exclusive split. The
join never fires, so everything behind it is unreachable, and `never` is
reported. Work that was modelled, agreed, and never happens.

## Cross-check

The reachability graph here is a second implementation, smaller than the one
in `token-simulation` and restricted to the exclusive and parallel gateways.
On the four examples both agree on the number of reachable markings: 6, 5,
10 and 5. Two implementations written for different purposes landing on the
same numbers is the check that the firing rules are right.
