/**
 * An iterator that walks a list from its end.
 *
 * <p>Nothing about the list changes, and no second traversal method is added
 * to it. A different iterator is a different class, which is why the pattern
 * lets a structure be walked in ways it was never written for.
 */
public class ReverseIterator<T> implements Iterator<T> {

    private final Iterator<T> backwards;

    /** An iterator over the list, from the last value to the first. */
    public ReverseIterator(DoublyLinkedList<T> list) {
        this.backwards = list.backwardIterator();
    }

    @Override
    public boolean hasNext() {
        return backwards.hasNext();
    }

    @Override
    public T next() {
        return backwards.next();
    }
}
