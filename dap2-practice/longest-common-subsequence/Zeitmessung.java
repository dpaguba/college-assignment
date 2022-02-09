import java.util.Locale;
import java.util.Random;

/**
 * Task 7.2, optional: times the table and the reconstruction separately.
 *
 * <p>Usage: {@code java Zeitmessung [repetitions]}. Both strings have the same
 * length, which is doubled from row to row, so the quadratic table and the
 * linear reconstruction separate visibly.
 */
public class Zeitmessung {

    private static final int[] LENGTHS = {500, 1000, 2000, 4000, 8000};

    public static void main(String[] args) {
        int repetitions = args.length > 0 ? Integer.parseInt(args[0]) : 5;
        Random rng = new Random(20260830);

        System.out.printf(Locale.ROOT, "%8s %16s %16s%n", "n", "LCSLaenge (ms)", "LCS (ms)");

        for (int length : LENGTHS) {
            String a = random(length, rng);
            String b = random(length, rng);

            double[] tableTimes = new double[repetitions];
            double[] walkTimes = new double[repetitions];

            for (int run = 0; run < repetitions; run++) {
                long start = System.nanoTime();
                int[][] table = LongestCommonSubsequence.lcsLaenge(a, b);
                long afterTable = System.nanoTime();
                LongestCommonSubsequence.lcs(table, a);
                long afterWalk = System.nanoTime();

                tableTimes[run] = (afterTable - start) / 1e6;
                walkTimes[run] = (afterWalk - afterTable) / 1e6;
            }

            System.out.printf(Locale.ROOT, "%8d %16.2f %16.2f%n", length,
                    median(tableTimes), median(walkTimes));
        }
    }

    private static String random(int length, Random rng) {
        String alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
        StringBuilder text = new StringBuilder(length);
        for (int i = 0; i < length; i++) {
            text.append(alphabet.charAt(rng.nextInt(alphabet.length())));
        }
        return text.toString();
    }

    private static double median(double[] values) {
        double[] copy = values.clone();
        java.util.Arrays.sort(copy);
        return copy[copy.length / 2];
    }
}
