/** Replaces every value by its magnitude. */
public class AllToAbsStrategy implements DoublyLinkedList.Transformation<Integer> {

    @Override
    public Integer transform(Integer value) {
        return Math.abs(value);
    }
}
