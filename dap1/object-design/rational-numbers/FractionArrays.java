/**
 * The array methods of the second practical sheet, written over fractions.
 *
 * <p>The sheet's point is that the loops are the ones already written for
 * integers, with two changes: comparison goes through {@code compareTo} and
 * arithmetic goes through the object's own methods. Everything else about the
 * algorithms is unchanged, which is the argument for defining a type at all.
 */
public class FractionArrays {

    private static final Fraction ZERO = new Fraction(0, 1);
    private static final Fraction ONE = new Fraction(1, 1);
    private static final Fraction TWO = new Fraction(2, 1);

    /** How many entries are negative, returned as a fraction. */
    public static Fraction countNegatives(Fraction[] values) {
        Fraction count = ZERO;
        for (Fraction value : values) {
            if (value.isNegative()) {
                count = count.add(ONE);
            }
        }
        return count;
    }

    /** The sum of the negative entries. */
    public static Fraction sumUpNegatives(Fraction[] values) {
        Fraction sum = ZERO;
        for (Fraction value : values) {
            if (value.isNegative()) {
                sum = sum.add(value);
            }
        }
        return sum;
    }

    /** The largest entry, or null for an empty array. */
    public static Fraction maximum(Fraction[] values) {
        Fraction largest = null;
        for (Fraction value : values) {
            if (largest == null || value.compareTo(largest) > 0) {
                largest = value;
            }
        }
        return largest;
    }

    /** How often the largest entry occurs, returned as a fraction. */
    public static Fraction countMaximum(Fraction[] values) {
        Fraction largest = maximum(values);
        Fraction count = ZERO;
        for (Fraction value : values) {
            if (largest != null && value.compareTo(largest) == 0) {
                count = count.add(ONE);
            }
        }
        return count;
    }

    /** Whether the entries ascend. */
    public static boolean isSorted(Fraction[] values) {
        for (int index = 1; index < values.length; index++) {
            if (values[index - 1].compareTo(values[index]) > 0) {
                return false;
            }
        }
        return true;
    }

    /** Adds the given fraction to every entry, returning the same array. */
    public static Fraction[] increaseArray(Fraction[] values, Fraction increment) {
        for (int index = 0; index < values.length; index++) {
            values[index] = values[index].add(increment);
        }
        return values;
    }

    /**
     * Doubles every entry if at least one is positive.
     *
     * <p>The condition has to be settled before anything is changed, so the
     * array is read once and then written, and a single pass that doubles as
     * it goes would answer a different question.
     */
    public static Fraction[] doubleIfContainsPositive(Fraction[] values) {
        boolean positive = false;
        for (Fraction value : values) {
            if (value.isPositive()) {
                positive = true;
            }
        }
        if (!positive) {
            return values;
        }
        for (int index = 0; index < values.length; index++) {
            values[index] = values[index].mul(TWO);
        }
        return values;
    }

    /** The entries as a comma-separated text. */
    public static String toString(Fraction[] values) {
        StringBuilder text = new StringBuilder();
        for (int index = 0; index < values.length; index++) {
            if (index > 0) {
                text.append(", ");
            }
            text.append(values[index]);
        }
        return text.toString();
    }
}
