/** A structure that can produce an iterator over its content. */
public interface Iterable<T> {

    /** A fresh iterator, positioned before the first value. */
    Iterator<T> iterator();
}
