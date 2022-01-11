/**
 * Inserts a marker behind a zero that is followed by a one.
 *
 * <p>The strategy sees one value at a time, so a question about neighbours is
 * answered by remembering the previous value and acting one step late. The
 * insertion goes behind the one, which is the element being examined when the
 * pattern becomes visible.
 */
public class OneFollowsZeroStrategy implements DoublyLinkedList.InsertionStrategy<Integer> {

    private Integer previous;

    @Override
    public boolean select(Integer reference) {
        boolean matched = previous != null && previous == 0 && reference == 1;
        previous = reference;
        return matched;
    }

    @Override
    public Integer insert(Integer reference) {
        return 1;
    }
}
