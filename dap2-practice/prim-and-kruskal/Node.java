import java.util.ArrayList;

/** A node with its adjacency list. Sheet 11, provided class, reimplemented. */
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
     * True when an edge from this node to the destination exists. Linear in the
     * degree, since the adjacency list is scanned.
     */
    public boolean adjacent(Node dest) {
        return getAdjacentEdge(dest) != null;
    }

    public Edge getAdjacentEdge(Node dest) {
        for (Edge edge : adjList) {
            if (edge.getDst().getId() == dest.getId()) {
                return edge;
            }
        }
        return null;
    }

    public void addEdge(Edge e) {
        adjList.add(e);
    }

    /** Adds a directed half-edge unless one to that destination already exists. */
    public boolean addEdge(Node destination, int weight) {
        if (adjacent(destination)) {
            return false;
        }
        adjList.add(new Edge(this, destination, weight));
        return true;
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
