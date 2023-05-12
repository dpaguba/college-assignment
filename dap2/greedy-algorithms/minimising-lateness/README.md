# Minimising lateness

One machine, jobs with deadlines, order them so that the worst overrun is
smallest.

| | |
|---|---|
| Time | O(n log n) |
| Space | O(n) |
| Greedy rule | earliest deadline first |

## The idea

Each job has a duration and a deadline. The machine runs one job at a time with
no gaps. A job that finishes at time f with deadline d has lateness max(0,
f − d), and the objective is to minimise the **largest** lateness over all
jobs, not the total.

Sort by deadline. That is the whole algorithm, and the durations are never
looked at.

## Why ignoring durations is right

Shortest job first is the intuitive rule and it loses. Jobs `(1, 100)` and
`(10, 10)`: running the short one first pushes the urgent job to time 11 for a
lateness of 1, while the reverse order finishes both on time.

## The proof

An **exchange** argument on inversions. An inversion is a pair where a job with
a later deadline runs before one with an earlier deadline. Two facts:

- A schedule with an inversion has an *adjacent* inversion. If deadlines are
  out of order somewhere, they are out of order between two neighbours.
- Swapping an adjacent inversion never increases the maximum lateness. Only
  the two swapped jobs change finishing time; the one moved earlier can only
  improve, and the one moved later now finishes when the other used to, with a
  deadline that is not earlier.

Each swap removes at least one inversion, so after finitely many swaps there
are none, and a schedule with no inversions is exactly earliest deadline first.
Every step was non-worsening, so that schedule is optimal.

## What is worth noticing

The proof says no order does better. It does not say nothing is late, and the
textbook instance has lateness 1 no matter what. Confusing "optimal" with
"zero" is the usual misreading of greedy proofs.

Adding release times, so a job cannot start before it becomes available, makes
the problem NP-hard. Adding a second machine does too. The tractability here
is narrower than it looks.
