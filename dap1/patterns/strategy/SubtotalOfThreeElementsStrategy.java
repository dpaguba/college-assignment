/**
 * Inserts the subtotal of three values behind every third element.
 *
 * <p>Values left over at the end of the list enter no subtotal, which the
 * task states and which falls out of the counting: the strategy only inserts
 * when it has seen three.
 */
public class SubtotalOfThreeElementsStrategy
        implements DoublyLinkedList.InsertionStrategy<Integer> {

    private int seen;
    private int group;

    @Override
    public boolean select(Integer reference) {
        seen++;
        group += reference;
        return seen % 3 == 0;
    }

    @Override
    public Integer insert(Integer reference) {
        int subtotal = group;
        group = 0;
        return subtotal;
    }
}
