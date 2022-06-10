"""The Post correspondence problem: dominoes that must spell the same word.

Given pairs of strings ``(u_i, v_i)``, is there a non-empty sequence of indices
with

    u_i1 u_i2 ... u_ik  =  v_i1 v_i2 ... v_ik

It looks like a puzzle and it is **undecidable**, which is what makes it
valuable: it is the standard tool for proving other problems undecidable,
because reducing from it is usually easier than reducing from halting.

The undecidability is by reduction from the halting problem: the dominoes are
built so that the only way to match is to spell out an accepting computation of
a machine, step by step. Solving the puzzle would decide halting.

Search here is bounded by construction. There is no other option: an unbounded
search would be a decision procedure for an undecidable problem.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Domino:
    """One pair of strings, written as a fraction in the lectures."""

    top: str
    bottom: str

    def __str__(self):
        """The domino as a fraction, top over bottom."""
        return f"({self.top}/{self.bottom})"


def solve(dominoes, max_length=12, max_width=40):
    """Search for a matching sequence, bounded in length and in string size.

    Breadth-first over partial matches, keeping only the **overhang**: the part
    of one side already written that the other has not caught up with. Two
    partial solutions with the same overhang behave identically from then on,
    so the search state is the overhang and not the whole pair of strings.

    Returns the indices of a solution, or None when the bound is reached, which
    is not the same as "there is none".
    """
    start = []
    queue = [(0, "", "")]
    seen = {("", "")}

    while queue:
        depth, top, bottom = queue.pop(0)
        if depth >= max_length:
            continue

        for index, domino in enumerate(dominoes):
            new_top = top + domino.top
            new_bottom = bottom + domino.bottom

            shared = min(len(new_top), len(new_bottom))
            if new_top[:shared] != new_bottom[:shared]:
                continue

            overhang = (new_top[shared:], new_bottom[shared:])
            if max(len(overhang[0]), len(overhang[1])) > max_width:
                continue

            path = _reconstruct(queue, depth, top, bottom, index)

            if new_top == new_bottom and new_top:
                return _search_path(dominoes, new_top, max_length)

            key = overhang
            if key not in seen:
                seen.add(key)
                queue.append((depth + 1, new_top, new_bottom))

    return None


def _reconstruct(queue, depth, top, bottom, index):
    """Placeholder kept so the search reads as a breadth-first walk."""
    return None


def _search_path(dominoes, target, max_length):
    """Recover an index sequence spelling a known solution string."""
    def walk(prefix_top, prefix_bottom, chosen):
        """Extends the chosen sequence while the two strings can still agree."""
        if prefix_top == prefix_bottom == target:
            return chosen
        if len(chosen) > max_length:
            return None

        for index, domino in enumerate(dominoes):
            top = prefix_top + domino.top
            bottom = prefix_bottom + domino.bottom
            if not target.startswith(top) or not target.startswith(bottom):
                continue
            found = walk(top, bottom, chosen + [index])
            if found:
                return found

        return None

    return walk("", "", [])


def check(dominoes, indices):
    """Verify a claimed solution: both sides must spell the same non-empty word."""
    if not indices:
        return False, "", ""

    top = "".join(dominoes[index].top for index in indices)
    bottom = "".join(dominoes[index].bottom for index in indices)
    return top == bottom, top, bottom


def modified_to_standard(dominoes, first_index=0):
    """Reduce the modified problem, where a fixed domino must start, to the plain one.

    Every symbol is padded: ``*`` after each character on the top and before
    each character on the bottom, so the two sides can only stay aligned by
    respecting the intended order. A special start domino and a special end
    domino force the first and last positions.

    This construction is the one step of the undecidability proof that can be
    run rather than described, which is why it is here: the reduction from
    halting produces a *modified* instance, and this turns it into a plain one.
    """
    def pad_after(text):
        """The text with a marker after every symbol."""
        return "".join(symbol + "*" for symbol in text)

    def pad_before(text):
        """The text with a marker before every symbol."""
        return "".join("*" + symbol for symbol in text)

    padded = [Domino(pad_after(domino.top), pad_before(domino.bottom))
              for domino in dominoes]

    start = Domino("*" + padded[first_index].top, padded[first_index].bottom)
    end = Domino("$", "*$")

    return [start] + padded + [end]


def example_with_solution():
    """A small instance that does match, from the standard textbook set."""
    return [Domino("a", "baa"), Domino("ab", "aa"), Domino("bba", "bb")]


def example_without_solution():
    """An instance where no sequence can match.

    Every domino makes the top longer than the bottom, so the two sides can
    never level out. That is a proof for this instance, and no such argument
    works in general, which is precisely why the problem is undecidable.
    """
    return [Domino("ab", "a"), Domino("bb", "b"), Domino("aab", "ab")]
