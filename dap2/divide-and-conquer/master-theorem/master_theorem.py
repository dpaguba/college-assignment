"""The Master theorem: reading the cost of a divide and conquer recurrence."""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose, log


@dataclass
class Answer:
    """Which case applied, the resulting bound, and why."""

    case: int
    bound: str
    critical_exponent: float
    reason: str


def solve(a, b, k):
    """Solve T(n) = a·T(n/b) + Θ(n^k) and say which case decided it.

    Almost every divide and conquer algorithm has this shape: `a` subproblems
    of size n/b, plus n^k work to split and combine. The theorem says the
    answer depends on one comparison, between k and log_b(a).

    The exponent log_b(a) is the cost of the leaves: how much work the
    recursion produces at the bottom. n^k is the cost of one level of combining.
    Whichever grows faster decides, and when they tie a logarithmic factor
    appears for the log_b(n) levels.

    | | |
    |---|---|
    | k < log_b(a) | the leaves dominate, Θ(n^log_b(a)) |
    | k = log_b(a) | every level costs the same, Θ(n^k log n) |
    | k > log_b(a) | the top level dominates, Θ(n^k) |

    Reading the three cases as "who does the work" rather than as three
    formulas is what makes them memorable, and it explains at a glance why
    Karatsuba and Strassen matter: both reduce `a` while leaving b and k alone,
    which lowers log_b(a) and therefore the whole bound.
    """
    if a < 1:
        raise ValueError("there must be at least one subproblem")
    if b <= 1:
        raise ValueError("the subproblems must be strictly smaller, so b > 1")
    if k < 0:
        raise ValueError("the combine step cannot cost a negative power")

    critical = log(a, b)

    if isclose(k, critical, abs_tol=1e-9):
        power = "" if isclose(k, 0, abs_tol=1e-9) else f"n^{k:g} "
        return Answer(
            case=2,
            bound=f"Theta({power}log n)",
            critical_exponent=critical,
            reason=f"k = log_{b}({a}) = {critical:.4g}, so every level costs the same",
        )

    if k < critical:
        exponent = f"{critical:.4g}".rstrip("0").rstrip(".")
        return Answer(
            case=1,
            bound=f"Theta(n^{exponent})",
            critical_exponent=critical,
            reason=f"k = {k:g} < log_{b}({a}) = {critical:.4g}, so the leaves dominate",
        )

    return Answer(
        case=3,
        bound=f"Theta(n^{k:g})",
        critical_exponent=critical,
        reason=f"k = {k:g} > log_{b}({a}) = {critical:.4g}, so the top level dominates",
    )
