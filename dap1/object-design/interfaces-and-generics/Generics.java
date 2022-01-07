/**
 * Bounded type parameters, and what an interface buys.
 *
 * <p>A method that compares its arguments needs to know they can be compared.
 * The bound says so in the signature, so the method body may call
 * {@code compareTo} and any type that implements the interface may be passed,
 * including ones written after this method was.
 */
public class Generics {

    /** The largest of several comparable values. */
    public static <T extends Comparable<T>> T largest(T[] values) {
        T largest = null;
        for (T value : values) {
            if (largest == null || value.compareTo(largest) > 0) {
                largest = value;
            }
        }
        return largest;
    }

    /** How many values the condition accepts. */
    public static <T> int count(T[] values, Test<T> test) {
        int matching = 0;
        for (T value : values) {
            if (test.holds(value)) {
                matching++;
            }
        }
        return matching;
    }

    /** Whether the object satisfies both interfaces at once. */
    public static boolean describesAndCompares(Object candidate) {
        return candidate instanceof Comparable && candidate.toString().length() > 0;
    }

    /** A condition on a value of any type. */
    public interface Test<T> {
        /** Whether the value satisfies the condition. */
        boolean holds(T value);
    }
}
