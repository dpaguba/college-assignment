/**
 * A weighted directed edge between two nodes.
 *
 * <p>Sheet 10, task 10.1a. The weight has to be positive, which is what
 * Dijkstra's algorithm needs on the next task and what the file format
 * guarantees.
 */
public class Edge {

    private final Node src;
    private final Node dst;
    private int weight;

    public Edge(Node src, Node dst, int weight) {
        if (weight <= 0) {
            throw new IllegalArgumentException("edge weights must be greater than 0");
        }
        this.src = src;
        this.dst = dst;
        this.weight = weight;
    }

    public int getWeight() {
        return weight;
    }

    public void setWeight(int weight) {
        if (weight <= 0) {
            throw new IllegalArgumentException("edge weights must be greater than 0");
        }
        this.weight = weight;
    }

    public Node getSrc() {
        return src;
    }

    public Node getDst() {
        return dst;
    }

    @Override
    public String toString() {
        return src.getId() + "---" + weight + "---" + dst.getId();
    }
}
