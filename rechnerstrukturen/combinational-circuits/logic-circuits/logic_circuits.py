"""Gates, circuits, and the two costs a circuit has.

A circuit has a **size**, the number of gates, and a **depth**, the longest
path from an input to the output. Size is area and depth is delay, and the same
function usually admits a trade between them: eight values ANDed in a chain and
in a tree use the same seven gates and have depths of seven and three.

NAND is universal: every function can be built from it alone. That is not a
curiosity but why NAND is the gate a process is optimised for.
"""

from __future__ import annotations

import math


def gate(name, inputs):
    """Evaluate one gate."""
    if name == "not":
        return 1 - inputs[0]
    if name == "and":
        return int(all(inputs))
    if name == "or":
        return int(any(inputs))
    if name == "nand":
        return 1 - int(all(inputs))
    if name == "nor":
        return 1 - int(any(inputs))
    if name == "xor":
        return int(sum(inputs) % 2 == 1)
    raise ValueError(f"unknown gate {name}")


def from_nand(name):
    """Build a gate from NANDs alone, as a list of operations.

    `not a` is `a nand a`, `a and b` is `not (a nand b)`, and `a or b` is
    `(not a) nand (not b)` by De Morgan. Every other function follows, which is
    what universality means and why a fabrication process only has to be good
    at one gate.
    """
    if name == "not":
        return [("nand", 0, 0)]
    if name == "and":
        return [("nand", 0, 1), ("nand", "t0", "t0")]
    if name == "or":
        return [("nand", 0, 0), ("nand", 1, 1), ("nand", "t0", "t1")]
    raise ValueError(f"cannot build {name} yet")


def simulate(circuit, inputs):
    """Run a NAND circuit given as a list of operations."""
    values = {}

    for index, (name, left, right) in enumerate(circuit):
        left_value = values[left] if isinstance(left, str) else inputs[left]
        right_value = values[right] if isinstance(right, str) else inputs[right]
        values[f"t{index}"] = gate(name, [left_value, right_value])

    return values[f"t{len(circuit) - 1}"]


def chain(operation, inputs):
    """Combine inputs one at a time, which is the deepest arrangement."""
    return {"kind": "chain", "operation": operation, "inputs": inputs}


def tree(operation, inputs):
    """Combine inputs pairwise, which is the shallowest.

    Only valid for an associative operation, which is exactly why associativity
    matters to a hardware designer: it is the licence to rebalance the circuit
    without changing the function.
    """
    return {"kind": "tree", "operation": operation, "inputs": inputs}


def size(circuit):
    """Gate count, which is the same for both arrangements."""
    return circuit["inputs"] - 1


def depth(circuit):
    """Longest path from an input to the output."""
    if circuit["kind"] == "chain":
        return circuit["inputs"] - 1
    return math.ceil(math.log2(circuit["inputs"]))


def multiplexer(values, select):
    """Select one of several inputs.

    Built from a decoder and one AND per input, so a multiplexer of `2^k`
    inputs costs `O(2^k)` gates and depth `k+1`. It is the hardware form of a
    conditional, and the reason a switch statement over a small range compiles
    to something with no branches.
    """
    return values[select]


def decoder(select, bits):
    """One-hot output: exactly one line high, chosen by the input."""
    return [1 if index == select else 0 for index in range(2 ** bits)]


def encoder(lines):
    """The inverse of a decoder: the index of the single high line."""
    active = [index for index, value in enumerate(lines) if value]
    if len(active) != 1:
        raise ValueError("an encoder needs exactly one active line")
    return active[0]


def fan_in_cost(inputs, maximum_fan_in):
    """Depth when gates have a limited number of inputs.

    Real gates take two to four inputs, so an eight-input AND is a tree of
    two-input gates and its depth is logarithmic rather than one. Ignoring this
    is what makes a paper design look faster than the chip.
    """
    return math.ceil(math.log(inputs, maximum_fan_in))
