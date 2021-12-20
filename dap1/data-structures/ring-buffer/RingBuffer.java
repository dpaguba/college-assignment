/**
 * The ring buffer of the seventh sheet.
 *
 * <p>A fixed array with two positions running around it. The awkward part is
 * that a read position equal to a write position means either full or empty,
 * and the two states are opposite. Storing the count settles it; the
 * alternative, leaving one slot unused, buys nothing here.
 */
public class RingBuffer {

    private final int[] values;
    private int readPosition;
    private int writePosition;
    private int count;

    /** A buffer holding at most the given number of values. */
    public RingBuffer(int capacity) {
        if (capacity <= 0) {
            throw new IllegalArgumentException("capacity must be positive");
        }
        this.values = new int[capacity];
    }

    /** How many values are stored. */
    public int size() {
        return count;
    }

    /** Whether none are. */
    public boolean isEmpty() {
        return count == 0;
    }

    /** Whether no further value fits. */
    public boolean isFull() {
        return count == values.length;
    }

    /**
     * Writes a value.
     *
     * @throws IllegalStateException if the buffer is full
     */
    public void put(int value) {
        if (isFull()) {
            throw new IllegalStateException("buffer full");
        }
        values[writePosition] = value;
        writePosition = (writePosition + 1) % values.length;
        count++;
    }

    /**
     * Reads the oldest value.
     *
     * @throws IllegalStateException if the buffer is empty
     */
    public int get() {
        if (isEmpty()) {
            throw new IllegalStateException("buffer empty");
        }
        int value = values[readPosition];
        readPosition = (readPosition + 1) % values.length;
        count--;
        return value;
    }
}
