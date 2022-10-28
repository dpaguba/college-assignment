"""Kahn process networks: determinism bought with a single restriction.

Processes communicate over unbounded channels and a read blocks until a token
is there. Nothing else is allowed, and in particular a process may not test
whether a channel is empty. That single prohibition is what makes the network
deterministic: the output depends on the inputs and not on the speed of
anything.

Allowing the test breaks it immediately, and the module runs the same network
in several orders to show the difference: the well-behaved one gives one
answer, the peeking one gives several.
"""


def example_network():
    """A well-behaved network: a doubling process feeding a summing one."""
    return {"kind": "kahn", "input": [1, 2, 3]}


def peeking_network():
    """The same network with a process that tests for an empty channel."""
    return {"kind": "peek", "input": [1, 2, 3]}


def run_in_orders(network, orders):
    """Runs the network under several schedules and collects the results.

    For a Kahn network every schedule gives the same result, which is the
    theorem. For the peeking one the result depends on how far ahead the
    producer has run, and the module models that by varying how many tokens
    are available when the consumer looks.
    """
    results = []
    for order in range(orders):
        if network["kind"] == "kahn":
            results.append([value * 2 for value in network["input"]])
        else:
            available = network["input"][:order % (len(network["input"]) + 1)]
            results.append([value * 2 for value in available])
    return results


def read_blocks():
    """Whether a read waits rather than returning an empty answer."""
    return True


def is_kahn_process(behaviour):
    """Whether a behaviour is allowed in the model."""
    allowed = {"blocking read": True, "write": True, "compute": True,
               "peek": False, "test for empty": False, "timeout": False}
    if behaviour not in allowed:
        raise ValueError("unknown behaviour: %s" % behaviour)
    return allowed[behaviour]


def channel_bound():
    """The bound on a channel in the model, which is that there is none.

    Unboundedness is part of the definition, and it is what an
    implementation has to give up: a real channel is finite, so a write can
    block, and a network that was deterministic can then deadlock.
    """
    return None


def sdf_is_a_special_case():
    """Whether synchronous dataflow is a restriction of this model.

    It is: fixed rates are a special case of a blocking read, and the
    restriction is what buys the compile time schedule that the general model
    cannot have.
    """
    return True
