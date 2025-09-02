"""Translating control structures into jumps.

A target machine has conditional and unconditional jumps and nothing else. Each
source-level construct becomes a fixed pattern of labels and jumps, and the
patterns are worth comparing because they differ in cost.

The lecture's `while` scheme evaluates the condition at the top, jumps out when
it is false, and jumps back at the bottom: one conditional jump and one direct
jump per iteration.
"""

from __future__ import annotations


def translate_while(condition, body):
    """The lecture's scheme for `while (cond) body`.

        lloop:
        code(cond)          // result in r0
        if r0 = 0 goto lexit
        code(body)
        goto lloop
        lexit:

    The condition is evaluated before the body, so the body may run zero
    times, and the loop costs two jumps per iteration.
    """
    return (["lloop:", f"code({condition})", "if r0 = 0 goto lexit"]
            + list(body) + ["goto lloop", "lexit:"])


def translate_do_while(condition, body):
    """The scheme for `do body while (cond)`, with a single conditional jump.

        lloop:
        code(body)
        code(!cond)         // result in r0
        if r0 = 0 goto lloop

    Negating the condition is what removes the second jump. Testing `r0 = 0`
    on the negated condition means "jump back while the condition holds", so
    the loop needs no exit jump at all and falls through when it ends.

    The body runs before any test, which is the whole point of the construct,
    and the reason the exit label can be dropped: there is nothing to skip on
    the way in.
    """
    return (["lloop:"] + list(body)
            + [f"code(!{condition})", "if r0 = 0 goto lloop"])


def translate_if(condition, then_part, else_part=None):
    """The scheme for `if (cond) then else`.

    One conditional jump past the then-part, one direct jump past the
    else-part. Without an else-part the direct jump disappears, which is why
    an if-then is cheaper than an if-then-else and why compilers care about
    the difference.
    """
    if else_part is None:
        return ([f"code({condition})", "if r0 = 0 goto lend"]
                + list(then_part) + ["lend:"])

    return ([f"code({condition})", "if r0 = 0 goto lelse"]
            + list(then_part) + ["goto lend", "lelse:"]
            + list(else_part) + ["lend:"])


def translate_for(initialisation, condition, step, body):
    """A `for` loop, which is a `while` with the pieces moved around.

    Written out to show that it introduces nothing new: the initialisation
    happens once before the loop and the step becomes the last statement of
    the body. Every source language construct that looks new usually is one of
    these three patterns in disguise.
    """
    return [f"code({initialisation})"] + translate_while(condition,
                                                         list(body) + [f"code({step})"])


def run_while(condition, counter):
    """Execute a `while` loop over a counter, returning the iteration count."""
    state = {counter: 0}
    while condition(state):
        state[counter] += 1
    return state[counter]


def run_do_while(condition, counter):
    """Execute a `do while` loop over a counter, returning the iteration count.

    The difference from `run_while` is one line and it is the difference the
    construct exists for: the body runs before the first test, so the count is
    never zero.
    """
    state = {counter: 0}
    while True:
        state[counter] += 1
        if not condition(state):
            return state[counter]


def jump_count(code):
    """How many conditional and direct jumps a translation contains."""
    return {
        "conditional": sum(1 for line in code if line.startswith("if ")),
        "direct": sum(1 for line in code if line.startswith("goto ")),
    }
