"""Parallel loops: scheduling, reductions, and the two ways to get it wrong.

The exercise sheets use OpenMP, where a loop becomes parallel by adding a
pragma. What the pragma hides is exactly what this module makes explicit: how
the iterations are handed out, and what happens to variables written by more
than one thread.

Two failures follow, and they look nothing alike. A **race** is a correctness
bug: two threads read and write a shared value and one update is lost. **False
sharing** is a performance bug: two threads write different variables that
happen to share a cache line, and the line bounces between them.
"""

from __future__ import annotations


def static_chunks(total, threads):
    """Split iterations into contiguous blocks, one per thread.

    Decided before the loop runs, so it costs nothing at run time and assumes
    every iteration takes the same time. When that assumption fails, one thread
    finishes late and the rest wait.
    """
    chunks = []
    base, extra = divmod(total, threads)
    start = 0

    for index in range(threads):
        size = base + (1 if index < extra else 0)
        chunks.append(list(range(start, start + size)))
        start += size

    return chunks


def simulate(costs, threads, schedule="static", overhead=0.01):
    """Simulate running iterations of given costs on a number of threads.

    Static scheduling assigns the blocks up front; dynamic scheduling hands out
    one iteration at a time to whichever thread is free, at a small cost per
    handout. The makespan is when the last thread finishes, which is the only
    number that matters for a loop with a barrier at the end.
    """
    if schedule == "static":
        chunks = static_chunks(len(costs), threads)
        times = [sum(costs[index] for index in chunk) for chunk in chunks]
        return {"makespan": max(times) if times else 0.0,
                "assignments": threads, "times": times}

    times = [0.0] * threads
    assignments = 0

    for cost in costs:
        earliest = min(range(threads), key=lambda index: times[index])
        times[earliest] += cost + overhead
        assignments += 1

    return {"makespan": max(times), "assignments": assignments, "times": times}


def parallel_sum(data, threads):
    """A reduction: each thread sums a chunk, then the partials are combined.

    Correct because the shared variable is written once per thread rather than
    once per iteration, and the combination happens after all of them. That is
    what `reduction(+:sum)` compiles to, and why it is not merely a faster
    critical section.
    """
    chunks = static_chunks(len(data), threads)
    partials = [sum(data[index] for index in chunk) for chunk in chunks]
    return sum(partials)


def racy_sum(data, threads, interleave=False):
    """The same loop with an unguarded shared accumulator.

    Simulated rather than threaded, so the lost update is reproducible instead
    of intermittent: each thread reads the accumulator, adds its own chunk and
    writes back, and with the reads interleaved every thread but the last has
    its work overwritten.

    A real race is worse than this, because it appears once in a thousand runs
    and disappears under a debugger.
    """
    chunks = static_chunks(len(data), threads)

    if not interleave:
        total = 0
        for chunk in chunks:
            total += sum(data[index] for index in chunk)
        return total

    seen = 0
    result = 0
    for chunk in chunks:
        local = seen + sum(data[index] for index in chunk)
        result = local

    return result


def guarded_sum(data, threads):
    """The shared accumulator with a critical section around the update.

    Correct and slower than a reduction: the threads serialise on the lock, so
    a loop whose body is cheap spends most of its time waiting. Correctness and
    scalability are separate questions, and the pragma that fixes one does not
    fix the other.
    """
    chunks = static_chunks(len(data), threads)
    total = 0

    for chunk in chunks:
        total += sum(data[index] for index in chunk)

    return total


def false_sharing_traffic(addresses, block, iterations):
    """Coherence messages caused by threads writing into one cache line.

    The variables are distinct, so the program is correct and there is no race.
    The hardware works in cache lines, so writes to neighbouring addresses
    invalidate each other and the line ping-pongs, once per write.

    Padding the variables apart is the fix, and the measurement shows why it is
    worth the memory: two counters four bytes apart generate a message per
    iteration, and the same counters a line apart generate none.
    """
    lines = {address // block for address in addresses}
    if len(lines) == 1 and len(addresses) > 1:
        return iterations * len(addresses)
    return 0


def speedup(costs, threads, schedule="static"):
    """Speedup against one thread, measured on the simulation."""
    sequential = sum(costs)
    parallel = simulate(costs, threads, schedule)["makespan"]
    return sequential / parallel if parallel else 0.0


def load_imbalance(result):
    """How much of the makespan is one thread waiting for another.

    Zero when every thread finishes together. The number matters because it
    separates the two reasons a parallel loop scales badly: too little work per
    thread, or the work spread unevenly.
    """
    times = result["times"]
    if not times or max(times) == 0:
        return 0.0
    return 1.0 - (sum(times) / len(times)) / max(times)
