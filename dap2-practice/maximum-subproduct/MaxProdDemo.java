import java.math.BigDecimal;
import java.util.Random;

/**
 * Checks {@link MaxProd} against brute force over every range.
 *
 * <p>Not part of the submission; the sheet asks for the two classes without a
 * main method.
 */
public class MaxProdDemo {

    public static void main(String[] args) {
        BigDecimal[] example = of("0.5", "3", "2.5", "0.1", "4", "2");
        Range unsigned = MaxProd.compute(example, MaxProd.buildTableUnsigned(example));
        System.out.println("unsigned: " + unsigned);

        BigDecimal[] withNegatives = of("2", "-3", "-4", "0.5", "-2", "6");
        Range signed = MaxProd.compute(withNegatives, MaxProd.buildTableSigned(withNegatives));
        System.out.println("signed:   " + signed);

        Random rng = new Random(20260830);
        int checked = 0;

        for (int trial = 0; trial < 4000; trial++) {
            int length = 1 + rng.nextInt(9);
            BigDecimal[] values = new BigDecimal[length];
            boolean allowNegative = trial % 2 == 0;
            for (int i = 0; i < length; i++) {
                int raw = rng.nextInt(allowNegative ? 21 : 11) - (allowNegative ? 10 : 0);
                values[i] = new BigDecimal(raw).divide(new BigDecimal(2));
            }

            BigDecimal expected = bruteForce(values);

            BigDecimal signedResult = MaxProd.compute(values, MaxProd.buildTableSigned(values)).getProd();
            if (signedResult.compareTo(expected) != 0) {
                throw new AssertionError("signed " + signedResult + " vs " + expected);
            }

            if (!allowNegative) {
                BigDecimal unsignedResult =
                        MaxProd.compute(values, MaxProd.buildTableUnsigned(values)).getProd();
                if (unsignedResult.compareTo(expected) != 0) {
                    throw new AssertionError("unsigned " + unsignedResult + " vs " + expected);
                }
            }

            checked++;
        }

        System.out.println(checked + " zufaellige Instanzen gegen Brute Force geprueft.");
    }

    /** Every range, multiplied out. */
    private static BigDecimal bruteForce(BigDecimal[] values) {
        BigDecimal best = null;
        for (int left = 0; left < values.length; left++) {
            BigDecimal product = BigDecimal.ONE;
            for (int right = left; right < values.length; right++) {
                product = product.multiply(values[right]);
                if (best == null || product.compareTo(best) > 0) {
                    best = product;
                }
            }
        }
        return best;
    }

    private static BigDecimal[] of(String... values) {
        BigDecimal[] result = new BigDecimal[values.length];
        for (int i = 0; i < values.length; i++) {
            result[i] = new BigDecimal(values[i]);
        }
        return result;
    }
}
