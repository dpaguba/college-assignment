/** Counts how often one value occurs, from the first task of the tenth sheet. */
public class CountXStrategy implements DoublyLinkedList.Strategy<Integer> {

    private final int wanted;
    private int count;

    /** A strategy counting occurrences of the given value. */
    public CountXStrategy(int wanted) {
        this.wanted = wanted;
    }

    @Override
    public void handle(Integer value) {
        if (value == wanted) {
            count++;
        }
    }

    /** How many occurrences were seen. */
    public int count() {
        return count;
    }
}
