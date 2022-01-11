/** Removes every value inside a closed interval. */
public class RemoveAllInIntervalStrategy implements DoublyLinkedList.Removal<Integer> {

    private final int bottom;
    private final int top;

    /** A strategy removing values between the bounds, both included. */
    public RemoveAllInIntervalStrategy(int bottom, int top) {
        this.bottom = bottom;
        this.top = top;
    }

    @Override
    public boolean removes(Integer value, Integer predecessor) {
        return value >= bottom && value <= top;
    }
}
