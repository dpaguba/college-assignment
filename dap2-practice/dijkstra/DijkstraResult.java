/**
 * The outcome of a shortest path search: the path as a graph, and its length.
 *
 * <p>Sheet 10, task 10.2.
 */
public class DijkstraResult {

    private final Graph path;
    private final int length;

    public DijkstraResult(Graph path, int length) {
        this.path = path;
        this.length = length;
    }

    public Graph getPath() {
        return path;
    }

    public int getLength() {
        return length;
    }

    /** True when no path exists, in which case the path graph has no nodes. */
    public boolean isEmpty() {
        return path == null || path.numNodes() == 0;
    }
}
