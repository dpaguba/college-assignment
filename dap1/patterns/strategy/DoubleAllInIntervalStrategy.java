/** Doubles every value inside a closed interval. */
public class DoubleAllInIntervalStrategy implements DoublyLinkedList.Transformation<Integer> {

    private final int bottom;
    private final int top;

    /** A strategy doubling values between the bounds, both included. */
    public DoubleAllInIntervalStrategy(int bottom, int top) {
        this.bottom = bottom;
        this.top = top;
    }

    @Override
    public Integer transform(Integer value) {
        return value >= bottom && value <= top ? value * 2 : value;
    }
}
