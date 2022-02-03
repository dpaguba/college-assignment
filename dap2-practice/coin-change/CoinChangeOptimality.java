import java.util.Arrays;

/**
 * Answers the question the sheet ends with: is the greedy rule always optimal?
 *
 * <p>Not part of the submission, and deliberately a separate class so that
 * {@code CoinChange} keeps the output format the sheet prescribes. Usage:
 * {@code java CoinChangeOptimality [limit]}.
 */
public class CoinChangeOptimality {

    private static final int[] EURO = {200, 100, 50, 20, 10, 5, 2, 1};
    private static final int[] MIRA = {200, 100, 50, 20, 10, 9, 7, 5, 2, 1};

    public static void main(String[] args) {
        int limit = args.length > 0 ? Integer.parseInt(args[0]) : 5000;

        report("Euro", EURO, limit);
        report("Mira", MIRA, limit);
    }

    private static void report(String name, int[] coins, int limit) {
        int mismatches = 0;
        int firstMismatch = -1;

        for (int amount = 0; amount <= limit; amount++) {
            int greedy = count(CoinChange.change(amount, coins));
            int best = optimal(amount, coins);
            if (greedy != best) {
                mismatches++;
                if (firstMismatch < 0) {
                    firstMismatch = amount;
                }
            }
        }

        System.out.println(name + ": " + mismatches + " amount(s) out of " + (limit + 1)
                + " where greedy is not optimal"
                + (firstMismatch < 0 ? "" : ", smallest is " + firstMismatch
                        + " (greedy " + count(CoinChange.change(firstMismatch, coins))
                        + " coins, optimum " + optimal(firstMismatch, coins) + ")"));
    }

    /**
     * The fewest coins possible, by dynamic programming.
     *
     * <p>best[k] = 1 + min over coins c of best[k − c], filled upwards from
     * best[0] = 0. O(amount × denominations), which is pseudo-polynomial: the
     * amount needs only its logarithm in digits to write down, so the table is
     * exponential in the length of the input.
     */
    public static int optimal(int amount, int[] coins) {
        int[] best = new int[amount + 1];
        Arrays.fill(best, Integer.MAX_VALUE);
        best[0] = 0;

        for (int value = 1; value <= amount; value++) {
            for (int coin : coins) {
                if (coin <= value && best[value - coin] != Integer.MAX_VALUE) {
                    best[value] = Math.min(best[value], best[value - coin] + 1);
                }
            }
        }

        return best[amount] == Integer.MAX_VALUE ? -1 : best[amount];
    }

    private static int count(int[] counts) {
        int total = 0;
        for (int value : counts) {
            total += value;
        }
        return total;
    }
}
