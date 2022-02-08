import java.util.ArrayList;

/**
 * A node together with its adjacency list.
 *
 * <p>Sheet 10, task 10.1b. Storing the outgoing edges at the node is what makes
 * this an adjacency list rather than a matrix: memory is O(n + m) instead of
 * O(n²), and iterating over the neighbours of one node costs its degree rather
 * than n. For the sparse graphs these algorithms run on, that is the whole
 * difference.
 */
public class Node {

    private final int id;
    private final ArrayList<Edge> adjList = new ArrayList<>();

    public Node(int id) {
        this.id = id;
    }

    public int getId() {
        return id;
    }

    public ArrayList<Edge> getAdjList() {
        return adjList;
    }

    /**
     * Adds an edge to the destination unless one already goes there.
     *
     * <p>The duplicate check is a linear scan of the adjacency list, so adding
     * all edges of a node costs O(degree²). A hash set of destinations would
     * make it linear; at the sizes on this sheet the list is simpler and the
     * order of the edges stays exactly the order they were read in, which the
     * expected outputs depend on.
     *
     * @return true when the edge was added
     */
    public boolean addEdge(Node dst, int weight) {
        for (Edge edge : adjList) {
            if (edge.getDst().getId() == dst.getId()) {
                return false;
            }
        }
        adjList.add(new Edge(this, dst, weight));
        return true;
    }

    /** True when an edge from this node to the destination exists. */
    public boolean adjacent(Node dst) {
        for (Edge edge : adjList) {
            if (edge.getDst().getId() == dst.getId()) {
                return true;
            }
        }
        return false;
    }

    @Override
    public boolean equals(Object other) {
        return other instanceof Node node && node.id == id;
    }

    @Override
    public int hashCode() {
        return Integer.hashCode(id);
    }

    @Override
    public String toString() {
        return String.valueOf(id);
    }
}
