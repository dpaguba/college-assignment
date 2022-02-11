/**
 * Sieve of Eratosthenes: counts the primes in [2, n] and prints them on request.
 *
 * <p>Sheet 1, task 1.2. Usage: {@code java Eratosthenes n [-o]}. The count goes
 * on the first line; with {@code -o} the primes follow on a second line,
 * separated by single spaces.
 *
 * <p>A second parameter other than {@code -o} is ignored rather than rejected,
 * which the sheet spells out explicitly.
 */
public class Eratosthenes {

    public static void main(String[] args) {
        if (args.length < 1 || args.length > 2) {
            System.out.println("Falsche Parameteranzahl!");
            usage();
            return;
        }

        int limit;
        try {
            limit = Integer.parseInt(args[0]);
        } catch (NumberFormatException notANumber) {
            System.out.println("Falscher Parameter! Nur Integer groesser 0 sind erlaubt.");
            usage();
            return;
        }

        if (limit < 1) {
            System.out.println("Falscher Parameter! Nur Integer groesser 0 sind erlaubt.");
            usage();
            return;
        }

        boolean printThem = args.length == 2 && args[1].equals("-o");

        boolean[] isPrime = sieve(limit);

        int count = 0;
        StringBuilder primes = new StringBuilder();
        for (int number = 2; number <= limit; number++) {
            if (isPrime[number]) {
                count++;
                if (primes.length() > 0) {
                    primes.append(' ');
                }
                primes.append(number);
            }
        }

        System.out.println(count);
        if (printThem) {
            System.out.println(primes);
        }
    }

    /**
     * Marks every composite up to the limit.
     *
     * <p>Two details carry the running time. The outer loop stops at the square
     * root, because a composite k has a factor no larger than sqrt(k) and has
     * therefore already been struck out. The inner loop starts at i*i rather
     * than 2*i, because every smaller multiple of i has a smaller prime factor
     * and was struck out earlier.
     *
     * <p>Together they give O(n log log n): each prime p strikes out about n/p
     * numbers, and the sum of 1/p over primes below n grows like log log n.
     *
     * @param limit the largest number to consider, at least 1
     * @return an array where index k is true exactly when k is prime
     */
    public static boolean[] sieve(int limit) {
        boolean[] isPrime = new boolean[limit + 1];
        for (int number = 2; number <= limit; number++) {
            isPrime[number] = true;
        }

        for (int factor = 2; (long) factor * factor <= limit; factor++) {
            if (isPrime[factor]) {
                for (int multiple = factor * factor; multiple <= limit; multiple += factor) {
                    isPrime[multiple] = false;
                }
            }
        }

        return isPrime;
    }

    private static void usage() {
        System.out.println("Aufruf mit : java Eratosthenes n [-o]");
        System.out.println("Es wird die Anzahl der Primzahlen aus dem Bereich [2,n] berechnet.");
        System.out.println("Mit -o werden diese Zahlen auch ausgegeben.");
        System.out.println("Bsp: java Eratosthenes 100 -o");
    }
}
