# Synchronisation

Two threads updating one variable lose updates, because `count = count + 1` is
three operations and another thread can run between them. The shared resource
is the **variable**, not the code, which is the distinction the exercise asks
for.

## The race, measured on the real program

The assignment's opening party, four members of staff serving twelve guests,
compiled and run 300 times:

| version | wrong results | counts seen |
|---|---|---|
| without a mutex | **90 of 300** | 6, 9, 10, 11, 12 |
| with a mutex | **0 of 300** | 12 |

Seven runs in ten give the right answer without any synchronisation at all.
That is the whole problem with races: the version that is wrong passes most
tests, and it passed the first time it was run here too.

## The three objects a bounded buffer needs

A producer-consumer buffer needs a mutex for the buffer and two counting
semaphores, for free slots and for filled slots. Each prevents a different
failure: without the mutex the buffer corrupts, without the free-slot semaphore
the producer overruns, without the filled-slot semaphore the consumer reads
nothing. Verified: peak occupancy never exceeds the capacity and there are no
underruns.

## Two questions from the sheet

**Why must the thread argument outlive `pthread_create`?** Because the call
returns before the thread runs, so a pointer to a local of the creating
function may refer to a dead stack frame by the time it is read.

**Why is `pthread_self` not an index?** Because `pthread_t` is opaque and
unordered. It is unique and it is not a small integer, so it cannot select a
share of the work. The index has to be passed in.
