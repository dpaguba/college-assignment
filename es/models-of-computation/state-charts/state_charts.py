"""State charts: hierarchy, parallel states, and history.

A flat automaton for the exam's cookie machine would need one state per
combination of power, size and crunchiness. The chart needs three small
machines: the two settings are parallel states inside the machine, and the
crunchiness carries a history marker so that switching the machine off and on
restores it while the size returns to its default.

That difference is the whole point of the notation. The history marker is one
symbol and it replaces a duplicate copy of the entire settings machine.
"""

CRUNCHINESS = ["very crunchy", "soft", "crunchy"]
"""The cycle the exam prescribes, starting at the default."""

SIZES = ["big", "small"]
"""The two sizes, starting at the default."""


def cookie_machine():
    """The initial configuration: off, with the defaults remembered."""
    return {"power": "off", "size": "big", "crunchiness": "very crunchy",
            "history": "very crunchy"}


def current(machine):
    """The configuration a user would see."""
    return dict(machine)


def press(machine, button):
    """The configuration after a button press."""
    state = dict(machine)
    if button == "power":
        if state["power"] == "off":
            state["power"] = "on"
            state["crunchiness"] = state["history"]
            state["size"] = "big"
        else:
            state["power"] = "off"
            state["history"] = state["crunchiness"]
        return state
    if state["power"] == "off":
        return state
    if button == "crunchiness":
        index = CRUNCHINESS.index(state["crunchiness"])
        state["crunchiness"] = CRUNCHINESS[(index + 1) % len(CRUNCHINESS)]
        state["history"] = state["crunchiness"]
        return state
    if button == "size":
        index = SIZES.index(state["size"])
        state["size"] = SIZES[(index + 1) % len(SIZES)]
        return state
    raise ValueError("unknown button: %s" % button)


def kind_of(state):
    """Whether a composite state is a parallel one or a choice."""
    kinds = {"settings": "AND", "crunchiness": "OR", "size": "OR",
             "machine": "OR"}
    if state not in kinds:
        raise ValueError("unknown state: %s" % state)
    return kinds[state]


def flat_state_count():
    """How many states a flat automaton would need for the same machine.

    Two power states times two sizes times three crunchiness settings, plus
    the remembered setting, which is what the history marker replaces.
    """
    return len(SIZES) * len(CRUNCHINESS) * 2
