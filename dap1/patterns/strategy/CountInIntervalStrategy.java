/** Counts the values inside a closed interval. */
public class CountInIntervalStrategy implements DoublyLinkedList.Strategy<Integer> {

    private final int bottom;
    private final int top;
    private int count;

    /** A strategy counting values between the bounds, both included. */
    public CountInIntervalStrategy(int bottom, int top) {
        this.bottom = bottom;
        this.top = top;
    }

    @Override
    public void handle(Integer value) {
        if (value >= bottom && value <= top) {
            count++;
        }
    }

    /** How many values fell inside. */
    public int count() {
        return count;
    }
}
