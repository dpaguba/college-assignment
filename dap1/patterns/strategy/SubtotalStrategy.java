/** Inserts the running subtotal behind every element. */
public class SubtotalStrategy implements DoublyLinkedList.InsertionStrategy<Integer> {

    private int total;

    @Override
    public boolean select(Integer reference) {
        total += reference;
        return true;
    }

    @Override
    public Integer insert(Integer reference) {
        return total;
    }
}
