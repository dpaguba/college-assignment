"""The three Cs: why each miss happened.

Every miss falls into one of three categories, and the classification is not a
label but a **measurement against two reference caches**:

- **compulsory**: the block had never been referenced, so no cache of any size
  would have had it
- **capacity**: a fully associative cache of the same size would also have
  missed, so the working set does not fit
- **conflict**: a fully associative cache of the same size would have hit, so
  the miss is caused by the mapping alone

Only the third is an artefact of the organisation, and it is the one
associativity removes. Separating them says which knob is worth turning: more
capacity, a better mapping, or nothing at all.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "replacement-policies"))
import replacement_policies as rp


def classify(addresses, size, block, associativity, policy="lru"):
    """Count the misses of a cache and split them into the three categories."""
    real = rp.Cache(size, block, associativity, policy)
    full = rp.Cache(size, block, max(1, size // block), policy)
    seen = set()

    counts = {"compulsory": 0, "capacity": 0, "conflict": 0, "misses": 0, "hits": 0}

    for address in addresses:
        block_id = address // block
        hit = real.access(address)
        full_hit = full.access(address)

        if hit:
            counts["hits"] += 1
            seen.add(block_id)
            continue

        counts["misses"] += 1
        if block_id not in seen:
            counts["compulsory"] += 1
        elif not full_hit:
            counts["capacity"] += 1
        else:
            counts["conflict"] += 1

        seen.add(block_id)

    return counts


def report(addresses, size, block, associativity):
    """The three Cs as fractions of the accesses."""
    counts = classify(addresses, size, block, associativity)
    total = counts["hits"] + counts["misses"]

    return {name: counts[name] / total if total else 0.0
            for name in ("compulsory", "capacity", "conflict")}


def effect_of_associativity(addresses, size, block, ways):
    """How the three categories move as associativity grows.

    Compulsory misses cannot move, capacity misses barely move, and conflict
    misses fall to zero at full associativity by definition. Seeing all three
    columns at once is what makes clear that associativity is the wrong fix for
    a working set that does not fit.
    """
    return {way: classify(addresses, size, block, way) for way in ways}
