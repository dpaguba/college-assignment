/** Removes every negative value. */
public class RemoveAllNegativesStrategy implements DoublyLinkedList.Removal<Integer> {

    @Override
    public boolean removes(Integer value, Integer predecessor) {
        return value < 0;
    }
}
