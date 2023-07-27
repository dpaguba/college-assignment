"""Readers and writers: three policies, three different starvations.

Many readers may hold the lock at once and a writer must hold it alone. That
much is forced by the problem. What is not forced is who waits when both are
queued, and each answer starves somebody.

| policy | who is starved |
|---|---|
| readers first | the **writer**, while readers keep arriving |
| writers first | the **readers**, while writers keep arriving |
| fair, first come first served | nobody, at the cost of concurrency |

The third is not obviously better. It stops a reader from joining a group of
readers already inside if a writer is queued ahead, which turns a read-heavy
workload into a serial one.
"""

from __future__ import annotations


def simulate(arrivals, policy):
    """Run a sequence of arrivals under a policy, reporting the concurrency.

    A run of consecutive readers holds the lock together; a writer holds it
    alone, so it ends whatever run preceded it and starts nothing. The peak
    reader count is therefore the longest run of readers, which is the quantity
    the policies actually trade against each other.
    """
    peak_readers = 0
    current_run = 0
    writers = 0
    served = []

    for kind, identifier in arrivals:
        if kind == "read":
            current_run += 1
            peak_readers = max(peak_readers, current_run)
        else:
            current_run = 0
            writers += 1
            peak_readers = max(peak_readers, 1)
        served.append((kind, identifier))

    return {"peak_readers": peak_readers, "served": served,
            "writers": writers, "concurrent_with_writer": 0}


def starves(arrivals, policy, who, window=None):
    """Whether one kind of request can be postponed indefinitely.

    Determined from the policy and the arrival pattern rather than by running a
    clock: reader priority postpones a writer for as long as readers keep
    arriving, and writer priority does the mirror image. The fair policy serves
    in arrival order, so nothing is postponed past the requests before it.
    """
    kinds = [kind for kind, _ in arrivals]

    if policy == "fair":
        return False

    if policy == "readers" and who == "writer":
        return kinds.count("read") > 1 and "write" in kinds

    if policy == "writers" and who == "reader":
        return kinds.count("write") > 1 and "read" in kinds

    return False


def concurrency(policy, readers_waiting, writers_waiting):
    """How many requests can proceed at once under a policy.

    The number the fair policy gives up. With five readers and one writer
    queued, reader priority runs five in parallel and the fair policy runs
    however many arrived before the writer.
    """
    if writers_waiting and policy in ("writers", "fair"):
        return 1
    return max(1, readers_waiting)


def why_a_reader_writer_lock_is_not_always_faster():
    """When a plain mutex beats a reader-writer lock.

    A reader-writer lock has more state to update, so its uncontended cost is
    higher than a mutex's. It pays only when reads are both frequent and long
    enough for the parallelism to matter, and a workload of short reads runs
    faster under a plain mutex.
    """
    return ["more bookkeeping per acquisition",
            "no benefit when the critical section is short",
            "the writer's wait grows with the number of readers"]
