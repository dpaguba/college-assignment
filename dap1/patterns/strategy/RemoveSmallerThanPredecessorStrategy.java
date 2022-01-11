/**
 * Removes values smaller than their predecessor in the original list.
 *
 * <p>The wording of the task decides the result. Comparing against the
 * predecessor as it stood before any removal is not the same as comparing
 * against the last value kept: on 5, 3, 4 the first rule keeps 5 and 4, and
 * the second keeps only 5, because 4 would then be compared with 5 instead of
 * with 3.
 */
public class RemoveSmallerThanPredecessorStrategy implements DoublyLinkedList.Removal<Integer> {

    @Override
    public boolean removes(Integer value, Integer predecessor) {
        return predecessor != null && value < predecessor;
    }
}
