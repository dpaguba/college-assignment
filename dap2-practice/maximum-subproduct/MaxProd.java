import java.math.BigDecimal;

/**
 * Maximum subproduct of a sequence, in linear time.
 *
 * <p>Sheet 6, task 6.2b and 6.2c. The multiplicative twin of Kadane's maximum
 * subarray, and the sign handling is what makes it different.
 *
 * <p>BigDecimal rather than double throughout, because a product of a few
 * hundred decimals loses precision fast and the comparisons that drive the
 * algorithm would then be decided by rounding error. Comparisons go through
 * compareTo, never equals: BigDecimal.equals also compares the scale, so
 * 2.0 and 2.00 are unequal to it.
 */
public class MaxProd {

    /**
     * Best product ending at each position, assuming no negative values.
     *
     * <p>d[0] = a[0], and d[r] = max(a[r], d[r-1] · a[r]): either the range
     * starts here, or it extends the best one ending at the previous position.
     * Nothing else can be optimal, because with non-negative values a longer
     * range never turns a large product into a small one except through a zero,
     * and starting fresh covers that case.
     *
     * <p>Theta(n) multiplications.
     */
    public static BigDecimal[] buildTableUnsigned(BigDecimal[] array) {
        BigDecimal[] table = new BigDecimal[array.length];
        if (array.length == 0) {
            return table;
        }

        table[0] = array[0];
        for (int r = 1; r < array.length; r++) {
            table[r] = array[r].max(table[r - 1].multiply(array[r]));
        }

        return table;
    }

    /**
     * Best product ending at each position, with negative values allowed.
     *
     * <p>The recurrence above breaks as soon as a negative number appears: the
     * worst product ending at r−1 becomes the best one ending at r if a[r] is
     * negative. So a second table is carried, the smallest product ending at
     * each position, and the two swap roles across a sign change.
     *
     * <p>Both are needed at every step, and each is the max or min of the same
     * three candidates: start fresh, extend the best, extend the worst. This is
     * the standard reason a dynamic program keeps more state than the question
     * asks for.
     */
    public static BigDecimal[] buildTableSigned(BigDecimal[] array) {
        BigDecimal[] best = new BigDecimal[array.length];
        BigDecimal[] worst = new BigDecimal[array.length];
        if (array.length == 0) {
            return best;
        }

        best[0] = array[0];
        worst[0] = array[0];

        for (int r = 1; r < array.length; r++) {
            BigDecimal fresh = array[r];
            BigDecimal viaBest = best[r - 1].multiply(array[r]);
            BigDecimal viaWorst = worst[r - 1].multiply(array[r]);

            best[r] = fresh.max(viaBest).max(viaWorst);
            worst[r] = fresh.min(viaBest).min(viaWorst);
        }

        return best;
    }

    /**
     * Turns the table into the actual range that achieves the maximum.
     *
     * <p>The right end is the position of the largest table entry. The left end
     * is found by multiplying leftwards from there until the running product
     * equals that entry, which must happen because the entry was built from
     * exactly that suffix.
     *
     * <p>Works for both tables: nothing here assumes the values are positive.
     */
    public static Range compute(BigDecimal[] array, BigDecimal[] table) {
        if (array.length == 0) {
            return null;
        }

        int right = 0;
        for (int r = 1; r < table.length; r++) {
            if (table[r].compareTo(table[right]) > 0) {
                right = r;
            }
        }

        BigDecimal running = BigDecimal.ONE;
        for (int left = right; left >= 0; left--) {
            running = running.multiply(array[left]);
            if (running.compareTo(table[right]) == 0) {
                return new Range(left, right, table[right]);
            }
        }

        throw new IllegalStateException("the table does not match the array it was built from");
    }
}
