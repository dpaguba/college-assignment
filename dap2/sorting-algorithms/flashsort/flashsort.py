"""Flashsort: estimate where every element belongs, then permute it there.

The number of classes is a fraction of n. Neubert's papers use 0.42 to 0.45;
fewer classes mean longer insertion runs at the end.
"""

from __future__ import annotations

CLASS_RATIO = 0.42

def flashsort(items, key=None):
    """Return a sorted copy of `items`, whose keys must be numbers.

    A linear map from the key range onto m buckets predicts each element's
    class. Counting the classes gives their boundaries, elements are permuted
    into their class in a single pass with O(1) extra memory, and a short
    insertion sort finishes the nearly ordered result.

    It is bucket sort that refuses to allocate the buckets, which is where the
    speed comes from and also the fragility: keys that are not close to
    uniform pile into one class and the final insertion sort turns quadratic.
    """
    result = list(items)
    of = key or (lambda item: item)
    size = len(result)
    if size < 2:
        return result

    keys = [of(value) for value in result]
    low, high = min(keys), max(keys)
    if low == high:
        return result

    classes = max(1, int(CLASS_RATIO * size))
    span = classes - 1

    def class_of(k):
        """The class a key falls into, by linear interpolation."""
        return int(span * (k - low) / (high - low))

    counts = [0] * classes
    for k in keys:
        counts[class_of(k)] += 1
    for index in range(1, classes):
        counts[index] += counts[index - 1]

    moved = 0
    position = 0
    current_class = classes - 1
    while moved < size:
        while position >= counts[current_class]:
            position += 1
            current_class = class_of(of(result[position]))
        held = result[position]
        while position < counts[current_class]:
            current_class = class_of(of(held))
            counts[current_class] -= 1
            result[counts[current_class]], held = held, result[counts[current_class]]
            moved += 1

    for index in range(1, size):
        value = result[index]
        back = index - 1
        while back >= 0 and of(result[back]) > of(value):
            result[back + 1] = result[back]
            back -= 1
        result[back + 1] = value

    return result
