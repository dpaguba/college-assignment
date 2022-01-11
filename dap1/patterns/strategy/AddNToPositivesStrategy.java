/** Raises every positive value by a fixed amount. */
public class AddNToPositivesStrategy implements DoublyLinkedList.Transformation<Integer> {

    private final int increment;

    /** A strategy adding the given amount to positive values. */
    public AddNToPositivesStrategy(int increment) {
        this.increment = increment;
    }

    @Override
    public Integer transform(Integer value) {
        return value > 0 ? value + increment : value;
    }
}
