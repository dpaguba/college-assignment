/**
 * An undirected edge, stored as two directed halves that know each other.
 *
 * <p>Sheet 11. The graph classes on this sheet were provided by the course and
 * are not part of the submission; they are reimplemented here from the
 * interface listed on the supplementary sheet, because the archive kept the
 * task descriptions and not the code.
 *
 * <p>An undirected edge appears in the adjacency list of both endpoints. The
 * sibling link keeps the two halves in step, so that changing a weight or
 * marking an edge as used is a single operation rather than a search.
 */
public class Edge implements Comparable<Edge> {

    private final Node src;
    private final Node dst;
    private int weight;
    private Edge sibling;

    public Edge(Node source, Node destination, int weight) {
        this.src = source;
        this.dst = destination;
        this.weight = weight;
    }

    public int getWeight() {
        return weight;
    }

    public void setWeight(int weight) {
        this.weight = weight;
        if (sibling != null && sibling.weight != weight) {
            sibling.setWeight(weight);
        }
    }

    public Node getSrc() {
        return src;
    }

    public Node getDst() {
        return dst;
    }

    public Edge getSiblingEdge() {
        return sibling;
    }

    void setSiblingEdge(Edge sibling) {
        this.sibling = sibling;
    }

    @Override
    public int compareTo(Edge other) {
        if (weight != other.weight) {
            return Integer.compare(weight, other.weight);
        }
        if (src.getId() != other.src.getId()) {
            return Integer.compare(src.getId(), other.src.getId());
        }
        return Integer.compare(dst.getId(), other.dst.getId());
    }

    /**
     * The id of the far end, for printing an adjacency list without repeating the
     * source on every entry.
     */
    public String toStringTarget() {
        return String.valueOf(dst.getId());
    }

    @Override
    public String toString() {
        return src.getId() + "---" + weight + "---" + dst.getId();
    }
}
