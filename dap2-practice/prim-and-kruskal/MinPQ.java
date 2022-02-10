import java.util.ArrayList;
import java.util.HashMap;

/**
 * A binary min-heap over nodes keyed by the weight of the cheapest edge reaching them.
 *
 * <p>Sheet 11, provided class, reimplemented. Same structure as the queue used
 * for Dijkstra, with the edge carried along so that Prim can recover the tree
 * and not only its weight.
 */
public class MinPQ {

    private final ArrayList<HeapElement> heap = new ArrayList<>();
    private final HashMap<Integer, Integer> positions = new HashMap<>();

    public boolean isEmpty() {
        return heap.isEmpty();
    }

    public boolean contains(Node node) {
        return positions.containsKey(node.getId());
    }

    /**
     * Adds a node with the edge that reaches it and that edge's weight as the key.
     */
    public void insert(Node node, Edge edge, int weight) {
        heap.add(new HeapElement(node, edge, weight));
        positions.put(node.getId(), heap.size() - 1);
        siftUp(heap.size() - 1);
    }

    /**
     * Removes and returns the entry with the smallest key, or null when empty.
     */
    public HeapElement extractMin() {
        if (heap.isEmpty()) {
            return null;
        }

        HeapElement smallest = heap.get(0);
        HeapElement last = heap.remove(heap.size() - 1);
        positions.remove(smallest.getNode().getId());

        if (!heap.isEmpty()) {
            heap.set(0, last);
            positions.put(last.getNode().getId(), 0);
            siftDown(0);
        }

        return smallest;
    }

    /** The recorded weight for a node still in the queue, or MAX_VALUE. */
    public int getWeight(Node node) {
        Integer index = positions.get(node.getId());
        return index == null ? Integer.MAX_VALUE : heap.get(index).getWeight();
    }

    /** Lowers the key of a node and remembers the edge that achieved it. */
    public void decreaseDistance(Node node, Edge edge, int weight) {
        Integer index = positions.get(node.getId());
        if (index == null || weight >= heap.get(index).getWeight()) {
            return;
        }

        heap.get(index).setWeight(weight);
        heap.get(index).setEdge(edge);
        siftUp(index);
    }

    private void siftUp(int index) {
        while (index > 0) {
            int parent = (index - 1) / 2;
            if (heap.get(parent).getWeight() <= heap.get(index).getWeight()) {
                break;
            }
            swap(parent, index);
            index = parent;
        }
    }

    private void siftDown(int index) {
        int count = heap.size();

        while (true) {
            int smallest = index;
            int left = 2 * index + 1;
            int right = left + 1;

            if (left < count && heap.get(left).getWeight() < heap.get(smallest).getWeight()) {
                smallest = left;
            }
            if (right < count && heap.get(right).getWeight() < heap.get(smallest).getWeight()) {
                smallest = right;
            }
            if (smallest == index) {
                return;
            }

            swap(index, smallest);
            index = smallest;
        }
    }

    private void swap(int first, int second) {
        HeapElement a = heap.get(first);
        HeapElement b = heap.get(second);
        heap.set(first, b);
        heap.set(second, a);
        positions.put(b.getNode().getId(), first);
        positions.put(a.getNode().getId(), second);
    }
}
