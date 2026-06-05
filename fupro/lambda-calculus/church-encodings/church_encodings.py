"""The course's own lambda terms, and what they compute.

The file ``terms.txt`` distributed with the lecture defines twenty-one terms:
the identity, the divergent term, the numerals and their arithmetic, the
booleans, and lists with their length, map and concatenation. They are
reproduced here verbatim, and every one is checked by reducing it and reading
the result back as a Python value.

Nothing but functions is available, so a number is what it does: the numeral
n applies a function n times. That is the whole encoding, and addition,
multiplication and the list operations all follow from it.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "syntax-and-substitution"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "reduction-strategies"))
import reduction_strategies as reduction
import syntax_and_substitution as syntax

COURSE_TERMS = {
    "I": "\\x.x",
    "OMEGA": "((\\x.(x x)) (\\x.(x x)))",
    "Z": "\\f.\\x. x",
    "S": "\\n.\\f.\\x. f (n f x)",
    "ZERO": "\\f.\\x. x",
    "TRUE": "\\t.\\f. t",
    "FALSE": "\\t.\\f. f",
    "NOT": "\\p.p (\\t.\\f. f) (\\t.\\f. t)",
    "AND": "\\l.\\r. l r l",
    "OR": "\\l.\\r. l l r",
    "NIL": "\\n.\\c.n",
    "CONS": "\\a.\\l.\\n.\\c. c a (l n c)",
    "LENGTH": "\\l. l (\\f.\\x. x) (\\a. \\n.\\f.\\x. f (n f x))",
    "MAP": "\\f.\\l. l (\\n.\\c.n) (\\a. (\\a.\\l.\\n.\\c. c a (l n c)) (f a))",
    "CONCAT": "\\a.\\b. a b (\\a.\\l.\\n.\\c. c a (l n c))",
}
"""The terms of the lecture's ``terms.txt``, with the definitions inlined."""

COURSE_TERMS["ONE"] = "((%s) (%s))" % (COURSE_TERMS["S"], COURSE_TERMS["Z"])
COURSE_TERMS["TWO"] = "((%s) (%s))" % (COURSE_TERMS["S"], COURSE_TERMS["ONE"])
COURSE_TERMS["THREE"] = "((%s) (%s))" % (COURSE_TERMS["S"], COURSE_TERMS["TWO"])
COURSE_TERMS["ADD"] = "\\n.\\m. n (%s) m" % COURSE_TERMS["S"]
COURSE_TERMS["MULT"] = "\\n.\\m. n ((%s) m) (%s)" % (COURSE_TERMS["ADD"],
                                                     COURSE_TERMS["Z"])
COURSE_TERMS["NEZ"] = "(%s) (%s) ((%s) (%s) ((%s) (%s) (%s)))" % (
    COURSE_TERMS["CONS"], COURSE_TERMS["ZERO"], COURSE_TERMS["CONS"],
    COURSE_TERMS["ONE"], COURSE_TERMS["CONS"], COURSE_TERMS["TWO"],
    COURSE_TERMS["NIL"])
COURSE_TERMS["EVEN"] = "\\n. n (\\p.\\t.\\f. p f t) (\\t.\\f. t)"
"""The exam's parity predicate: negate as often as the numeral says.

The order of the two arguments is the part worth stating. A numeral of the
course file applies its first argument to its second, so the function comes
first and the starting value second. The exam writes its numerals the other
way round, as a fold with the zero case first, and a predicate written for
one convention computes nothing under the other.
"""


def term(name):
    """The parsed term of the course file, by name."""
    if name not in COURSE_TERMS:
        raise ValueError("no such term: %s" % name)
    return syntax.parse(COURSE_TERMS[name])


def apply(*names):
    """Applies the named terms to each other, left to right.

    A name is looked up in the course file and anything else is taken as a
    term already built, so the result of one application can be fed into the
    next.
    """
    result = None
    for name in names:
        piece = term(name) if isinstance(name, str) and name in COURSE_TERMS \
            else (syntax.parse(name) if isinstance(name, str) else name)
        result = piece if result is None else syntax.application(result, piece)
    return reduction.normal_form(result)


def numeral(number):
    """The Church numeral of a natural number."""
    body = syntax.variable("x")
    for _ in range(number):
        body = syntax.application(syntax.variable("f"), body)
    return syntax.abstraction("f", syntax.abstraction("x", body))


def to_integer(value):
    """Reads a Church numeral back as an integer."""
    normal = reduction.normal_form(value) if value[0] != "lam" else value
    if normal is None or normal[0] != "lam":
        raise ValueError("not a numeral: %s" % syntax.to_text(value))
    body = normal[2]
    if body[0] != "lam":
        raise ValueError("not a numeral")
    count = 0
    inner = body[2]
    while inner[0] == "app":
        count += 1
        inner = inner[2]
    return count


def to_boolean(value):
    """Reads a Church boolean back as a boolean."""
    applied = reduction.normal_form(syntax.application(
        syntax.application(value, syntax.variable("yes")),
        syntax.variable("no")))
    return syntax.to_text(applied) == "yes"


def binary(number):
    """The Church encoding of the exam's binary numerals.

    The data type has three constructors, so the encoding takes three
    arguments: one for the marker at the least significant end and one for
    each kind of bit. This is the general rule for encoding an algebraic data
    type, and the exam asks for exactly this case.

    The nesting direction is the part that is easy to get backwards. The
    marker sits innermost, so the constructor closest to it carries the
    lowest place value and the outermost one carries the highest: the exam's
    ``One (Zero LSB)`` is 2 and not 1.
    """
    bits = []
    value = number
    while value:
        bits.append(value % 2)
        value //= 2
    body = syntax.variable("lsb")
    for bit in bits:
        body = syntax.application(syntax.variable("one" if bit else "zero"),
                                  body)
    return syntax.abstraction("lsb", syntax.abstraction(
        "zero", syntax.abstraction("one", body)))


def binary_to_integer(value):
    """Reads such an encoding back as an integer."""
    text = syntax.to_text(reduction.normal_form(value))
    inner = text.split(".", 3)[-1]
    total = 0
    for symbol in inner.replace("(", " ").replace(")", " ").split():
        if symbol == "zero":
            total = total * 2
        elif symbol == "one":
            total = total * 2 + 1
    return total
