"""Validation: three questions that are routinely confused.

Verification asks whether the model was built right, validation whether the
right model was built, and credibility whether anyone believes the answer.
The first is a programming question, the second an empirical one, and the
third a social one, and a project can pass any two and fail on the third.

The techniques the lecture lists range from comparing against measurements to
looking at an animation, and only some of them are statistical. Face validity
is not a test and is still worth doing, which is why the module labels each
technique rather than ranking them.
"""


def kinds():
    """The three questions and what each one asks."""
    return {"verification": "was the model built right",
            "validation": "was the right model built",
            "credibility": "does the user believe the result"}


def techniques():
    """The techniques the lecture names, with whether they are statistical."""
    return {"comparison with measurements": True,
            "confidence interval": True,
            "degenerate cases": False,
            "extreme condition test": False,
            "face validity": False,
            "animation": False,
            "sensitivity analysis": True}


def is_statistical(technique):
    """Whether a technique produces a number that can be tested."""
    table = techniques()
    if technique not in table:
        raise ValueError("unknown technique: %s" % technique)
    return table[technique]


def compare(model_values, reference_values, tolerance):
    """Whether the model means agree with the reference within a tolerance."""
    model_mean = sum(model_values) / len(model_values)
    reference_mean = sum(reference_values) / len(reference_values)
    return abs(model_mean - reference_mean) <= tolerance


def degenerate_case_holds():
    """Whether the model gives the obvious answer in a degenerate case.

    A queue with no arrivals must be empty. Such a case has an answer that
    needs no measurement, which is what makes it the cheapest validation
    there is and the first one to run.
    """
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                    "queueing-models"))
    import queueing_models
    trace = queueing_models.queue_trace(0.0001, 1.0, 200, seed=1)
    return sum(trace) / len(trace) < 0.01
