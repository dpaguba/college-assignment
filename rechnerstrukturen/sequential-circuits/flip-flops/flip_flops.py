"""Flip-flops: one bit of memory, and why one input combination is forbidden.

An RS flip-flop is two cross-coupled NOR gates. Setting `S` drives the output
to one, setting `R` drives it to zero, and setting neither holds the previous
value. That holding is the memory, and it exists because each gate's output is
the other's input.

`R = S = 1` is forbidden, and the exercise asks why. The answer is in two
parts. **Statically**, both outputs are forced to zero, so the invariant that
the second output is the complement of the first is violated: the circuit is in
a state it is not supposed to have. **Dynamically**, releasing both inputs at
once leaves both gates seeing zeros and both trying to drive high, and which
one wins depends on which gate happens to be faster. That is a race, and a
circuit whose state depends on manufacturing tolerances is unusable.

Every other flip-flop is a way of making that combination unreachable: D ties
the inputs together, JK defines the case as a toggle, T is JK with one input.
"""

from __future__ import annotations


def is_forbidden(reset, set_input):
    """Whether an input combination is the forbidden one."""
    return bool(reset and set_input)


def rs_step(previous, reset, set_input):
    """One step of an RS flip-flop, rejecting the forbidden input."""
    if is_forbidden(reset, set_input):
        raise ValueError("R = S = 1 is not allowed for an RS flip-flop")

    if set_input:
        return 1
    if reset:
        return 0
    return previous


def rs_raw(reset, set_input, previous):
    """The two gate outputs without the guard, showing what goes wrong.

    With both inputs high, both NOR gates output zero, so `q` and `not_q` are
    equal. The flip-flop's defining property is that they are complements, and
    here it simply does not hold.
    """
    q, not_q = previous
    new_q = 1 - (reset | not_q)
    new_not_q = 1 - (set_input | q)

    if is_forbidden(reset, set_input):
        return {"q": 0, "not_q": 0, "consistent": False}

    return {"q": new_q, "not_q": new_not_q, "consistent": new_q != new_not_q}


def rs_release_trace(steps):
    """The output after both inputs are released from the forbidden state.

    Both gates start at zero and both see a zero input, so both switch to one,
    and then both see a one and switch back. The circuit oscillates until an
    asymmetry in the gate delays breaks the tie, and which state it settles in
    is not determined by the inputs.

    The trace shows the oscillation rather than asserting it, which is the
    point of the exercise: the objection to `R = S = 1` is not that the
    standard forbids it but that the physics does not decide it.
    """
    state = (0, 0)
    trace = []

    for _ in range(steps):
        q, not_q = state
        state = (1 - not_q, 1 - q)
        trace.append(state[0])

    return trace


def d_step(previous, data):
    """A D flip-flop: the input is stored, and nothing is forbidden.

    Built by driving `S` with the data and `R` with its complement, so the two
    are never equal and the forbidden combination cannot be reached. That is
    the whole design, and it is why D is what a register is built from.
    """
    return data


def jk_step(previous, j, k):
    """A JK flip-flop: the forbidden combination is defined as a toggle.

    The other way out. Instead of making `J = K = 1` unreachable it is given a
    meaning, which makes the flip-flop more useful and the circuit slightly
    larger, since the current state has to be fed back into the inputs.
    """
    if j and k:
        return 1 - previous
    if j:
        return 1
    if k:
        return 0
    return previous


def t_step(previous, toggle):
    """A T flip-flop: toggle or hold.

    A JK flip-flop with its two inputs tied together. A chain of them divides a
    clock by two at every stage, which is what a ripple counter is.
    """
    return 1 - previous if toggle else previous


def setup_and_hold(setup, hold, arrival):
    """Whether a data change respects the timing window.

    A flip-flop samples its input at the clock edge, and the input must be
    stable from `setup` before it until `hold` after it. Violating the window
    puts the flip-flop into a metastable state, where its output sits between
    the two logic levels for an unbounded time.

    Metastability cannot be designed away, only made improbable, which is why
    crossing a clock domain costs two flip-flops and a paragraph of
    justification.
    """
    return -setup <= arrival <= -0.0 or arrival >= hold
