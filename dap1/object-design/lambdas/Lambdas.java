/**
 * Lambdas and anonymous classes, from chapter fourteen.
 *
 * <p>The lecture introduces both together because they solve the same
 * problem, and the sheet asks for the same method written twice. What the
 * lambda drops is the ceremony; what it keeps is the type, so the two
 * versions are interchangeable at every call site.
 */
public class Lambdas {

    /** How many values satisfy the condition. */
    public static int countMatching(int[] values, Condition condition) {
        int matching = 0;
        for (int value : values) {
            if (condition.holds(value)) {
                matching++;
            }
        }
        return matching;
    }

    /** The conjunction of two conditions, itself a condition. */
    public static Condition and(Condition first, Condition second) {
        return value -> first.holds(value) && second.holds(value);
    }

    /** The negation. */
    public static Condition not(Condition condition) {
        return value -> !condition.holds(value);
    }

    /**
     * How many values exceed a bound given at the call site.
     *
     * <p>The lambda reads {@code bound}, a local of the enclosing method, so
     * the value is captured. Java requires it to be effectively final, which
     * is what keeps the captured value meaningful once the enclosing call has
     * returned.
     */
    public static int countGreaterThan(int[] values, int bound) {
        return countMatching(values, value -> value > bound);
    }

    /** Applies the operation to every value. */
    public static int[] map(int[] values, Transformation transformation) {
        int[] result = new int[values.length];
        for (int index = 0; index < values.length; index++) {
            result[index] = transformation.apply(values[index]);
        }
        return result;
    }

    /** Combines the values into one, starting from the given value. */
    public static int fold(int[] values, int start, Combination combination) {
        int result = start;
        for (int value : values) {
            result = combination.apply(result, value);
        }
        return result;
    }

    /** A transformation of one value. */
    public interface Transformation {
        /** The transformed value. */
        int apply(int value);
    }

    /** A combination of two values. */
    public interface Combination {
        /** The combined value. */
        int apply(int left, int right);
    }
}
