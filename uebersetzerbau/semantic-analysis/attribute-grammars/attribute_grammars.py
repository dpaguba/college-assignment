"""Attribute grammars: computing values on a parse tree.

A context-free grammar cannot express that two parts of a program agree. It
cannot require that a variable is declared before use, that argument counts
match, or that a word has as many `b`s as `a`s. Attributes are how a compiler
adds exactly that, without leaving the syntax-directed framework.

Each rule carries semantic rules computing attributes of the nodes it relates.
An attribute is **synthesized** when its value flows from the children upwards,
and **inherited** when it flows from the parent or the siblings downwards.

The sheet's example is the clean case: `{a^n b^n a^n}` is not context free, yet
a synthesized counter and one comparison decide membership.
"""

from __future__ import annotations


class CycleError(Exception):
    """The attribute dependencies contain a cycle, so no order exists."""


def evaluate(grammar, tree, rules):
    """Evaluate every attribute on a parse tree, in dependency order.

    Attributes are keyed by the path to their node: the empty string is the
    root, `.0` its first child, `.0.1` that child's second. The path form makes
    the dependency graph explicit and is what allows the evaluation order to be
    computed rather than assumed.

    The evaluator is deliberately general. A real compiler restricts itself to
    S-attributed or L-attributed grammars precisely so that this graph never
    has to be built, because those two classes can be evaluated during parsing.
    """
    values = {}
    pending = _tasks(grammar, tree, rules)

    progress = True
    while pending and progress:
        progress = False
        for task in list(pending):
            path, name, function, node_path, child_paths = task
            node = values.setdefault(node_path, {})
            children = [values.get(child, {}) for child in child_paths]

            try:
                result = function(node, children)
            except KeyError:
                continue

            values.setdefault(path, {})[name] = result
            _publish(values, path, name, result)
            pending.remove(task)
            progress = True

    if pending:
        raise CycleError(f"{len(pending)} attribute(s) could not be evaluated")

    return values


def _tasks(grammar, tree, rules):
    """One evaluation task per semantic rule occurrence in the tree."""
    tasks = []

    def walk(node, path):
        """Collect the semantic rules attached to one node's rule.

        The empty child a parse tree gives a nonterminal expanded by an epsilon
        rule is dropped here, so that the rule key is `("A", ())` and matches
        how the semantic rules are written.
        """
        if not node.children:
            return

        real = [(index, child) for index, child in enumerate(node.children)
                if child.symbol != ""]
        key = (node.symbol, tuple(child.symbol for _, child in real))
        child_paths = [f"{path}.{index}" for index, _ in real]

        for name, function in rules.get(key, {}).items():
            if "." in name:
                target, attribute = name.split(".", 1)
                index = _child_index([child for _, child in real], target)
                tasks.append((child_paths[index], attribute, function, path, child_paths))
            else:
                tasks.append((path, name, function, path, child_paths))

        for position, (index, child) in enumerate(real):
            walk(child, child_paths[position])

    walk(tree, "")
    return tasks


def _child_index(children, target):
    """Which child a rule name like `L.pos` refers to.

    A name may be a bare symbol, or a symbol with an index when the same
    nonterminal appears twice on the right side, which is why the sheet writes
    `A1` and `A2` rather than `A` twice.
    """
    if target and target[-1].isdigit():
        symbol, number = target[:-1], int(target[-1])
        occurrences = [index for index, child in enumerate(children)
                       if child.symbol == symbol]
        return occurrences[number - 1]

    for index, child in enumerate(children):
        if child.symbol == target:
            return index

    raise KeyError(f"no child named {target}")


def _publish(values, path, name, result):
    """Record a computed attribute so dependents can read it."""
    values.setdefault(path, {})[name] = result


def evaluation_order(grammar, tree, rules):
    """The order the attributes were actually computed in.

    Not unique, and that is the point: any order respecting the dependencies
    gives the same values, and finding one is the whole scheduling problem.
    A grammar for which no order exists is circular and is rejected.
    """
    values = {}
    pending = _tasks(grammar, tree, rules)
    order = []

    progress = True
    while pending and progress:
        progress = False
        for task in list(pending):
            path, name, function, node_path, child_paths = task
            node = values.setdefault(node_path, {})
            children = [values.get(child, {}) for child in child_paths]

            try:
                result = function(node, children)
            except KeyError:
                continue

            values.setdefault(path, {})[name] = result
            order.append(f"{path}.{name}")
            pending.remove(task)
            progress = True

    if pending:
        raise CycleError(f"{len(pending)} attribute(s) could not be evaluated")

    return order


def is_s_attributed(rules):
    """Whether every attribute is synthesized.

    An S-attributed grammar can be evaluated bottom up during a shift-reduce
    parse, with the attribute values living on the parser stack beside the
    states. That is why yacc's `$$` and `$1` exist and why they only ever look
    downwards.
    """
    return all("." not in name for rule in rules.values() for name in rule)


class _Probe(dict):
    """A dictionary that records which attributes a semantic rule reads.

    Every lookup returns zero, which supports the arithmetic and comparisons a
    semantic rule performs, so the rule can be run once purely to observe what
    it depends on. Straight-line rules are recorded exactly; a rule with a
    branch only reveals the side it took, which is why this reports a
    dependency set rather than proving one.
    """

    def __init__(self, seen, label):
        """Record where to store the accesses and under which label."""
        super().__init__()
        self.seen = seen
        self.label = label

    def __getitem__(self, key):
        """Record the access and return a neutral value."""
        self.seen.add((self.label, key))
        return 0


def dependencies(rules):
    """What each semantic rule reads, as (source, attribute) pairs.

    The source is `"parent"` for the node the rule belongs to, or the index of
    a child. Obtained by running each rule once against recording
    dictionaries rather than by parsing its source.
    """
    result = {}

    for key, rule in rules.items():
        arity = len(key[1])
        for name, function in rule.items():
            seen = set()
            node = _Probe(seen, "parent")
            children = [_Probe(seen, index) for index in range(arity)]
            try:
                function(node, children)
            except (KeyError, IndexError, TypeError, ZeroDivisionError):
                pass
            result[(key, name)] = seen

    return result


def is_l_attributed(rules):
    """Whether inherited attributes only read what a left-to-right pass has.

    L-attributed means each inherited attribute of child `i` depends only on
    the parent's own attributes and on children strictly to the left of `i`.
    That is exactly the information a recursive descent parser holds when it
    descends into child `i`, which is why L-attributed grammars can be
    evaluated during a top-down parse with no tree at all.

    An S-attributed grammar is L-attributed trivially, since it has no
    inherited attributes to constrain.
    """
    reads = dependencies(rules)

    for (key, name), seen in reads.items():
        if "." not in name:
            continue
        target = name.split(".", 1)[0]
        index = _child_index_by_name(key[1], target)
        for source, _ in seen:
            if source == "parent":
                continue
            if source >= index:
                return False

    return True


def _child_index_by_name(symbols, target):
    """Position of a symbol on a right side, resolving `A1`, `A2` suffixes."""
    if target and target[-1].isdigit():
        symbol, number = target[:-1], int(target[-1])
        occurrences = [index for index, name in enumerate(symbols) if name == symbol]
        return occurrences[number - 1]

    for index, name in enumerate(symbols):
        if name == target:
            return index

    raise KeyError(f"no symbol named {target}")


def classify(rules):
    """Which attributes are synthesized and which are inherited."""
    synthesized, inherited = set(), set()

    for rule in rules.values():
        for name in rule:
            if "." in name:
                inherited.add(name.split(".", 1)[1])
            else:
                synthesized.add(name)

    return {"synthesized": sorted(synthesized), "inherited": sorted(inherited)}
