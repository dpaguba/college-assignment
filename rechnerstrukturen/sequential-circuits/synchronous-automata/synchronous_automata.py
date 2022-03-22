"""Moore and Mealy machines as synchronous circuits.

A sequential circuit is a state register and two blocks of combinational logic:
one computing the next state, one computing the output. Where the output block
gets its inputs is the whole difference between the two models.

A **Moore** output depends only on the state, so it changes only at a clock
edge and is glitch-free. A **Mealy** output depends on the state and the
current input, so it reacts one cycle earlier and inherits every glitch the
input has.

Mealy machines need at most as many states, and often fewer, which is the trade:
fewer flip-flops against a less well-behaved output.
"""

from __future__ import annotations

import math


class Moore:
    """A machine whose output is a function of the state alone."""

    def __init__(self, states, initial, transitions, outputs):
        """Store the state set, the transition table and the output map."""
        self.states = list(states)
        self.initial = initial
        self.transitions = dict(transitions)
        self.outputs = dict(outputs)

    def run(self, inputs):
        """Outputs produced while reading an input sequence.

        The output at step `i` is the one of the state **before** the input is
        applied, which is what makes a Moore machine react one cycle late.
        """
        state = self.initial
        result = []

        for symbol in inputs:
            result.append(self.outputs[state])
            state = self.transitions[(state, symbol)]

        return result


class Mealy:
    """A machine whose output depends on the state and the input."""

    def __init__(self, states, initial, transitions):
        """Store the state set and the combined transition and output table."""
        self.states = list(states)
        self.initial = initial
        self.transitions = dict(transitions)

    def run(self, inputs):
        """Outputs produced while reading an input sequence."""
        state = self.initial
        result = []

        for symbol in inputs:
            state, output = self.transitions[(state, symbol)]
            result.append(output)

        return result


def to_moore(mealy):
    """Convert a Mealy machine into a Moore machine.

    Each Mealy state is split into one Moore state per output value that can
    lead into it, so the output becomes a property of the state. The result has
    at least as many states, and its output sequence is the original delayed by
    one step, which is the price of removing the dependence on the input.
    """
    outputs = sorted({output for _, output in mealy.transitions.values()})
    states = [(state, output) for state in mealy.states for output in outputs]

    transitions = {}
    for (state, symbol), (target, output) in mealy.transitions.items():
        for value in outputs:
            transitions[((state, value), symbol)] = (target, output)

    return Moore(states=states, initial=(mealy.initial, outputs[0]),
                 transitions=transitions,
                 outputs={entry: entry[1] for entry in states})


def flip_flops_needed(states):
    """How many flip-flops a state encoding needs.

    The logarithm, rounded up. Using more is a deliberate choice: a one-hot
    encoding costs one flip-flop per state and makes the next-state logic
    trivial, which is often the better trade in an FPGA and never in an ASIC.
    """
    return max(1, math.ceil(math.log2(states)))


def one_hot_bits(states):
    """Flip-flops for a one-hot encoding, for comparison."""
    return states


def next_state_table(machine, alphabet):
    """The transition table as a truth table over encoded states.

    This is the step where an automaton becomes a circuit: encode the states as
    bit vectors and the table becomes a Boolean function per flip-flop, to be
    minimised like any other.
    """
    encoding = {state: index for index, state in enumerate(machine.states)}
    rows = []

    for state in machine.states:
        for symbol in alphabet:
            key = (state, symbol)
            if key not in machine.transitions:
                continue
            target = machine.transitions[key]
            if isinstance(target, tuple) and not isinstance(machine, Moore):
                target = target[0]
            rows.append({"state": encoding[state], "input": symbol,
                         "next": encoding[target]})

    return rows
