/**
 * A time interval with a start and an end, ordered by finishing time.
 *
 * <p>Sheet 6, task 6.1a. The ordering is not a detail: interval scheduling is
 * correct precisely because the intervals are processed by increasing end
 * point, so the comparison lives in the data type the algorithm consumes.
 */
public class Interval implements Comparable<Interval> {

    private final int start;
    private final int end;

    public Interval(int start, int end) {
        this.start = start;
        this.end = end;
    }

    public int getStart() {
        return start;
    }

    public int getEnd() {
        return end;
    }

    /**
     * Orders by end point alone.
     *
     * <p>Subtraction would overflow for end points far apart, so the comparison
     * is delegated to Integer.compare, which cannot.
     */
    @Override
    public int compareTo(Interval other) {
        return Integer.compare(end, other.end);
    }

    @Override
    public String toString() {
        return "[" + start + "," + end + "]";
    }
}
