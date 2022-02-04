/**
 * One entry of the priority queue: a node and its tentative distance.
 *
 * <p>Sheet 10, task 10.2. The template from the course archive was not in the
 * material that survived, so this is a reimplementation of the interface the
 * sheet describes.
 */
public class HeapElement {

    private final Node node;
    private int distance;

    public HeapElement(Node node, int distance) {
        this.node = node;
        this.distance = distance;
    }

    public Node getNode() {
        return node;
    }

    public int getDistance() {
        return distance;
    }

    public void setDistance(int distance) {
        this.distance = distance;
    }

    @Override
    public String toString() {
        return node.getId() + "@" + distance;
    }
}
