/**
 * Inserts values taken from a second list, one per element, until it runs out.
 *
 * <p>The strategy holds an iterator over the source list, so the list being
 * changed knows nothing about the list being read.
 */
public class InsertFromListStrategy implements DoublyLinkedList.InsertionStrategy<Integer> {

    private final Iterator<Integer> source;

    /** A strategy taking its values from the given list. */
    public InsertFromListStrategy(DoublyLinkedList<Integer> source) {
        this.source = source.iterator();
    }

    @Override
    public boolean select(Integer reference) {
        return source.hasNext();
    }

    @Override
    public Integer insert(Integer reference) {
        return source.next();
    }
}
