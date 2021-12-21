/**
 * Array and matrix exercises from the second sheet, plus the sieve.
 *
 * <p>The tasks here are the first place the course asks for a loop whose end
 * condition is part of the problem rather than the length of the array: the
 * pair count consumes two elements at a time, and prime factorisation stops
 * when the remaining value has been reduced to one.
 */
public class ArraysAndMatrices {

    /**
     * The largest divisor of the value below the value itself.
     *
     * <p>Searching downwards from the value finds it immediately for even
     * numbers and runs to one for primes. Searching upwards from two for the
     * smallest divisor and dividing is the same answer with far fewer steps,
     * which is the version implemented here.
     */
    public static int largestProperDivisor(int value) {
        for (int candidate = 2; (long) candidate * candidate <= value; candidate++) {
            if (value % candidate == 0) {
                return value / candidate;
            }
        }
        return 1;
    }

    /** The prime factors of the value, ascending, with repetitions. */
    public static int[] primeFactors(int value) {
        int[] found = new int[32];
        int count = 0;
        int rest = value;
        for (int candidate = 2; (long) candidate * candidate <= rest; candidate++) {
            while (rest % candidate == 0) {
                found[count++] = candidate;
                rest /= candidate;
            }
        }
        if (rest > 1) {
            found[count++] = rest;
        }
        int[] result = new int[count];
        System.arraycopy(found, 0, result, 0, count);
        return result;
    }

    /**
     * How many pairs of equal neighbours the array contains.
     *
     * <p>Each element belongs to at most one pair, so a match advances the
     * index by two. The published examples are the test: four equal values in
     * a row give two pairs, not three.
     */
    public static int countPairs(int[] values) {
        int pairs = 0;
        int index = 0;
        while (index < values.length - 1) {
            if (values[index] == values[index + 1]) {
                pairs++;
                index += 2;
            } else {
                index++;
            }
        }
        return pairs;
    }

    /** The sieve of Eratosthenes up to and including the limit. */
    public static boolean[] sieve(int limit) {
        boolean[] prime = new boolean[limit + 1];
        for (int index = 2; index <= limit; index++) {
            prime[index] = true;
        }
        for (int candidate = 2; (long) candidate * candidate <= limit; candidate++) {
            if (prime[candidate]) {
                for (int multiple = candidate * candidate; multiple <= limit;
                        multiple += candidate) {
                    prime[multiple] = false;
                }
            }
        }
        return prime;
    }

    /** The sum of each row. */
    public static int[] rowSums(int[][] matrix) {
        int[] sums = new int[matrix.length];
        for (int row = 0; row < matrix.length; row++) {
            for (int column = 0; column < matrix[row].length; column++) {
                sums[row] += matrix[row][column];
            }
        }
        return sums;
    }

    /** The sum of each column. */
    public static int[] columnSums(int[][] matrix) {
        int columns = matrix.length == 0 ? 0 : matrix[0].length;
        int[] sums = new int[columns];
        for (int[] row : matrix) {
            for (int column = 0; column < row.length; column++) {
                sums[column] += row[column];
            }
        }
        return sums;
    }

    /** The matrix with rows and columns exchanged. */
    public static int[][] transpose(int[][] matrix) {
        int rows = matrix.length;
        int columns = rows == 0 ? 0 : matrix[0].length;
        int[][] result = new int[columns][rows];
        for (int row = 0; row < rows; row++) {
            for (int column = 0; column < columns; column++) {
                result[column][row] = matrix[row][column];
            }
        }
        return result;
    }

    /** Whether the matrix equals its own transpose. */
    public static boolean isSymmetric(int[][] matrix) {
        for (int row = 0; row < matrix.length; row++) {
            if (matrix[row].length != matrix.length) {
                return false;
            }
            for (int column = 0; column < matrix[row].length; column++) {
                if (matrix[row][column] != matrix[column][row]) {
                    return false;
                }
            }
        }
        return true;
    }
}
