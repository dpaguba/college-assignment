/**
 * The iterator interface as the lecture defines it.
 *
 * <p>Two methods and no more: whether something remains, and the next value.
 * A structure that offers this hides how it stores anything, so the code that
 * walks it works for a list, a tree, or several lists in a row.
 */
public interface Iterator<T> {

    /** Whether a further value is available. */
    boolean hasNext();

    /** The next value, advancing the iterator. */
    T next();
}
