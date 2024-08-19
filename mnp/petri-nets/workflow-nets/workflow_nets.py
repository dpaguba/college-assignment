"""Workflow nets, soundness, and the net fragments behind BPMN.

A BPMN diagram has no semantics of its own. The meaning of a gateway is given
by the net fragment it stands for, and once a model is a Petri net the
questions a modeller cares about (will it always finish, can it deadlock, can
it leave work behind) are the standard net properties. Soundness packages
those three into one criterion.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "net-structure"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "reachability"))
import net_structure as nets
import reachability as reach


class WorkflowNet(nets.Net):
    """A net with a distinguished start place and end place."""

    def __init__(self, places, transitions, arcs, start, end):
        """Build a workflow net with one token in the start place."""
        nets.Net.__init__(self, places, transitions, arcs, {start: 1})
        self.start = start
        self.end = end

    def with_marking(self, marking):
        """A copy with a different marking, keeping start and end."""
        copy = WorkflowNet(self.places, self.transitions, self.arcs,
                           self.start, self.end)
        copy.marking = {place: count for place, count in marking.items() if count}
        return copy

    def is_workflow_net(self):
        """One source, one sink, and every node on a path between them."""
        if any(target == self.start for _, target in self.arcs):
            return False
        if any(source == self.end for source, _ in self.arcs):
            return False
        nodes = set(self.places) | set(self.transitions)
        return (self._reach_from(self.start) >= nodes and
                self._reach_to(self.end) >= nodes)

    def _reach_from(self, node):
        """The nodes reachable from a node by following arcs forwards."""
        seen, frontier = {node}, [node]
        while frontier:
            current = frontier.pop()
            for source, target in self.arcs:
                if source == current and target not in seen:
                    seen.add(target)
                    frontier.append(target)
        return seen

    def _reach_to(self, node):
        """The nodes that reach a node by following arcs backwards."""
        seen, frontier = {node}, [node]
        while frontier:
            current = frontier.pop()
            for source, target in self.arcs:
                if target == current and source not in seen:
                    seen.add(source)
                    frontier.append(source)
        return seen


def is_sound(net, limit=20000):
    """Soundness: the final marking is always reachable and always the last.

    Three conditions in one. Termination, because the final marking is
    reachable from everywhere; proper completion, because no marking has a
    token in the end place alongside anything else; and no dead transitions,
    because every transition appears somewhere in the graph.
    """
    if not net.is_workflow_net():
        return False
    final = frozenset({(net.end, 1)})
    try:
        structure = reach.graph(net, limit)
    except ValueError:
        return False
    if final not in structure["nodes"]:
        return False
    for node in structure["nodes"]:
        state = net.with_marking(dict(node))
        if final not in reach.reachable(state, limit):
            return False
        if dict(node).get(net.end, 0) and dict(node) != {net.end: 1}:
            return False
    used = {label for _, label, _ in structure["edges"]}
    return not set(net.transitions) - used


def bpmn_pattern(name):
    """The Petri net fragment a BPMN pattern stands for."""
    catalogue = {
        "task": {"places": 2, "transitions": 1,
                 "note": "перехід між вхідним і вихідним місцем"},
        "parallel gateway": {"places": 4, "transitions": 2,
                             "note": "AND-split і AND-join, два паралельні місця"},
        "exclusive gateway": {"places": 3, "transitions": 2,
                              "note": "XOR: два переходи з одного місця"},
        "sequence": {"places": 3, "transitions": 2,
                     "note": "два переходи один за одним"},
    }
    if name not in catalogue:
        raise ValueError("невідомий шаблон: %s" % name)
    return catalogue[name]
