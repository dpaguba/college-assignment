"""Grammars and pushdown automata describe the same languages.

Two constructions, and the pair is the second equivalence theorem of the
course, matching Kleene's for the regular level.

**Grammar to automaton** is short: one state, the stack holds the part of the
sentential form still to be derived, and the machine simulates a leftmost
derivation. Expanding a variable is popping it and pushing its right-hand side;
matching a terminal is popping it while reading the same input symbol.

**Automaton to grammar** is the hard direction. A variable ``[p X q]`` stands
for "starting in state p with X on top, the automaton can consume some input
and end in state q with X removed". The rules mirror the transitions, and the
number of variables is cubic in the size of the automaton, which is why nobody
runs this construction in practice and everyone can state it.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "context-free-grammars"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "pushdown-automata"))

from context_free_grammars import Grammar
from pushdown_automata import EPSILON, PDA, to_empty_stack


def grammar_to_pda(grammar, name=None):
    """Build a one-state PDA accepting the language by empty stack.

    The stack starts with the start variable. Two kinds of move:

    - ``(q, eps, A) -> (q, alpha)`` for every rule ``A -> alpha``: expand
    - ``(q, a, a) -> (q, eps)`` for every terminal a: match and consume

    The stack is exactly the suffix of the current leftmost sentential form
    that has not been matched yet, which is why one state suffices: all the
    memory is in the stack.
    """
    transitions = {}

    for variable, sides in grammar.rules.items():
        for right in sides:
            transitions.setdefault(("q", EPSILON, variable), set()).add(("q", "".join(right)))

    for terminal in grammar.terminals:
        transitions.setdefault(("q", terminal, terminal), set()).add(("q", ""))

    return PDA({"q"}, tuple(sorted(grammar.terminals)),
               tuple(sorted(grammar.variables | grammar.terminals)),
               transitions, "q", grammar.start, set(), "empty",
               name or f"pda({grammar.name})")


def pda_to_grammar(pda, name=None, max_states=6):
    """Build a grammar for the language of a PDA, by the triple construction.

    A variable ``[p X q]`` derives exactly the input words that take the
    automaton from state p to state q while removing X from the stack. The
    start rules say the whole run must remove the initial stack symbol.

    For a transition ``(p, a, X) -> (r, Y1...Yk)`` the rule is

        [p X q] -> a [r Y1 s1] [s1 Y2 s2] ... [s(k-1) Yk q]

    over every choice of intermediate states, which is where the cubic blow-up
    comes from: one rule per combination.

    Only sensible for small automata, hence ``max_states``. The construction is
    a proof that the languages coincide, not an algorithm anybody runs.
    """
    pda = to_empty_stack(pda)

    if len(pda.states) > max_states:
        raise ValueError(f"the automaton has {len(pda.states)} states, which makes "
                         f"the construction produce more rules than is useful")

    states = sorted(pda.states, key=str)
    rules = {}
    start = "S0"

    def variable(left, symbol, right):
        """The name of the triple variable used by the standard construction."""
        return f"[{left},{symbol},{right}]"

    for state in states:
        rules.setdefault(start, []).append((variable(pda.start, pda.start_stack, state),))

    for (source, read, top), targets in pda.transitions.items():
        for target, pushed in targets:
            symbols = list(pushed)

            for finish in states:
                head = variable(source, top, finish)

                if not symbols:
                    if target == finish:
                        body = (read,) if read else ()
                        rules.setdefault(head, [])
                        if body not in rules[head]:
                            rules[head].append(body)
                    continue

                for chain in _state_chains(states, len(symbols) - 1):
                    middle = [target] + list(chain) + [finish]
                    body = ([read] if read else []) + [
                        variable(middle[index], symbols[index], middle[index + 1])
                        for index in range(len(symbols))]
                    rules.setdefault(head, [])
                    if tuple(body) not in rules[head]:
                        rules[head].append(tuple(body))

    variables = set(rules)
    for sides in list(rules.values()):
        for body in sides:
            for symbol in body:
                if symbol.startswith("["):
                    variables.add(symbol)

    for symbol in variables:
        rules.setdefault(symbol, [])

    grammar = Grammar(variables, set(pda.input_alphabet),
                      {head: sides for head, sides in rules.items() if sides},
                      start, name or f"grammar({pda.name})")

    import sys as _sys
    from pathlib import Path as _Path
    _sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "grammar-cleanup"))
    from grammar_cleanup import remove_useless

    return remove_useless(grammar, grammar.name)


def _state_chains(states, length):
    """Every tuple of intermediate states of a given length."""
    if length == 0:
        yield ()
        return
    for head in states:
        for rest in _state_chains(states, length - 1):
            yield (head,) + rest


def round_trip(grammar, max_length=5):
    """Grammar to automaton and back, comparing the languages.

    The grammar that comes back is unrecognisable and describes the same
    language, which is the only claim the theorem makes.
    """
    pda = grammar_to_pda(grammar)
    recovered = pda_to_grammar(pda)

    import sys as _sys
    from pathlib import Path as _Path
    _sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "cyk"))
    _sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "chomsky-normal-form"))
    from chomsky_normal_form import to_chomsky_normal_form
    from cyk import language

    original = language(to_chomsky_normal_form(grammar), max_length)
    through_pda = pda.language(max_length)

    return {
        "grammar language": original,
        "pda language": through_pda,
        "match": original == through_pda,
        "recovered variables": len(recovered.variables),
    }
