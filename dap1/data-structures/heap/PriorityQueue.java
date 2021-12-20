/**
 * A binary heap in an array, from chapter nineteen.
 *
 * <p>The tree is implicit: the children of position i are at 2i+1 and 2i+2,
 * so no node object and no link is needed. The heap condition is local, and
 * that is what makes both operations logarithmic: an insertion can only
 * violate it along one path to the root, and an extraction only along one
 * path to a leaf.
 */
public class PriorityQueue {

    private int[] values = new int[8];
    private int count;

    /** How many values the queue holds. */
    public int size() {
        return count;
    }

    /** Whether it holds none. */
    public boolean isEmpty() {
        return count == 0;
    }

    /** Adds a value. */
    public void insert(int value) {
        if (count == values.length) {
            int[] larger = new int[values.length * 2];
            System.arraycopy(values, 0, larger, 0, values.length);
            values = larger;
        }
        values[count] = value;
        siftUp(values, count);
        count++;
    }

    /** The smallest value, left in place. */
    public int minimum() {
        if (count == 0) {
            throw new IllegalStateException("queue empty");
        }
        return values[0];
    }

    /**
     * Removes and returns the smallest value.
     *
     * @throws IllegalStateException if the queue is empty
     */
    public int extractMinimum() {
        if (count == 0) {
            throw new IllegalStateException("queue empty");
        }
        int smallest = values[0];
        count--;
        values[0] = values[count];
        siftDown(values, 0, count);
        return smallest;
    }

    /**
     * Builds a heap from an array in place.
     *
     * <p>Sifting down from the last inner node upwards costs linear time,
     * while inserting the values one at a time costs n log n. The counting
     * methods below show the difference on descending input.
     */
    public static int[] build(int[] values) {
        int[] heap = values.clone();
        for (int index = heap.length / 2 - 1; index >= 0; index--) {
            siftDown(heap, index, heap.length);
        }
        return heap;
    }

    /** Whether the array satisfies the heap condition everywhere. */
    public static boolean isHeap(int[] heap) {
        for (int index = 0; index < heap.length; index++) {
            int left = 2 * index + 1;
            int right = 2 * index + 2;
            if (left < heap.length && heap[left] < heap[index]) {
                return false;
            }
            if (right < heap.length && heap[right] < heap[index]) {
                return false;
            }
        }
        return true;
    }

    /** Sorting by building a heap and draining it. */
    public static int[] heapsort(int[] values) {
        PriorityQueue queue = new PriorityQueue();
        for (int value : values) {
            queue.insert(value);
        }
        int[] sorted = new int[values.length];
        for (int index = 0; index < sorted.length; index++) {
            sorted[index] = queue.extractMinimum();
        }
        return sorted;
    }

    /** How many exchanges building the heap in place performs. */
    public static int buildSwaps(int[] values) {
        int[] heap = values.clone();
        int[] counter = {0};
        for (int index = heap.length / 2 - 1; index >= 0; index--) {
            siftDownCounting(heap, index, heap.length, counter);
        }
        return counter[0];
    }

    /** How many inserting the values one at a time performs. */
    public static int insertSwaps(int[] values) {
        int[] heap = new int[values.length];
        int[] counter = {0};
        int size = 0;
        for (int value : values) {
            heap[size] = value;
            int index = size;
            while (index > 0) {
                int parent = (index - 1) / 2;
                if (heap[index] >= heap[parent]) {
                    break;
                }
                swap(heap, index, parent);
                counter[0]++;
                index = parent;
            }
            size++;
        }
        return counter[0];
    }

    private static void siftUp(int[] heap, int start) {
        int index = start;
        while (index > 0) {
            int parent = (index - 1) / 2;
            if (heap[index] >= heap[parent]) {
                return;
            }
            swap(heap, index, parent);
            index = parent;
        }
    }

    private static void siftDown(int[] heap, int start, int size) {
        int index = start;
        while (true) {
            int left = 2 * index + 1;
            int right = 2 * index + 2;
            int smallest = index;
            if (left < size && heap[left] < heap[smallest]) {
                smallest = left;
            }
            if (right < size && heap[right] < heap[smallest]) {
                smallest = right;
            }
            if (smallest == index) {
                return;
            }
            swap(heap, index, smallest);
            index = smallest;
        }
    }

    private static void siftDownCounting(int[] heap, int start, int size, int[] counter) {
        int index = start;
        while (true) {
            int left = 2 * index + 1;
            int right = 2 * index + 2;
            int smallest = index;
            if (left < size && heap[left] < heap[smallest]) {
                smallest = left;
            }
            if (right < size && heap[right] < heap[smallest]) {
                smallest = right;
            }
            if (smallest == index) {
                return;
            }
            swap(heap, index, smallest);
            counter[0]++;
            index = smallest;
        }
    }

    private static void swap(int[] heap, int first, int second) {
        int held = heap[first];
        heap[first] = heap[second];
        heap[second] = held;
    }
}
