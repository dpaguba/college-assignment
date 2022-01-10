import java.util.List;

/**
 * One iterator over several lists in sequence, from the ninth sheet.
 *
 * <p>The awkward part is the empty list: after finishing one list the
 * iterator must skip every empty list that follows before it can answer
 * whether a further value exists. Advancing in {@code hasNext} rather than in
 * {@code next} is what keeps that answer correct.
 */
public class MultiListIterator<T> implements Iterator<T> {

    private final List<DoublyLinkedList<T>> lists;
    private int position;
    private Iterator<T> current;

    /** An iterator over the lists, in the order given. */
    public MultiListIterator(List<DoublyLinkedList<T>> lists) {
        this.lists = lists;
        this.current = lists.isEmpty() ? null : lists.get(0).iterator();
    }

    @Override
    public boolean hasNext() {
        while (current != null && !current.hasNext()) {
            position++;
            current = position < lists.size() ? lists.get(position).iterator() : null;
        }
        return current != null;
    }

    @Override
    public T next() {
        if (!hasNext()) {
            throw new IllegalStateException("no further value");
        }
        return current.next();
    }
}
