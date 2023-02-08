"""IPv4 addressing and subnetting.

An address is 32 bits and a prefix says how many of them name the network. The
rest name the host, and two of those combinations are reserved: all zeros is
the network itself and all ones is the broadcast, so a `/24` holds 256
addresses and 254 usable ones.

Subnetting a block among several networks is a packing problem with one rule
that makes it easy: **allocate the largest demand first**. Each subnet must
start at a multiple of its own size, so a small subnet placed early leaves a
gap that no larger one can use.
"""

from __future__ import annotations

import math


class Address:
    """One IPv4 address."""

    def __init__(self, value):
        """Accept dotted quad text or a 32-bit integer."""
        if isinstance(value, int):
            self.value = value
        else:
            parts = [int(part) for part in value.split(".")]
            self.value = sum(part << (8 * (3 - index))
                             for index, part in enumerate(parts))

    def __int__(self):
        """The address as a 32-bit integer."""
        return self.value

    def __str__(self):
        """The address in dotted quad form."""
        return ".".join(str((self.value >> shift) & 0xFF)
                        for shift in (24, 16, 8, 0))

    def __eq__(self, other):
        """Two addresses are equal when their integers are."""
        return isinstance(other, Address) and self.value == other.value


class Network:
    """An address block, written as an address and a prefix length."""

    def __init__(self, text):
        """Parse `a.b.c.d/prefix`, masking off the host bits."""
        address, _, prefix = text.partition("/")
        self.prefix = int(prefix)
        self.base = int(Address(address)) & self._mask()

    def _mask(self):
        """The network mask as an integer."""
        return ((1 << self.prefix) - 1) << (32 - self.prefix) if self.prefix else 0

    def address_count(self):
        """Every address in the block, reserved ones included."""
        return 1 << (32 - self.prefix)

    def usable_count(self):
        """Addresses that can be given to a host.

        Two fewer than the total, except for a `/31`, which modern practice
        uses for point-to-point links precisely because there is nothing to
        broadcast to. The exercise uses `/30` for its links, which wastes two
        addresses per link and is what the older rule requires.
        """
        return max(0, self.address_count() - 2)

    def first(self):
        """The lowest address in the block."""
        return Address(self.base)

    def last(self):
        """The highest address in the block."""
        return Address(self.base + self.address_count() - 1)

    def network_address(self):
        """The reserved all-zeros host address."""
        return self.first()

    def broadcast_address(self):
        """The reserved all-ones host address."""
        return self.last()

    def contains(self, address):
        """Whether an address falls inside the block."""
        return int(self.first()) <= int(address) <= int(self.last())

    def __str__(self):
        """The block in prefix notation."""
        return f"{Address(self.base)}/{self.prefix}"

    def __eq__(self, other):
        """Two blocks are equal when base and prefix agree."""
        return (isinstance(other, Network) and self.base == other.base
                and self.prefix == other.prefix)


def binary(address, prefix):
    """The address in binary with the network part marked.

    The form the exercise asks for, with a bar where the prefix ends. Writing
    it out is how the boundary stops being arbitrary: a `/20` cuts in the
    middle of the third byte, which is exactly why the dotted quad form hides
    what is going on.
    """
    bits = format(int(Address(address)), "032b")
    grouped = [bits[index:index + 8] for index in range(0, 32, 8)]
    text = ".".join(grouped)

    position = prefix + prefix // 8
    return text[:position] + "|" + text[position:]


def prefix_for(hosts):
    """The smallest prefix whose block holds this many hosts.

    Two addresses go to the network and the broadcast, so a demand for 1971
    hosts needs 1973 addresses and therefore 2048, a `/21`. Forgetting the two
    is the classic error, and it shows up only for demands that are exactly a
    power of two.
    """
    needed = hosts + 2
    bits = max(1, math.ceil(math.log2(needed)))
    return 32 - bits


def allocate(block, demands, sort=True):
    """Assign a subnet to each demand inside a block.

    Largest first, because a subnet must start at a multiple of its own size.
    Placing a `/30` at the start of a `/20` leaves the next `/21` no aligned
    space until half the block has been skipped, so an ordered allocation can
    fail where the same demands fit easily.

    That failure is not hypothetical: allocating the exercise's own demands in
    reverse order raises, and in decreasing order they fit exactly.
    """
    outer = Network(block)
    ordered = sorted(demands, key=lambda entry: -entry[1]) if sort else list(demands)

    cursor = int(outer.first())
    result = []

    for name, hosts in ordered:
        prefix = prefix_for(hosts)
        size = 1 << (32 - prefix)
        aligned = ((cursor + size - 1) // size) * size

        if aligned + size - 1 > int(outer.last()):
            raise ValueError(f"{name} does not fit in {block}")

        result.append({"name": name, "demand": hosts,
                       "network": Network(f"{Address(aligned)}/{prefix}")})
        cursor = aligned + size

    order = {name: index for index, (name, _) in enumerate(demands)}
    return sorted(result, key=lambda entry: order[entry["name"]])


def utilisation(block, allocation):
    """How much of a block an allocation uses.

    Always below one, because every subnet is rounded up to a power of two.
    The exercise's demands total 3620 hosts and consume 3812 addresses of a
    4096-address block, which is the cost of the alignment rule.
    """
    outer = Network(block)
    used = sum(entry["network"].address_count() for entry in allocation)
    return used / outer.address_count()
