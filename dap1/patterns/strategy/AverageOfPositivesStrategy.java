/**
 * The average of the positive values, as a double.
 *
 * <p>The strategy holds two numbers between calls, which is why the pattern
 * uses an object rather than a method: the state of a partial computation has
 * to live somewhere, and here it lives in the strategy rather than in the
 * list or in the loop.
 */
public class AverageOfPositivesStrategy implements DoublyLinkedList.Strategy<Integer> {

    private long sum;
    private int count;

    @Override
    public void handle(Integer value) {
        if (value > 0) {
            sum += value;
            count++;
        }
    }

    /** The average, or zero when no positive value occurred. */
    public double average() {
        return count == 0 ? 0.0 : (double) sum / count;
    }
}
