"""Karatsuba: multiplying two numbers with three smaller products instead of four.

Below the cutoff the recursion costs more than the multiplication saves, so
short operands go straight to the built-in product.
"""

from __future__ import annotations

SMALL = 4

def karatsuba(left, right):
    """Return `left * right`, computed by divide and conquer.

    Schoolbook multiplication of two n-digit numbers costs n² digit products,
    and until 1960 that was believed to be optimal; Kolmogorov had conjectured
    it. Karatsuba, then twenty-three, disproved it in a week.

    Split each number in half: x = a·B + b and y = c·B + d. The product needs
    a·c, b·d and (a·d + b·c), which looks like four multiplications. The trick
    is that

        a·d + b·c = (a + b)·(c + d) - a·c - b·d

    and both a·c and b·d are already computed, so the middle term costs one
    more multiplication rather than two. **Three instead of four**, and the
    recurrence changes from T(n) = 4T(n/2) + O(n), which the Master theorem
    resolves to n², to T(n) = 3T(n/2) + O(n), which gives n^log₂3, about n^1.585.

    Additions grew in number and additions are linear, so the trade is
    favourable and stays favourable. This was the first algorithm to beat n²
    for multiplication, and it opened a line that runs through Toom-Cook and
    Schönhage-Strassen to Harvey and van der Hoeven's O(n log n) in 2019.

    The saving is in the third product: it replaces the two cross terms, which
    is what takes four half-sized multiplications down to three.
    """
    if left < 0 or right < 0:
        return -karatsuba(abs(left), right) if (left < 0) != (right < 0) else karatsuba(abs(left), abs(right))

    if left < 10**SMALL or right < 10**SMALL:
        return left * right

    half = max(len(str(left)), len(str(right))) // 2
    base = 10**half

    high_left, low_left = divmod(left, base)
    high_right, low_right = divmod(right, base)

    upper = karatsuba(high_left, high_right)
    lower = karatsuba(low_left, low_right)
    middle = karatsuba(high_left + low_left, high_right + low_right) - upper - lower

    return upper * base * base + middle * base + lower

def multiplication_counts(left, right):
    """How many recursive products one split makes. Three is the whole point."""
    calls = 0

    def counted(a, b, depth=0):
        """The counting wrapper, which records one call per multiplication."""
        nonlocal calls
        if depth == 1:
            calls += 1
            return a * b
        half = max(len(str(a)), len(str(b))) // 2
        base = 10**half
        high_a, low_a = divmod(a, base)
        high_b, low_b = divmod(b, base)
        upper = counted(high_a, high_b, depth + 1)
        lower = counted(low_a, low_b, depth + 1)
        middle = counted(high_a + low_a, high_b + low_b, depth + 1) - upper - lower
        return upper * base * base + middle * base + lower

    counted(left, right)
    return calls
