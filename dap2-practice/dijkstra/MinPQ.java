import java.util.ArrayList;
import java.util.HashMap;

/**
 * A binary min-heap over nodes keyed by distance, with decrease-key.
 *
 * <p>Sheet 10, task 10.2. Insert and extractMin are O(log n); decreaseDistance
 * is O(log n) as well, and that is the operation the queue exists for.
 *
 * <p>Decrease-key needs to find an element in the middle of the heap, which a
 * plain heap cannot do. The position map from node id to array index is what
 * makes it possible, and keeping that map correct through every swap is the
 * only real work in this class.
 */
public class MinPQ {

    private final ArrayList<HeapElement> heap = new ArrayList<>();
    private final HashMap<Integer, Integer> positions = new HashMap<>();

    public boolean isEmpty() {
        return heap.isEmpty();
    }

    public int size() {
        return heap.size();
    }

    public boolean contains(Node node) {
        return positions.containsKey(node.getId());
    }

    /** Adds a node with a distance, or lowers the distance if it is already in. */
    public void insert(Node node, int distance) {
        Integer existing = positions.get(node.getId());
        if (existing != null) {
            decreaseDistance(node, distance);
            return;
        }

        heap.add(new HeapElement(node, distance));
        positions.put(node.getId(), heap.size() - 1);
        siftUp(heap.size() - 1);
    }

    /** Removes and returns the entry with the smallest distance. */
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

    /**
     * Lowers the recorded distance of a node.
     *
     * <p>Ignores an attempt to raise it, which is what makes the caller in
     * Dijkstra a single unconditional line: relaxing an edge either improves
     * the distance or does nothing.
     */
    public void decreaseDistance(Node node, int distance) {
        Integer index = positions.get(node.getId());
        if (index == null || distance >= heap.get(index).getDistance()) {
            return;
        }

        heap.get(index).setDistance(distance);
        siftUp(index);
    }

    private void siftUp(int index) {
        while (index > 0) {
            int parent = (index - 1) / 2;
            if (heap.get(parent).getDistance() <= heap.get(index).getDistance()) {
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

            if (left < count && heap.get(left).getDistance() < heap.get(smallest).getDistance()) {
                smallest = left;
            }
            if (right < count && heap.get(right).getDistance() < heap.get(smallest).getDistance()) {
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
