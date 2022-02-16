"""Prenex form, Skolemisation and the clause form of the matrix.

Resolution needs clauses, and a first-order formula is not one. Three
transformations get it there:

1. **rename apart**, so no two quantifiers bind the same name
2. **prenex form**, pulling every quantifier to the front
3. **Skolemisation**, replacing each existential by a function of the
   universals that enclose it

The first two preserve equivalence. The third does **not**: it preserves only
satisfiability, and that is enough, because resolution proves unsatisfiability
and nothing else. Conflating the two is the standard mistake, and it matters:
`forall x exists y R(x,y)` and `forall x R(x,f(x))` have different models, and
either both or neither has one.
"""

from __future__ import annotations

import itertools
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "structures-and-models"))
import structures_and_models as sm

parse = sm.parse
free_variables = sm.free_variables


def to_text(formula):
    """Print a formula."""
    kind = formula[0]

    if kind == "atom":
        if not formula[2]:
            return formula[1]
        return f"{formula[1]}({','.join(_term_text(a) for a in formula[2])})"
    if kind == "!":
        return "!" + to_text(formula[1])
    if kind in ("forall", "exists"):
        return f"{kind} {formula[1]} {to_text(formula[2])}"
    return f"({to_text(formula[1])} {kind} {to_text(formula[2])})"


def _term_text(term):
    """Print a term."""
    if isinstance(term, tuple):
        return f"{term[0]}({','.join(_term_text(a) for a in term[1])})"
    return term


def bound_variables(formula):
    """Every variable bound by a quantifier."""
    kind = formula[0]
    if kind == "atom":
        return []
    if kind == "!":
        return bound_variables(formula[1])
    if kind in ("forall", "exists"):
        return [formula[1]] + bound_variables(formula[2])
    return bound_variables(formula[1]) + bound_variables(formula[2])


def rename_apart(formula, counter=None):
    """Give every quantifier its own variable name.

    Without this the prenex step is wrong: pulling two quantifiers over the
    same name to the front makes one capture what the other bound. The sheets
    do it as the first line of every derivation for exactly that reason.
    """
    counter = counter if counter is not None else {"next": 1}
    return _rename(formula, {}, counter)


def _rename(formula, mapping, counter):
    """Rename bound variables, carrying the mapping down."""
    kind = formula[0]

    if kind == "atom":
        return ("atom", formula[1],
                [_rename_term(argument, mapping) for argument in formula[2]])
    if kind == "!":
        return ("!", _rename(formula[1], mapping, counter))
    if kind in ("forall", "exists"):
        fresh = f"{formula[1]}{counter['next']}"
        counter["next"] += 1
        inner = dict(mapping, **{formula[1]: fresh})
        return (kind, fresh, _rename(formula[2], inner, counter))
    return (kind, _rename(formula[1], mapping, counter),
            _rename(formula[2], mapping, counter))


def _rename_term(term, mapping):
    """Apply a renaming to a term."""
    if isinstance(term, tuple):
        return (term[0], [_rename_term(argument, mapping) for argument in term[1]])
    return mapping.get(term, term)


def to_prenex(formula):
    """Pull every quantifier to the front, after renaming apart.

    The connectives are eliminated down to negation, conjunction and
    disjunction first, because the rule for moving a quantifier over an
    implication depends on which side it is on, and the rule for moving one
    over an equivalence does not exist.
    """
    current = rename_apart(_eliminate(formula))

    while True:
        result = _pull(current)
        if result is None:
            return current
        current = result


def _eliminate(formula):
    """Rewrite implication and equivalence away."""
    kind = formula[0]

    if kind == "atom":
        return formula
    if kind == "!":
        return ("!", _eliminate(formula[1]))
    if kind in ("forall", "exists"):
        return (kind, formula[1], _eliminate(formula[2]))
    if kind == "->":
        return ("|", ("!", _eliminate(formula[1])), _eliminate(formula[2]))
    if kind == "<->":
        left, right = _eliminate(formula[1]), _eliminate(formula[2])
        return ("&", ("|", ("!", left), right), ("|", ("!", right), left))
    return (kind, _eliminate(formula[1]), _eliminate(formula[2]))


def _pull(formula):
    """One step of moving a quantifier outwards, or `None` when done."""
    kind = formula[0]

    if kind == "!":
        inner = formula[1]
        if inner[0] == "forall":
            return ("exists", inner[1], ("!", inner[2]))
        if inner[0] == "exists":
            return ("forall", inner[1], ("!", inner[2]))
        rewritten = _pull(inner)
        return ("!", rewritten) if rewritten else None

    if kind in ("&", "|"):
        for index, other in ((1, 2), (2, 1)):
            if formula[index][0] in ("forall", "exists"):
                quantifier = formula[index]
                rest = formula[other]
                body = ((kind, quantifier[2], rest) if index == 1
                        else (kind, rest, quantifier[2]))
                return (quantifier[0], quantifier[1], body)

        for index in (1, 2):
            rewritten = _pull(formula[index])
            if rewritten is not None:
                parts = list(formula)
                parts[index] = rewritten
                return tuple(parts)
        return None

    if kind in ("forall", "exists"):
        rewritten = _pull(formula[2])
        return (kind, formula[1], rewritten) if rewritten else None

    return None


def is_prenex(formula):
    """Whether every quantifier stands in front of a quantifier-free matrix."""
    current = formula
    while current[0] in ("forall", "exists"):
        current = current[2]
    return not bound_variables(current)


def quantifier_prefix(formula):
    """The quantifier prefix of a prenex formula, as strings."""
    prefix = []
    current = formula
    while current[0] in ("forall", "exists"):
        prefix.append(f"{current[0]} {current[1]}")
        current = current[2]
    return prefix


def matrix(formula):
    """The quantifier-free part of a prenex formula."""
    current = formula
    while current[0] in ("forall", "exists"):
        current = current[2]
    return current


def skolemise(formula, counter=None):
    """Replace each existential by a function of the universals before it.

    A leading existential becomes a constant, because no universal encloses it.
    That is the same rule, not a special case: a function of zero arguments.
    """
    counter = counter if counter is not None else {"next": 1}
    universals = []
    substitution = {}
    current = formula

    while current[0] in ("forall", "exists"):
        if current[0] == "forall":
            universals.append(current[1])
            current = current[2]
            continue

        name = f"f{counter['next']}"
        counter["next"] += 1
        substitution[current[1]] = ((name, list(universals)) if universals else (name, []))
        current = current[2]

    body = _substitute(current, substitution)
    for variable in reversed(universals):
        body = ("forall", variable, body)
    return body


def _substitute(formula, substitution):
    """Replace variables by terms throughout a formula."""
    kind = formula[0]

    if kind == "atom":
        return ("atom", formula[1],
                [_substitute_term(argument, substitution) for argument in formula[2]])
    if kind == "!":
        return ("!", _substitute(formula[1], substitution))
    if kind in ("forall", "exists"):
        return (kind, formula[1], _substitute(formula[2], substitution))
    return (kind, _substitute(formula[1], substitution),
            _substitute(formula[2], substitution))


def _substitute_term(term, substitution):
    """Replace variables by terms inside a term."""
    if isinstance(term, tuple):
        return (term[0], [_substitute_term(a, substitution) for a in term[1]])
    if term in substitution:
        replacement = substitution[term]
        if isinstance(replacement, tuple) and not replacement[1]:
            return replacement[0]
        return replacement
    return term


def matrix_clauses(formula):
    """The matrix of a Skolem formula as clauses, after conversion to CNF."""
    body = matrix(formula)
    body = _nnf(body)

    while True:
        result = _distribute(body)
        if result is None:
            break
        body = result

    return _collect(body)


def _nnf(formula):
    """Push negation inwards over the quantifier-free matrix."""
    kind = formula[0]

    if kind == "atom":
        return formula
    if kind == "!":
        inner = formula[1]
        if inner[0] == "!":
            return _nnf(inner[1])
        if inner[0] == "&":
            return ("|", _nnf(("!", inner[1])), _nnf(("!", inner[2])))
        if inner[0] == "|":
            return ("&", _nnf(("!", inner[1])), _nnf(("!", inner[2])))
        return formula
    return (kind, _nnf(formula[1]), _nnf(formula[2]))


def _distribute(formula):
    """One step of distributing disjunction over conjunction."""
    if formula[0] == "|":
        for index, other in ((1, 2), (2, 1)):
            if formula[index][0] == "&":
                inner = formula[index]
                rest = formula[other]
                return ("&", ("|", inner[1], rest), ("|", inner[2], rest))

    if formula[0] in ("&", "|"):
        for index in (1, 2):
            rewritten = _distribute(formula[index])
            if rewritten is not None:
                parts = list(formula)
                parts[index] = rewritten
                return tuple(parts)

    return None


def _collect(formula):
    """Split a CNF matrix into clauses of literals."""
    def literals(current):
        """Collect the literals of one clause."""
        if current[0] == "|":
            return literals(current[1]) + literals(current[2])
        return [to_text(current)]

    def conjuncts(current):
        """Split a conjunction into clauses."""
        if current[0] == "&":
            return conjuncts(current[1]) + conjuncts(current[2])
        return [literals(current)]

    return conjuncts(formula)


def _small_structures(formula, size):
    """Every structure of a given size over the formula's relation symbols."""
    relations = _relation_symbols(formula)
    domain = list(range(size))

    slots = []
    for name, arity in sorted(relations.items()):
        slots.append((name, [tuple(t) for t in itertools.product(domain, repeat=arity)]))

    counts = [len(tuples) for _, tuples in slots]
    for bits in itertools.product([False, True], repeat=sum(counts)):
        index = 0
        interpretation = {}
        for (name, tuples), count in zip(slots, counts):
            interpretation[name] = {tup for tup, keep in
                                    zip(tuples, bits[index:index + count]) if keep}
            index += count
        yield domain, interpretation


def _relation_symbols(formula):
    """The relation symbols of a formula with their arities."""
    kind = formula[0]
    if kind == "atom":
        return {formula[1]: len(formula[2])}
    if kind == "!":
        return _relation_symbols(formula[1])
    if kind in ("forall", "exists"):
        return _relation_symbols(formula[2])
    result = dict(_relation_symbols(formula[1]))
    result.update(_relation_symbols(formula[2]))
    return result


def same_models(first, second, size=3):
    """Whether two formulas hold in exactly the same small structures.

    A finite check of an infinite property, so it refutes rather than proves.
    That is enough for its purpose here: prenex conversion is supposed to
    preserve equivalence, and a disagreement on a three-element structure would
    show that it does not.

    Formulas containing function symbols are rejected rather than silently
    mishandled. Comparing a formula with its Skolem form is the natural thing
    to try and the wrong question: Skolemisation does not preserve
    equivalence, and `satisfiability_agrees` is what applies there.
    """
    for formula in (first, second):
        if _function_symbols(formula):
            raise ValueError("same_models compares relation-only formulas; "
                             "use satisfiability_agrees for Skolem forms")

    for domain, relations in _small_structures(first, size):
        structure = sm.Structure(domain, relations)
        if structure.models(first) != structure.models(second):
            return False
    return True


def satisfiability_agrees(original, skolem, size=3):
    """Whether both formulas have a model among the small structures.

    The weaker property Skolemisation guarantees. Checking it separately from
    equivalence is the point: `forall x exists y R(x,y)` and its Skolem form
    disagree on some structures and agree on whether any structure satisfies
    them.
    """
    functions = _function_symbols(skolem)

    original_satisfiable = any(
        sm.Structure(domain, relations).models(original)
        for domain, relations in _small_structures(original, size))

    skolem_satisfiable = False
    for domain, relations in _small_structures(skolem, size):
        for interpretation in _function_interpretations(functions, domain):
            structure = sm.Structure(domain, relations, functions=interpretation)
            if structure.models(skolem):
                skolem_satisfiable = True
                break
        if skolem_satisfiable:
            break

    return original_satisfiable == skolem_satisfiable


def _function_symbols(formula):
    """The function symbols of a formula with their arities."""
    result = {}

    def walk_term(term):
        """Collect function symbols inside a term."""
        if isinstance(term, tuple):
            result[term[0]] = len(term[1])
            for argument in term[1]:
                walk_term(argument)

    def walk(current):
        """Collect function symbols in a formula."""
        kind = current[0]
        if kind == "atom":
            for argument in current[2]:
                walk_term(argument)
        elif kind == "!":
            walk(current[1])
        elif kind in ("forall", "exists"):
            walk(current[2])
        else:
            walk(current[1])
            walk(current[2])

    walk(formula)
    return result


def _function_interpretations(functions, domain):
    """Every way of interpreting the function symbols over a domain."""
    if not functions:
        yield {}
        return

    names = sorted(functions)
    tables = []
    for name in names:
        arity = functions[name]
        inputs = [tuple(t) for t in itertools.product(domain, repeat=arity)]
        tables.append([dict(zip(inputs, values))
                       for values in itertools.product(domain, repeat=len(inputs))])

    for combination in itertools.product(*tables):
        interpretation = {}
        for name, table in zip(names, combination):
            interpretation[name] = (lambda table: lambda *args: table[args])(table)
        yield interpretation
