"""Cache coherence: MSI and MESI on a snooping bus.

With one cache per processor, the same address can sit in several caches at
once, and a write in one of them makes the others wrong. A coherence protocol
is the rule that stops that, and the states are what each cache records about
its own copy.

MSI has three: **Modified**, the only valid copy and it is dirty; **Shared**,
one of possibly several clean copies; **Invalid**, no usable copy.

MESI adds **Exclusive**: the only copy, and clean. That fourth state exists for
one reason, and it is a measurable one. In MSI, reading a line and then writing
it costs two bus transactions, because the read leaves the line Shared and the
write must announce the upgrade. In MESI the read leaves it Exclusive, so the
write is silent.
"""

from __future__ import annotations


class System:
    """A set of processors with private caches on a snooping bus."""

    def __init__(self, processors, protocol="msi"):
        """Start every line invalid in every cache."""
        self.processors = processors
        self.protocol = protocol
        self.caches = [{} for _ in range(processors)]
        self.messages = 0

    def state(self, processor, address):
        """The state of a line in one cache."""
        return self.caches[processor].get(address, "I")

    def _sharers(self, address, exclude=None):
        """Which other caches hold a valid copy."""
        return [index for index in range(self.processors)
                if index != exclude and self.state(index, address) != "I"]

    def read(self, processor, address):
        """A read: fetch the line if it is not already valid here.

        A read hit costs nothing. A read miss goes on the bus, and what the
        line becomes depends on whether anyone else has it: Shared if they do,
        and under MESI Exclusive if they do not.
        """
        if self.state(processor, address) != "I":
            return "hit"

        others = self._sharers(address, exclude=processor)
        self.messages += 1

        for other in others:
            if self.state(other, address) == "M":
                self.caches[other][address] = "S"
                self.messages += 1
            elif self.state(other, address) == "E":
                self.caches[other][address] = "S"

        if others or self.protocol == "msi":
            self.caches[processor][address] = "S"
        else:
            self.caches[processor][address] = "E"

        return "miss"

    def write(self, processor, address):
        """A write: become the only valid copy.

        Every other cache is invalidated, which is what makes this a write
        **invalidate** protocol. The alternative, broadcasting the new value,
        is a write update protocol and loses on bandwidth for everything except
        tightly shared data.
        """
        current = self.state(processor, address)

        if current == "M":
            return "hit"

        if current == "E":
            self.caches[processor][address] = "M"
            return "silent upgrade"

        self.messages += 1
        for other in self._sharers(address, exclude=processor):
            self.caches[other][address] = "I"

        self.caches[processor][address] = "M"
        return "miss" if current == "I" else "upgrade"

    def invariant_holds(self, address):
        """Whether at most one cache has the line modified.

        The property the protocol exists to maintain, checked directly rather
        than trusted. A protocol that keeps two modified copies has lost, and
        no amount of correct-looking state transitions makes up for it.
        """
        return sum(1 for index in range(self.processors)
                   if self.state(index, address) == "M") <= 1


def ping_pong_cost(iterations, protocol="msi"):
    """Bus messages when two processors write the same line in turn.

    The worst case for any invalidate protocol, and the reason two threads
    updating adjacent counters can run slower than one thread doing both. Each
    write invalidates the other cache and takes the line back, so the traffic
    is proportional to the number of writes and not to the amount of data.
    """
    system = System(processors=2, protocol=protocol)

    for _ in range(iterations):
        system.write(0, 0x40)
        system.write(1, 0x40)

    return system.messages
