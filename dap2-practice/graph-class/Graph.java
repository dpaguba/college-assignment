import java.util.ArrayList;

/**
 * A weighted directed graph as a list of nodes.
 *
 * <p>Sheet 10, task 10.1c.
 */
public class Graph {

    private final ArrayList<Node> nodes = new ArrayList<>();

    /** True when a node with this id exists. */
    public boolean contains(int id) {
        return getNode(id) != null;
    }

    /**
     * Adds a node unless the id is taken.
     *
     * @return true when the node was added
     */
    public boolean addNode(int id) {
        if (contains(id)) {
            return false;
        }
        nodes.add(new Node(id));
        return true;
    }

    /**
     * The node with this id, or null.
     *
     * <p>A linear scan, which makes every lookup O(n) and graph construction
     * O(n·m). A HashMap from id to node would fix that, and the sheet
     * prescribes the ArrayList, so the cost is stated rather than hidden.
     */
    public Node getNode(int id) {
        for (Node node : nodes) {
            if (node.getId() == id) {
                return node;
            }
        }
        return null;
    }

    /**
     * Adds an edge between two existing nodes.
     *
     * @return true when both nodes exist and the edge was added
     */
    public boolean addEdge(int src, int dst, int weight) {
        Node source = getNode(src);
        Node destination = getNode(dst);

        if (source == null || destination == null) {
            return false;
        }

        return source.addEdge(destination, weight);
    }

    public int numNodes() {
        return nodes.size();
    }

    public ArrayList<Node> getNodes() {
        return nodes;
    }

    /** Every edge in the graph, in node order. */
    public ArrayList<Edge> getEdges() {
        ArrayList<Edge> edges = new ArrayList<>();
        for (Node node : nodes) {
            edges.addAll(node.getAdjList());
        }
        return edges;
    }

    @Override
    public String toString() {
        StringBuilder text = new StringBuilder();
        for (Node node : nodes) {
            for (Edge edge : node.getAdjList()) {
                if (text.length() > 0) {
                    text.append(", ");
                }
                text.append(edge);
            }
        }
        return "[" + text + "]";
    }
}
