"""DNS: a distributed database resolved by walking a tree.

No single server holds the mapping, and no single server could. The name space
is a tree, each zone is served by its own machines, and a resolution walks down
it: root, then top level domain, then the domain's own servers.

**Iterative** resolution asks each server for the next referral and follows it,
so the client does the walking. **Recursive** resolution asks one server to do
the walk, which is what a machine's configured resolver does for it.

Caching is what makes any of this affordable: the root servers would otherwise
see every lookup on the internet.
"""

from __future__ import annotations


class Hierarchy:
    """A name tree with records at the leaves and a cache in front."""

    def __init__(self, delegations, records, ttl=3600):
        """Store the delegation tree, the records and the cache lifetime."""
        self.delegations = dict(delegations)
        self.records = dict(records)
        self.ttl = ttl
        self.cache = {}
        self.now = 0

    def advance(self, seconds):
        """Move the clock forward, which is how cache entries expire."""
        self.now += seconds

    def resolve(self, name, mode="iterative"):
        """Look a name up, reporting how many queries it cost."""
        cached = self.cache.get(name)
        if cached and cached["expires"] > self.now:
            return {"address": cached["address"], "queries": 0, "cached": True}

        if name not in self.records:
            return {"address": None, "queries": 1, "cached": False}

        if mode == "recursive":
            queries = 1
        else:
            queries = self._depth(name) + 1

        self.cache[name] = {"address": self.records[name],
                            "expires": self.now + self.ttl}
        return {"address": self.records[name], "queries": queries, "cached": False}

    def _depth(self, name):
        """How many referrals an iterative walk needs to reach a name."""
        depth = 0
        zone = ""

        while True:
            children = self.delegations.get(zone, [])
            following = next((child for child in children
                              if name == child or name.endswith("." + child)), None)
            if following is None:
                return depth
            zone = following
            depth += 1


def cache_hit_rate(lookups, distinct):
    """What fraction of lookups a cache answers.

    High, because name popularity is heavily skewed: a handful of names account
    for most traffic. That skew is the reason a small cache with a short
    lifetime removes most of the load.
    """
    return 1 - distinct / lookups if lookups else 0.0


def record_types():
    """The record types the course uses and what each answers."""
    return {
        "A": "name to IPv4 address",
        "AAAA": "name to IPv6 address",
        "NS": "zone to the servers authoritative for it",
        "MX": "domain to its mail servers",
        "CNAME": "name to another name",
    }


def why_udp(size):
    """Why DNS uses UDP for small answers and TCP for large ones.

    A query and its answer usually fit in one datagram, so a TCP handshake
    would triple the cost of the exchange. Above the datagram limit the server
    sets a truncation flag and the client retries over TCP, which is also how
    zone transfers work.
    """
    return "udp" if size <= 512 else "tcp"
