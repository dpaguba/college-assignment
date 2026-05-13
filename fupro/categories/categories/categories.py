"""Categories: objects, arrows, composition, and two laws.

A category is not a structure with much in it. Every object has an identity
arrow, arrows compose when their ends match, composition is associative and
the identities do nothing. Everything else in the chapter is a consequence,
including what a functor has to preserve.

The point of stating so little is that so much satisfies it: sets and
functions, types and programs, a preorder with at most one arrow between any
two objects, and a monoid seen as a category with one object.
"""


def finite_category():
    """A small category: three objects and the arrows between them."""
    objects = ["A", "B", "C"]
    arrows = {"idA": ("A", "A"), "idB": ("B", "B"), "idC": ("C", "C"),
              "f": ("A", "B"), "g": ("B", "C"), "gf": ("A", "C")}
    composition = {
        ("idA", "idA"): "idA", ("idB", "idB"): "idB", ("idC", "idC"): "idC",
        ("f", "idA"): "f", ("idB", "f"): "f",
        ("g", "idB"): "g", ("idC", "g"): "g",
        ("g", "f"): "gf", ("gf", "idA"): "gf", ("idC", "gf"): "gf",
    }
    return {"objects": objects, "arrows": arrows, "composition": composition,
            "identities": {"A": "idA", "B": "idB", "C": "idC"}}


def broken_category():
    """The same data with one composition removed, so the laws fail."""
    category = finite_category()
    del category["composition"][("idB", "f")]
    return category


def compose(category, second, first):
    """The composite arrow, or nothing when the pair does not compose."""
    return category["composition"].get((second, first))


def identity_law(category):
    """Whether every identity leaves the arrows it meets unchanged."""
    for arrow, (source, target) in category["arrows"].items():
        if compose(category, arrow, category["identities"][source]) != arrow:
            return False
        if compose(category, category["identities"][target], arrow) != arrow:
            return False
    return True


def associativity_law(category):
    """Whether composing in either order gives the same arrow."""
    arrows = category["arrows"]
    for first in arrows:
        for second in arrows:
            for third in arrows:
                left = compose(category, second, first)
                right = compose(category, third, second)
                if left is None or right is None:
                    continue
                if compose(category, third, left) != compose(category, right,
                                                             first):
                    return False
    return True


def identity_functor(category):
    """The functor that maps a category to itself."""
    return {"objects": {name: name for name in category["objects"]},
            "arrows": {name: name for name in category["arrows"]}}


def broken_functor(category):
    """A map that sends every arrow to an identity, breaking composition."""
    return {"objects": {name: name for name in category["objects"]},
            "arrows": {name: category["identities"][ends[0]]
                       for name, ends in category["arrows"].items()}}


def is_functor(source, target, mapping):
    """Whether the map preserves identities, sources, targets and composition."""
    for name in source["objects"]:
        if mapping["objects"][name] not in target["objects"]:
            return False
        if mapping["arrows"][source["identities"][name]] != \
                target["identities"][mapping["objects"][name]]:
            return False
    for name, (start, end) in source["arrows"].items():
        image = mapping["arrows"][name]
        if target["arrows"][image] != (mapping["objects"][start],
                                       mapping["objects"][end]):
            return False
    for first in source["arrows"]:
        for second in source["arrows"]:
            composite = compose(source, second, first)
            if composite is None:
                continue
            expected = compose(target, mapping["arrows"][second],
                               mapping["arrows"][first])
            if mapping["arrows"][composite] != expected:
                return False
    return True
