/**
 * A stack over any element type, from chapter twelve.
 *
 * <p>Before generics this class was written over {@code Object} and every
 * read needed a cast that the compiler could not check. The type parameter
 * moves that check to compile time, and the array inside shows the price:
 * a generic array cannot be created directly, so one of {@code Object} is
 * made and cast once, in a single place that can be reasoned about.
 */
public class GenericStack<T> {

    private Object[] values = new Object[8];
    private int count;

    /** Puts a value on top. */
    public void push(T value) {
        if (count == values.length) {
            Object[] larger = new Object[values.length * 2];
            System.arraycopy(values, 0, larger, 0, values.length);
            values = larger;
        }
        values[count++] = value;
    }

    /**
     * Takes the top value off.
     *
     * @throws IllegalStateException if the stack is empty
     */
    @SuppressWarnings("unchecked")
    public T pop() {
        if (count == 0) {
            throw new IllegalStateException("stack empty");
        }
        T value = (T) values[--count];
        values[count] = null;
        return value;
    }

    /** The top value, left in place. */
    @SuppressWarnings("unchecked")
    public T top() {
        if (count == 0) {
            throw new IllegalStateException("stack empty");
        }
        return (T) values[count - 1];
    }

    /** Whether the stack holds nothing. */
    public boolean isEmpty() {
        return count == 0;
    }

    /** How many values it holds. */
    public int size() {
        return count;
    }
}
