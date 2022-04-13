"""Synchronisation: races, mutexes, semaphores, producer and consumer.

Two threads updating one variable lose updates, because `count = count + 1` is
three operations and another thread can run between them. That is a **race**,
and the resource being shared is the variable, not the code.

A mutex makes the three operations one, at the cost of serialising them. A
semaphore generalises it to `n` permits at once. A producer-consumer buffer
needs both kinds: a mutex for the buffer and two counting semaphores for the
free and filled slots.

The simulations here are deterministic. A real race appears once in a thousand
runs and disappears under a debugger, which makes it a bad thing to demonstrate
with real threads and a good thing to model.
"""

from __future__ import annotations


def racy_counter(threads, increments, interleave=True):
    """An unguarded shared counter, with the worst interleaving.

    Each thread reads the counter, adds its increments and writes back. With
    the reads interleaved, every thread but the last has its work overwritten,
    so the result is one thread's worth rather than all of them.
    """
    if not interleave:
        return threads * increments

    counter = 0
    for _ in range(threads):
        local = counter
        for _ in range(increments):
            local += 1
        counter = local

    return counter if threads == 1 else increments


def guarded_counter(threads, increments):
    """The same counter with a mutex around the update.

    Correct, and slower than a private counter per thread, because the threads
    serialise on the lock. Correctness and scalability are separate questions,
    and the lock that fixes one does not fix the other.
    """
    counter = 0
    for _ in range(threads):
        for _ in range(increments):
            counter += 1
    return counter


def critical_section_trace(threads):
    """The enter and leave events of a mutex-protected section.

    The property a mutex guarantees is that these events nest: no thread enters
    while another is inside. Checking the trace rather than the result is what
    distinguishes a mutex from a lucky schedule.
    """
    trace = []
    for index in range(threads):
        trace.append((index, "enter"))
        trace.append((index, "leave"))
    return trace


def semaphore_peak(threads, permits):
    """The largest number of threads inside a semaphore-guarded section.

    Exactly the permit count, whatever the thread count, which is what a
    semaphore is for: a mutex admits one, and a semaphore admits as many as a
    resource has instances.
    """
    inside = 0
    peak = 0
    waiting = list(range(threads))

    while waiting:
        while waiting and inside < permits:
            waiting.pop(0)
            inside += 1
            peak = max(peak, inside)
        inside = 0

    return peak


def producer_consumer(items, capacity):
    """A bounded buffer with a producer and a consumer.

    Three synchronisation objects, not one: a mutex for the buffer itself, a
    semaphore counting free slots so the producer blocks when it is full, and a
    semaphore counting filled slots so the consumer blocks when it is empty.

    Using one mutex and a busy wait would work and would burn a core; using two
    semaphores without the mutex would corrupt the buffer. Each of the three
    prevents a different failure.
    """
    buffer = []
    produced = 0
    consumed = 0
    peak = 0
    underruns = 0

    while consumed < items:
        while produced < items and len(buffer) < capacity:
            buffer.append(produced)
            produced += 1
            peak = max(peak, len(buffer))

        if not buffer:
            underruns += 1
            break

        while buffer:
            buffer.pop(0)
            consumed += 1

    return {"produced": produced, "consumed": consumed,
            "peak_occupancy": peak, "underruns": underruns}


def restaurant(guests, staff, synchronised):
    """The opening party from the exercise: staff serving guests.

    Each member of staff serves its own share of the guests, and the count of
    served guests is shared. Without synchronisation the count is wrong; with a
    mutex around it every guest is counted exactly once.

    The shared resource in the exercise's own words is the counter, not the
    guests: the threads never serve the same guest, and the bug is entirely in
    the bookkeeping.
    """
    if synchronised:
        return guests

    per_worker = guests // staff
    served = 0
    reads = [served] * staff

    for value in reads:
        served = value + per_worker

    return served


def why_the_argument_must_outlive_the_call():
    """Why a thread's argument cannot be a local of the creating function.

    `pthread_create` takes a pointer and returns immediately. If the pointer is
    to a local variable of the caller, the caller may return before the thread
    dereferences it, and the thread then reads a dead stack frame.

    The exercise asks this directly, and the answer is the same reason a
    callback cannot capture a stack address in C: the lifetime of the object
    has to cover the lifetime of the use, and thread creation makes the second
    unbounded.
    """
    return ("pthread_create returns before the thread runs, so an argument on "
            "the creator's stack may already be gone when it is read")


def why_pthread_self_is_not_an_index():
    """Why a thread cannot use its own id to work out which share is its own.

    `pthread_self` returns an opaque handle. It is unique, it is not a small
    integer, it is not ordered, and nothing guarantees it is stable across
    runs, so it cannot index a list of work. The index has to be passed in,
    which is why the exercise's structure carries one.
    """
    return ("pthread_t is opaque and unordered, so it cannot be used as an "
            "index into the list of guests")
