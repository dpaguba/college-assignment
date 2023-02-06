"""Switches, learning, and the address resolution protocol.

A switch is a bridge with many ports and no configuration. It learns where a
host is by watching the **source** address of the frames it receives, and it
forwards by looking up the **destination**. A destination it has not learned is
flooded to every other port, which is correct and wasteful and self-correcting:
the reply teaches it the way back.

That is the whole algorithm, and it is why a switch is plug-and-play in a way a
router is not.
"""

from __future__ import annotations


class Switch:
    """A learning switch: a table from address to port."""

    def __init__(self):
        """Start with an empty table."""
        self.table = {}

    def receive(self, port, source, destination):
        """Learn the source, then decide what to do with the frame.

        Three outcomes. A known destination on another port is **forwarded**; a
        known destination on the same port is **dropped**, because the two
        hosts are on the same segment and have already heard each other; an
        unknown destination is **flooded**.
        """
        self.table[source] = port

        target = self.table.get(destination)
        if target is None:
            return {"action": "flood", "port": None}
        if target == port:
            return {"action": "drop", "port": port}
        return {"action": "forward", "port": target}

    def forget(self, address):
        """Remove an entry, which is what an ageing timer does.

        Entries expire because hosts move. Without ageing, unplugging a machine
        and plugging it into another port would black-hole its traffic until
        the switch was restarted.
        """
        self.table.pop(address, None)


class ArpCache:
    """A mapping from network addresses to hardware addresses."""

    def __init__(self):
        """Start empty."""
        self.entries = {}

    def learn(self, address, hardware):
        """Record a mapping, usually from a broadcast reply."""
        self.entries[address] = hardware

    def lookup(self, address):
        """The hardware address, or `None` if it must be asked for."""
        return self.entries.get(address)

    def resolve(self, address):
        """What a host does when the mapping is missing.

        It broadcasts a question to the whole segment and the owner answers.
        Everyone else hears both, which is why an ARP cache fills up without
        anyone asking, and why spoofing a reply is so easy.
        """
        if address in self.entries:
            return {"action": "cached", "hardware": self.entries[address]}
        return {"action": "broadcast", "hardware": None}


def layer_of(device):
    """Which layer a device operates at.

    A switch reads hardware addresses and needs none of its own; a router reads
    network addresses and has one per interface. That difference decides
    everything else: a switch cannot split a broadcast domain and a router
    cannot avoid being configured.
    """
    return {"hub": 1, "switch": 2, "bridge": 2, "router": 3}[device]


def broadcast_domain(devices):
    """How many broadcast domains a set of devices creates.

    One per router interface. Hubs and switches pass broadcasts through, which
    is why a large switched network floods and why the fix is subnetting rather
    than a faster switch.
    """
    return sum(1 for device in devices if layer_of(device) == 3) or 1
