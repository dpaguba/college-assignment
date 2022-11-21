"""CRISP-DM: the process model, and where the work actually goes.

Six phases, and the arrows between them run in both directions. The reason
the diagram is drawn as a cycle is that every phase can send the project
back: modelling reveals that the data needs different preparation, and data
understanding reveals that the business question was wrong.

The effort distribution is the part practitioners quote. Preparing the data
takes more time than modelling by a wide margin, and a project plan that
allocates them equally is planning the wrong project.
"""

PHASES = ["business understanding", "data understanding", "data preparation",
          "modelling", "evaluation", "deployment"]
"""The six phases in their nominal order."""

RETURNS = {
    "business understanding": [],
    "data understanding": ["business understanding"],
    "data preparation": ["data understanding"],
    "modelling": ["data preparation"],
    "evaluation": ["business understanding", "modelling"],
    "deployment": ["evaluation"],
}
"""Which phase each one can send the project back to."""


def phases():
    """The six phases in order."""
    return list(PHASES)


def can_return_to(phase):
    """The phases a given phase can send the project back to."""
    if phase not in RETURNS:
        raise ValueError("unknown phase: %s" % phase)
    return RETURNS[phase]


def typical_effort():
    """How the effort is usually distributed, as shares of the whole."""
    return {"business understanding": 0.10, "data understanding": 0.15,
            "data preparation": 0.45, "modelling": 0.15,
            "evaluation": 0.10, "deployment": 0.05}


def is_iterative():
    """Whether the process is a cycle rather than a sequence."""
    return any(RETURNS[phase] for phase in PHASES)
