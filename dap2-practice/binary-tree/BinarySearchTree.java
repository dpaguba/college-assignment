/**
 * A binary search tree in the style the exercise assumes: an empty tree is an
 * object, not a null reference.
 *
 * <p>Every node holds a value and two children, and a node with no value is an
 * empty tree. That costs two extra objects per leaf and buys the thing the
 * exercise methods depend on: recursion never has to test for null, so
 * {@code leftChild.countNodes(...)} is always a legal call and the base case
 * lives in one place.
 *
 * @param <T> the element type, which has to be ordered
 */
public class BinarySearchTree<T extends Comparable<T>> {

    private T content;
    private BinarySearchTree<T> leftChild;
    private BinarySearchTree<T> rightChild;

    /** Creates an empty tree. */
    public BinarySearchTree() {
    }

    /** True when this node carries no value. */
    public boolean isEmpty() {
        return content == null;
    }

    /**
     * Inserts a value, ignoring duplicates.
     *
     * <p>O(h) for a tree of height h, which is O(log n) when the insertions
     * arrive in a mixed order and O(n) when they arrive sorted. Nothing here
     * rebalances, so sorted input degenerates into a linked list.
     */
    public void insert(T value) {
        if (isEmpty()) {
            content = value;
            leftChild = new BinarySearchTree<>();
            rightChild = new BinarySearchTree<>();
            return;
        }

        int comparison = value.compareTo(content);
        if (comparison < 0) {
            leftChild.insert(value);
        } else if (comparison > 0) {
            rightChild.insert(value);
        }
    }

    /** True when the value is in the tree. O(h). */
    public boolean contains(T value) {
        if (isEmpty()) {
            return false;
        }
        int comparison = value.compareTo(content);
        if (comparison == 0) {
            return true;
        }
        return comparison < 0 ? leftChild.contains(value) : rightChild.contains(value);
    }

    /** Number of values stored. */
    public int size() {
        return isEmpty() ? 0 : 1 + leftChild.size() + rightChild.size();
    }

    /**
     * Exercise 1: counts the nodes whose depth lies between top and bottom.
     *
     * <p>The root sits at depth 0. Descending one level shifts the window by
     * one, so the recursion passes {@code top - 1, bottom - 1} down and the
     * test at each node is simply whether 0 is inside the window.
     *
     * <p>The recursion stops as soon as {@code bottom} goes negative, because
     * every node below is deeper than the window and can contribute nothing.
     * That is what keeps the cost proportional to the part of the tree the
     * window actually touches instead of the whole tree.
     */
    public int countNodes(int top, int bottom) {
        if (isEmpty() || bottom < 0 || top > bottom) {
            return 0;
        }

        int here = top <= 0 ? 1 : 0;
        return here + leftChild.countNodes(top - 1, bottom - 1) + rightChild.countNodes(top - 1, bottom - 1);
    }

    /**
     * Exercise 2: prints the smallest values in ascending order and stops.
     *
     * <p>An in-order walk visits a search tree in sorted order, so the k
     * smallest values are simply the first k nodes it reaches. The return value
     * carries how many are still wanted, which is what lets the recursion stop
     * in the middle of the tree rather than walking all of it and discarding
     * the tail.
     *
     * <p>Cost is O(h + k), not O(n). Printing the three smallest of a million
     * values descends to the leftmost leaf and stops.
     *
     * @param wanted how many values to print
     * @return how many are still wanted after this subtree
     */
    public int sortedUpTo(int wanted) {
        if (wanted <= 0 || isEmpty()) {
            return wanted;
        }

        int remaining = leftChild.sortedUpTo(wanted);
        if (remaining <= 0) {
            return 0;
        }

        System.out.println(content);
        return rightChild.sortedUpTo(remaining - 1);
    }

    public static void main(String[] args) {
        BinarySearchTree<Integer> tree = new BinarySearchTree<>();
        for (int value : new int[] {50, 30, 70, 20, 40, 60, 80, 35, 45}) {
            tree.insert(value);
        }

        System.out.println("size: " + tree.size());
        System.out.println("nodes at depth 0..1: " + tree.countNodes(0, 1));
        System.out.println("nodes at depth 2..3: " + tree.countNodes(2, 3));
        System.out.println("the four smallest:");
        tree.sortedUpTo(4);
    }
}
