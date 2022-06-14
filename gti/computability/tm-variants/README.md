# Variants of the machine

Multiple tapes, nondeterminism, a queue instead of a tape. Each looks like more
power and none of them is: they all accept exactly the same languages, and that
robustness is the real argument for the Church-Turing thesis.

What the variants change is **time**, and that is where the fourth block starts.

| Variant | Cost of simulating it on one deterministic tape |
|---|---|
| k tapes | quadratic |
| nondeterministic | exponential |

## Two tapes

`two_tape_separator` decides `{ w # w }`: copy the part before the separator to
the second tape, rewind, compare in one sweep. On a single tape the same job is
a long back-and-forth, which is exactly where the quadratic factor comes from,
and `simulate_multitape` reports what those sweeps would cost.

## Nondeterminism

The search is **breadth-first**, deliberately. One branch may run for ever, and
depth-first would follow it and never come back. That is the standard
simulation argument, and the exponential cost is visible in the number of
configurations explored.

`nondeterministic_contains` guesses where the pattern starts and verifies.
Nondeterminism adds no power and it does shorten descriptions, which is the
accurate summary of what it is for.

## Queue automata, as the course defines them

Sheet 10 defines them precisely: transitions over `Q x (Sigma + eps) x
(Gamma + eps) x Q x Gamma*`, the queue **starts empty**, and a transition with
epsilon in the queue position fires regardless of the content and removes
nothing. The implementation here follows that definition rather than the more
common "input preloaded in the queue" version, because the exercise asks about
this one.

The exercise's real question is why a queue is as strong as a tape. The answer
is **rotation**: taking the front and appending it at the back walks the whole
content past the head, so everything can be inspected and rewritten. A stack
cannot, because reading destroys, and that is the entire gap between this model
and a pushdown automaton.

`queue_equal_counts` needs no rotation, which is worth noticing: `a^n b^n` is
within reach of a stack too. The marker trick it uses is nice on its own, the
end marker can only reach the front after every counter has been consumed, so
the counts must agree exactly.
