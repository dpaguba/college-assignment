/**
 * Greatest common divisor of two positive integers, by Euclid's algorithm.
 *
 * <p>Sheet 1, task 1.1. Usage: {@code java Euclid a b}.
 *
 * <p>The task restricts the input to natural numbers greater than zero, so zero
 * and negatives take the same branch as unparsable text.
 */
public class Euclid {

    public static void main(String[] args) {
        if (args.length != 2) {
            System.out.println("Falsche Parameteranzahl!");
            usage();
            return;
        }

        int first;
        int second;
        try {
            first = Integer.parseInt(args[0]);
            second = Integer.parseInt(args[1]);
        } catch (NumberFormatException notANumber) {
            System.out.println("Falscher Parameter - Nur Zahlen sind erlaubt!");
            usage();
            return;
        }

        if (first <= 0 || second <= 0) {
            System.out.println("Falscher Parameter - Nur Zahlen sind erlaubt!");
            usage();
            return;
        }

        System.out.println(gcd(first, second));
    }

    /**
     * Euclid's algorithm, recursively.
     *
     * <p>{@code gcd(a, b) = gcd(b, a mod b)} holds because any common divisor of
     * a and b also divides a − qb, and conversely. The recursion terminates
     * because the second argument strictly decreases and stays non-negative.
     *
     * <p>The number of steps is O(log min(a, b)): the worst case is a pair of
     * consecutive Fibonacci numbers, which is Lamé's theorem and the first
     * running-time analysis of an algorithm in history.
     *
     * <p>The arguments need not be ordered. If a &lt; b the first step swaps
     * them, since a mod b = a in that case.
     */
    public static int gcd(int a, int b) {
        return b == 0 ? a : gcd(b, a % b);
    }

    private static void usage() {
        System.out.println("Aufruf mit: java Euclid a b");
        System.out.println("Dabei muessen a und b natuerliche Zahlen groesser 0 sein.");
        System.out.println("Beispiel: java Euclid 24 896");
    }
}
