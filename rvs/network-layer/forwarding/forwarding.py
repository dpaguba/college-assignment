"""Forwarding: the longest prefix match, and route aggregation.

A forwarding table maps prefixes to interfaces, and a lookup takes the **most
specific** matching entry. That rule is what lets a default route coexist with
exceptions to it, and it is why the table's order does not matter.

Aggregation is the reverse: two adjacent prefixes of the same length pointing
at the same interface merge into one shorter prefix. That is what keeps the
global routing table from growing with every network that is connected.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "ip-addressing"))
import ip_addressing as ip


def lookup(table, address):
    """The interface for an address, by longest prefix match."""
    target = int(ip.Address(address))
    best = None

    for prefix, interface in table:
        network = ip.Network(prefix)
        if network.contains(ip.Address(target)):
            if best is None or network.prefix > best[0]:
                best = (network.prefix, interface)

    return best[1] if best else None


def aggregate(table):
    """Merge adjacent prefixes of equal length and equal interface.

    Two `/25` blocks that are siblings become one `/24`. The check that they
    are **siblings** rather than merely adjacent is what makes this safe: a
    prefix must start at a multiple of its size, so only one of the two
    possible pairings is a valid merge.
    """
    entries = [(ip.Network(prefix), interface) for prefix, interface in table]
    changed = True

    while changed:
        changed = False
        for index, (first, first_interface) in enumerate(entries):
            for offset, (second, second_interface) in enumerate(entries):
                if index == offset or first_interface != second_interface:
                    continue
                if first.prefix != second.prefix or first.prefix == 0:
                    continue

                size = first.address_count()
                if abs(first.base - second.base) != size:
                    continue

                low = min(first.base, second.base)
                if low % (2 * size) != 0:
                    continue

                merged = ip.Network(f"{ip.Address(low)}/{first.prefix - 1}")
                entries = [entry for position, entry in enumerate(entries)
                           if position not in (index, offset)]
                entries.append((merged, first_interface))
                changed = True
                break
            if changed:
                break

    return sorted(((str(network), interface) for network, interface in entries),
                  key=lambda entry: (ip.Network(entry[0]).base,
                                     ip.Network(entry[0]).prefix))


def table_size(table):
    """How many entries a table has, which is what router memory costs."""
    return len(table)


def default_route_is_last_resort(table):
    """Whether the table has a default route, and that nothing is more general.

    A `/0` matches everything, so under longest prefix match it is used exactly
    when nothing else matches. That is not a special case in the lookup, it is
    the same rule applied to the least specific possible entry.
    """
    return any(prefix.endswith("/0") for prefix, _ in table)
