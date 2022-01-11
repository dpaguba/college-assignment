/**
 * Removes every value inside an interval and counts how many went.
 *
 * <p>The same decision as the previous strategy with one field added, which
 * is the argument for the pattern: two questions that share a traversal do
 * not need two traversals, and neither needs a change to the list.
 */
public class RemoveAndCountAllInIntervalStrategy implements DoublyLinkedList.Removal<Integer> {

    private final int bottom;
    private final int top;
    private int removed;

    /** A strategy removing and counting values between the bounds. */
    public RemoveAndCountAllInIntervalStrategy(int bottom, int top) {
        this.bottom = bottom;
        this.top = top;
    }

    @Override
    public boolean removes(Integer value, Integer predecessor) {
        boolean inside = value >= bottom && value <= top;
        if (inside) {
            removed++;
        }
        return inside;
    }

    /** How many values were removed. */
    public int removed() {
        return removed;
    }
}
