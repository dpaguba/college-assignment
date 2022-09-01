# Transactions and the unit of work

The unit of work remembers what a row looked like when it was loaded and
compares at the end. Assigning a field writes nothing: the module measures 0
writes during the work and 1 at the commit. That is dirty checking, and it is
why an explicit save call is often absent.

A rollback leaves the store exactly as it was.

Loading the same key twice returns the same object, not two copies. That is
the identity map, and it is what makes the comparison at the end possible.

## The states

| state | meaning |
|---|---|
| new | not yet known to the store |
| managed | watched, changes will be written |
| detached | known to the store, no longer watched |
| removed | scheduled for deletion |

A change to a detached object is written nowhere, which the module measures
as 0 writes. This is the usual explanation for a change that disappears: the
object left the unit of work before it was edited.

A flush writes without ending the transaction, which is needed when a
generated key is required before the commit.
