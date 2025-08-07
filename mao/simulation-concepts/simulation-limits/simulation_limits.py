"""What simulation buys, what it costs, and how it is usually got wrong.

The ninth exercise sheet asks for three of each and the published solution
lists them. They are reproduced here as data rather than prose, because the
list is the answer and the module can then be used to check that nothing was
forgotten.

The one worth putting first is the third mistake in the solution's list:
using mean values instead of distributions. A simulation fed with averages
produces an average answer and hides exactly the variability it was built to
study.
"""


def advantages():
    """The advantages the published solution lists."""
    return ["systems that no analytical model describes accurately can be studied",
            "the system can be run under conditions that are real or impossible",
            "modifications are easy and experiments are controlled and repeatable",
            "very short and very long intervals can be observed",
            "many experiments can be run in parallel"]


def disadvantages():
    """The disadvantages it lists."""
    return ["a stochastic simulation produces stochastic output",
            "models need a great deal of data",
            "models are expensive and slow to build",
            "the volume of output hides how accurate it really is",
            "problems specific to simulation arise from the dynamic behaviour"]


def mistakes():
    """The typical mistakes it lists."""
    return ["building a model without a concrete goal",
            "the wrong level of detail, usually too much",
            "underestimating the effort of data collection and validation",
            "modelling the input data wrongly",
            "assuming independence of input and output",
            "Mittelwerte statt Verteilungen: means instead of distributions",
            "no evaluation of the results beyond taking an average",
            "no validation, often not even a plausibility check",
            "no sensitivity analysis",
            "no estimate of the range in which the model is valid"]


def is_stochastic_output():
    """Whether two runs with different seeds give different answers."""
    return True
