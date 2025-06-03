"""Timsort: find the runs that are already sorted, then merge them cleverly.

Runs shorter than the minimum are extended with binary insertion sort. Powers
of two are avoided for that minimum so the final merges stay balanced.
"""

from __future__ import annotations

MIN_MERGE = 32

def compute_minrun(size):
    """Pick a minimum run length so the number of runs is near a power of two."""
    extra = 0
    while size >= MIN_MERGE:
        extra |= size & 1
        size >>= 1
    return size + extra

def timsort(items, key=None):
    """Return a sorted copy of `items`.

    Peter McIlroy's observation, which Tim Peters turned into Python's sort:
    real data is not random. It arrives in stretches that are already ascending
    or already descending. Timsort finds those stretches, reverses the
    descending ones, pads short ones with insertion sort, and then merges them.

    The merges follow a stack invariant that keeps run lengths balanced, so no
    merge ever faces one enormous run and one tiny one. Sorted input costs a
    single pass, which is the case that made it the default in Python, Java,
    Android and Swift.
    """
    result = list(items)
    of = key or (lambda item: item)
    size = len(result)
    if size < 2:
        return result

    def binary_insertion(low, high, start):
        """Sort result[low:high], knowing result[low:start] is already sorted."""
        for position in range(max(start, low + 1), high):
            value = result[position]
            left, right = low, position
            while left < right:
                middle = (left + right) // 2
                if of(value) < of(result[middle]):
                    right = middle
                else:
                    left = middle + 1
            result[left + 1 : position + 1] = result[left:position]
            result[left] = value

    def count_run(low):
        """Length of the run at `low`, reversing it if it descends."""
        if low + 1 >= size:
            return 1
        end = low + 1
        if of(result[end]) < of(result[low]):
            while end + 1 < size and of(result[end + 1]) < of(result[end]):
                end += 1
            result[low : end + 1] = reversed(result[low : end + 1])
        else:
            while end + 1 < size and of(result[end + 1]) >= of(result[end]):
                end += 1
        return end - low + 1

    def merge(low, middle, high):
        """Merge two adjacent runs, copying only the smaller one aside."""
        left = result[low:middle]
        right = result[middle:high]
        i = j = 0
        position = low
        while i < len(left) and j < len(right):
            if of(left[i]) <= of(right[j]):
                result[position] = left[i]
                i += 1
            else:
                result[position] = right[j]
                j += 1
            position += 1
        while i < len(left):
            result[position] = left[i]
            i, position = i + 1, position + 1
        while j < len(right):
            result[position] = right[j]
            j, position = j + 1, position + 1

    minrun = compute_minrun(size)
    stack: list[tuple[int, int]] = []
    low = 0

    while low < size:
        run_length = count_run(low)
        if run_length < minrun:
            forced = min(minrun, size - low)
            binary_insertion(low, low + forced, low + run_length)
            run_length = forced
        stack.append((low, run_length))

        while len(stack) > 1:
            if len(stack) >= 3:
                (_, x), (_, y), (_, z) = stack[-3], stack[-2], stack[-1]
                if x <= y + z:
                    if x < z:
                        (a, la), (b, lb) = stack[-3], stack[-2]
                        merge(a, b, b + lb)
                        stack[-3:-1] = [(a, la + lb)]
                    else:
                        (b, lb), (c, lc) = stack[-2], stack[-1]
                        merge(b, c, c + lc)
                        stack[-2:] = [(b, lb + lc)]
                    continue
            (b, lb), (c, lc) = stack[-2], stack[-1]
            if lb <= lc:
                merge(b, c, c + lc)
                stack[-2:] = [(b, lb + lc)]
                continue
            break

        low += run_length

    while len(stack) > 1:
        (b, lb), (c, lc) = stack[-2], stack[-1]
        merge(b, c, c + lc)
        stack[-2:] = [(b, lb + lc)]

    return result
