"""Petri nets: places, transitions, arcs, and a marking.

A marking is a dictionary from place to token count with empty places left
out, so two markings that describe the same state compare equal and can be
used directly as nodes of the reachability graph.

Firing is local. A transition looks only at its own input places, which is
what makes the model concurrent by construction: two transitions that share no
input place are independent whether or not anything says so.
"""


class Net:
    """A Petri net together with its current marking."""

    def __init__(self, places, transitions, arcs, marking):
        """Build a net, rejecting arcs that name unknown nodes."""
        self.places = list(places)
        self.transitions = list(transitions)
        self.arcs = [tuple(arc) for arc in arcs]
        self.marking = {place: count for place, count in marking.items() if count}
        unknown = {node for arc in self.arcs for node in arc} - \
            set(self.places) - set(self.transitions)
        if unknown:
            raise ValueError("невідомі вузли: %s" % sorted(unknown))

    def preset(self, transition):
        """The input places of a transition."""
        return [source for source, target in self.arcs
                if target == transition and source in self.places]

    def postset(self, transition):
        """The output places of a transition."""
        return [target for source, target in self.arcs
                if source == transition and target in self.places]

    def weight(self, source, target):
        """The arc weight, counted as the number of parallel arcs."""
        return sum(1 for arc in self.arcs if arc == (source, target))

    def enabled(self, transition):
        """Whether every input place holds enough tokens."""
        return all(self.marking.get(place, 0) >= self.weight(place, transition)
                   for place in set(self.preset(transition)))

    def enabled_transitions(self):
        """Every transition enabled in the current marking."""
        return [transition for transition in self.transitions
                if self.enabled(transition)]

    def fire(self, transition):
        """The net that results from firing a transition."""
        if not self.enabled(transition):
            raise ValueError("перехід %s не активований" % transition)
        marking = dict(self.marking)
        for place in set(self.preset(transition)):
            marking[place] = marking.get(place, 0) - self.weight(place, transition)
        for place in set(self.postset(transition)):
            marking[place] = marking.get(place, 0) + self.weight(transition, place)
        return self.with_marking(marking)

    def with_marking(self, marking):
        """A copy of the net carrying a different marking."""
        return Net(self.places, self.transitions, self.arcs, marking)

    def in_conflict(self, first, second):
        """Conflict: a shared input place holding too few tokens for both.

    Sharing an input place is not enough on its own. Two transitions reading
    the same place conflict only when the tokens there cannot serve both,
    which is why the marking has to be consulted.
    """
        if first == second:
            return False
        shared = set(self.preset(first)) & set(self.preset(second))
        if not shared:
            return False
        if not (self.enabled(first) and self.enabled(second)):
            return False
        return any(self.marking.get(place, 0) <
                   self.weight(place, first) + self.weight(place, second)
                   for place in shared)

    def concurrent(self, first, second):
        """Concurrency: both enabled, and neither competes for the other's tokens."""
        return (first != second and self.enabled(first) and self.enabled(second)
                and not self.in_conflict(first, second))

    def key(self):
        """A hashable form of the marking."""
        return frozenset(self.marking.items())
