/**
 * One entry of the priority queue: a node and the edge that reaches it.
 *
 * <p>Sheet 11, provided class, reimplemented. The edge is null for the start
 * node and for nodes not yet reached.
 */
public class HeapElement {

    private final Node node;
    private Edge edge;
    private int weight;

    public HeapElement(Node node, Edge edge, int weight) {
        this.node = node;
        this.edge = edge;
        this.weight = weight;
    }

    public Node getNode() {
        return node;
    }

    public Edge getEdge() {
        return edge;
    }

    public void setEdge(Edge edge) {
        this.edge = edge;
    }

    public int getWeight() {
        return weight;
    }

    public void setWeight(int weight) {
        this.weight = weight;
    }
}
