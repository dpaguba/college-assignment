"""Type classes: an interface, its instances, and how one is chosen.

A class declares methods and may give defaults. An instance supplies the
missing ones for a type. Resolution happens on the type rather than on the
value, which is what separates a type class from an object's method table and
why an instance can be added for a type that was written earlier.

An instance for a parametrised type may need one for the parameter, which is
the constraint written before the arrow in a Haskell instance head.
"""


class NoInstance(Exception):
    """Raised when no instance is declared for a type."""


CLASSES = {
    "Eq": {"methods": ["equals"],
           "defaults": {"not_equals": lambda instance:
                        lambda left, right: not instance["equals"](left, right)}},
    "Ord": {"methods": ["less"], "superclass": "Eq",
            "defaults": {"greater": lambda instance:
                         lambda left, right: instance["less"](right, left),
                         "at_most": lambda instance:
                         lambda left, right: not instance["less"](right, left)}},
}
"""The classes of the lecture, with their default methods."""

INSTANCES = {
    ("Eq", "Int"): {"equals": lambda left, right: left == right},
    ("Eq", "Bool"): {"equals": lambda left, right: left == right},
    ("Ord", "Int"): {"less": lambda left, right: left < right},
}
"""The declared instances."""


def resolve(class_name, type_name):
    """The instance for a type, with defaults and superclass methods filled in."""
    if type_name.startswith("List "):
        return _list_instance(class_name, type_name[len("List "):])
    if (class_name, type_name) not in INSTANCES:
        raise NoInstance("no instance of %s for %s" % (class_name, type_name))
    instance = dict(INSTANCES[(class_name, type_name)])
    superclass = CLASSES[class_name].get("superclass")
    if superclass:
        instance.update(resolve(superclass, type_name))
        instance.update(INSTANCES[(class_name, type_name)])
    for name, builder in CLASSES[class_name]["defaults"].items():
        if name not in instance:
            instance[name] = builder(instance)
    return instance


def _list_instance(class_name, element_type):
    """The instance for a list, built from the instance for the elements.

    This is the constraint in an instance head: lists can be compared exactly
    when their elements can, and the instance is derived rather than written
    out for every element type.
    """
    element = resolve(class_name, element_type)
    if class_name == "Eq":
        instance = {"equals": lambda left, right:
                    len(left) == len(right)
                    and all(element["equals"](a, b) for a, b in zip(left, right))}
    else:
        instance = {"less": lambda left, right: _lexicographic(element, left,
                                                              right)}
        instance.update(_list_instance("Eq", element_type))
    for name, builder in CLASSES[class_name]["defaults"].items():
        if name not in instance:
            instance[name] = builder(instance)
    return instance


def _lexicographic(element, left, right):
    """Whether the first list precedes the second, element by element."""
    for first, second in zip(left, right):
        if element["less"](first, second):
            return True
        if element["less"](second, first):
            return False
    return len(left) < len(right)


def has_instance(class_name, type_name):
    """Whether an instance exists."""
    try:
        resolve(class_name, type_name)
        return True
    except NoInstance:
        return False
