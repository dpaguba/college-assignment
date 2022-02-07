/**
 * Exponential search followed by ternary search.
 *
 * <p>Sheet 3, task 3.2. Usage: {@code java Search x}, where x is how many
 * computation steps are available. The program finds the largest array size
 * that insertion sort can handle in that many steps, given the worst case
 * T(n) = (3n² + 7n − 10)/2 from the lecture.
 *
 * <p>The point is that a value which could be found by rearranging an
 * inequality is found by searching instead. That is the useful half: the search
 * needs nothing but the ability to evaluate T, so it works for functions that
 * cannot be inverted in closed form. It only needs T to be monotone.
 */
public class Search {

    public static void main(String[] args) {
        if (args.length != 1) {
            System.out.println("FEHLER: Es muss genau eine positive ganze Zahl uebergeben werden.");
            return;
        }

        long steps;
        try {
            steps = Long.parseLong(args[0]);
        } catch (NumberFormatException notANumber) {
            System.out.println("FEHLER: Es muss genau eine positive ganze Zahl uebergeben werden.");
            return;
        }

        if (steps <= 0) {
            System.out.println("FEHLER: Es muss genau eine positive ganze Zahl uebergeben werden.");
            return;
        }

        long bound = exponentialSearch(steps);
        long best = ternarySearch(bound / 2, bound, steps);

        System.out.println("Ergebnis: T(" + best + ") = " + cost(best));
    }

    /**
     * Worst case step count of insertion sort on n elements, from the lecture.
     *
     * <p>Long throughout: x may be large enough that n is in the millions, and
     * n² then leaves the int range long before T does anything interesting.
     */
    public static long cost(long n) {
        return (3 * n * n + 7 * n - 10) / 2;
    }

    /**
     * Doubles m until T(m) exceeds the budget.
     *
     * <p>Returns an m with nmax &lt; m ≤ 2·nmax, so the answer is bracketed in
     * O(log nmax) evaluations without knowing any bound in advance. This is the
     * standard way to turn an unbounded search into a bounded one, and it is why
     * exponential search exists at all: binary search needs a right end, and
     * this manufactures one.
     */
    private static long exponentialSearch(long steps) {
        long m = 1;
        while (cost(m) <= steps) {
            m *= 2;
        }
        return m;
    }

    /**
     * Narrows [left, right) to a single value, cutting two thirds each step.
     *
     * <p>Two probes at one third and two thirds decide which third contains the
     * answer. That is log₃ instead of log₂ rounds, but two evaluations per round
     * instead of one, so it is slower than binary search: 2/log₂3 ≈ 1.26 times
     * as many evaluations. Ternary search earns its place on unimodal functions,
     * where a single midpoint tells you nothing; on a monotone one like this it
     * is a demonstration, not an improvement.
     *
     * <p>The invariant is T(left) ≤ x &lt; T(right), which holds when the
     * recursion starts because of the doubling phase and is preserved by every
     * branch.
     */
    private static long ternarySearch(long left, long right, long steps) {
        System.out.println("links: T(" + left + ") = " + cost(left)
                + ", rechts: T(" + right + ") = " + cost(right));

        if (left == right - 1) {
            return left;
        }

        long firstThird = left + (right - left) / 3;
        long secondThird = left + 2 * (right - left) / 3;

        if (cost(firstThird) > steps) {
            return ternarySearch(left, firstThird, steps);
        }
        if (cost(secondThird) > steps) {
            return ternarySearch(firstThird, secondThird, steps);
        }
        return ternarySearch(secondThird, right, steps);
    }
}
