import java.util.ArrayList;
import java.util.List;

/**
 * The binary search tree of chapters seven and twelve, with the exam tasks.
 *
 * <p>The course's representation is the one used here: every subtree is a
 * tree object, and an empty tree is an object whose content is null. That is
 * why the recursive methods never test a child for null and always call the
 * child, which is what the exam tasks assume.
 *
 * <p>The order condition is the whole structure. Everything else, the search,
 * the sorted walk, the minimum, is a consequence, and the depth is the one
 * property insertion order can ruin: the same seven values give depth three
 * or depth seven depending on the order they arrive in.
 */
public class BinarySearchTree<T extends Comparable<T>> {

    private T content;
    private BinarySearchTree<T> leftChild;
    private BinarySearchTree<T> rightChild;

    /** An empty tree. */
    public BinarySearchTree() {
    }

    /** The value at the root, or null when the tree is empty. */
    public T getContent() {
        return content;
    }

    /** Whether the tree holds nothing. */
    public boolean isEmpty() {
        return content == null;
    }

    /** Whether the tree is a single node. */
    public boolean isLeaf() {
        return !isEmpty() && leftChild.isEmpty() && rightChild.isEmpty();
    }

    /** The left subtree, empty rather than null in an empty tree. */
    public BinarySearchTree<T> getLeftChild() {
        return leftChild == null ? new BinarySearchTree<T>() : leftChild;
    }

    /** The right subtree. */
    public BinarySearchTree<T> getRightChild() {
        return rightChild == null ? new BinarySearchTree<T>() : rightChild;
    }

    /** Inserts a value, ignoring one that is already present. */
    public void insert(T value) {
        if (isEmpty()) {
            content = value;
            leftChild = new BinarySearchTree<>();
            rightChild = new BinarySearchTree<>();
            return;
        }
        int order = value.compareTo(content);
        if (order < 0) {
            leftChild.insert(value);
        } else if (order > 0) {
            rightChild.insert(value);
        }
    }

    /** Whether the value is in the tree. */
    public boolean contains(T value) {
        if (isEmpty()) {
            return false;
        }
        int order = value.compareTo(content);
        if (order == 0) {
            return true;
        }
        return order < 0 ? leftChild.contains(value) : rightChild.contains(value);
    }

    /** The values in ascending order. */
    public List<T> inOrder() {
        List<T> values = new ArrayList<>();
        collectInOrder(values);
        return values;
    }

    /** The values level by level. */
    public List<T> breadthFirst() {
        List<T> values = new ArrayList<>();
        List<BinarySearchTree<T>> level = new ArrayList<>();
        if (!isEmpty()) {
            level.add(this);
        }
        while (!level.isEmpty()) {
            List<BinarySearchTree<T>> following = new ArrayList<>();
            for (BinarySearchTree<T> tree : level) {
                values.add(tree.content);
                if (!tree.leftChild.isEmpty()) {
                    following.add(tree.leftChild);
                }
                if (!tree.rightChild.isEmpty()) {
                    following.add(tree.rightChild);
                }
            }
            level = following;
        }
        return values;
    }

    /** How many nodes the tree has. */
    public int countNodes() {
        if (isEmpty()) {
            return 0;
        }
        return 1 + leftChild.countNodes() + rightChild.countNodes();
    }

    /** How many leaves it has. */
    public int countLeaves() {
        if (isEmpty()) {
            return 0;
        }
        if (isLeaf()) {
            return 1;
        }
        return leftChild.countLeaves() + rightChild.countLeaves();
    }

    /** The number of nodes on the longest path from the root. */
    public int depth() {
        if (isEmpty()) {
            return 0;
        }
        return 1 + Math.max(leftChild.depth(), rightChild.depth());
    }

    /** The largest number of nodes on any one level. */
    public int width() {
        int widest = 0;
        List<BinarySearchTree<T>> level = new ArrayList<>();
        if (!isEmpty()) {
            level.add(this);
        }
        while (!level.isEmpty()) {
            widest = Math.max(widest, level.size());
            List<BinarySearchTree<T>> following = new ArrayList<>();
            for (BinarySearchTree<T> tree : level) {
                if (!tree.leftChild.isEmpty()) {
                    following.add(tree.leftChild);
                }
                if (!tree.rightChild.isEmpty()) {
                    following.add(tree.rightChild);
                }
            }
            level = following;
        }
        return widest;
    }

    /** The smallest value. */
    public T minimum() {
        if (isEmpty()) {
            return null;
        }
        return leftChild.isEmpty() ? content : leftChild.minimum();
    }

    /** The largest value. */
    public T maximum() {
        if (isEmpty()) {
            return null;
        }
        return rightChild.isEmpty() ? content : rightChild.maximum();
    }

    /**
     * Removes a value.
     *
     * <p>The case with two children is the one worth knowing: the node keeps
     * its position and takes the smallest value of its right subtree, which
     * is the next value in order and therefore the only one that can stand
     * there without breaking the order condition.
     *
     * @return whether the value was there
     */
    public boolean delete(T value) {
        if (isEmpty()) {
            return false;
        }
        int order = value.compareTo(content);
        if (order < 0) {
            return leftChild.delete(value);
        }
        if (order > 0) {
            return rightChild.delete(value);
        }
        if (leftChild.isEmpty() && rightChild.isEmpty()) {
            content = null;
            leftChild = null;
            rightChild = null;
        } else if (leftChild.isEmpty()) {
            content = rightChild.content;
            leftChild = rightChild.leftChild;
            rightChild = rightChild.rightChild;
        } else if (rightChild.isEmpty()) {
            content = leftChild.content;
            rightChild = leftChild.rightChild;
            leftChild = leftChild.leftChild;
        } else {
            T successor = rightChild.minimum();
            rightChild.delete(successor);
            content = successor;
        }
        return true;
    }

    /**
     * How many nodes lie on the levels from top to bottom, both included.
     *
     * <p>An exam task. The root is on level zero, levels that do not exist
     * are simply skipped, and a top below a bottom gives zero.
     */
    public int countNodes(int top, int bottom) {
        return countNodes(top, bottom, 0);
    }

    /**
     * The largest value on one level, or null when the level is empty.
     *
     * <p>An exam task. The order condition says nothing across a level, so
     * this one has to look at every node on it.
     */
    public T largestOn(int level) {
        List<T> values = valuesOn(level, 0);
        T largest = null;
        for (T value : values) {
            if (largest == null || value.compareTo(largest) > 0) {
                largest = value;
            }
        }
        return largest;
    }

    /**
     * The largest value below the bound, or null.
     *
     * <p>An exam task, and the one where the order condition pays: a value
     * that is at least the bound rules out its whole right subtree.
     */
    public T maxOfLess(T bound) {
        if (isEmpty()) {
            return null;
        }
        if (content.compareTo(bound) >= 0) {
            return leftChild.maxOfLess(bound);
        }
        T fromRight = rightChild.maxOfLess(bound);
        return fromRight == null ? content : fromRight;
    }

    /** The smallest values, in ascending order, at most the given number. */
    public List<T> sortedUpTo(int wanted) {
        List<T> values = new ArrayList<>();
        collectUpTo(wanted, values);
        return values;
    }

    /** The subtree rooted at a value, or null when it is absent. */
    public BinarySearchTree<T> subTree(T value) {
        if (isEmpty()) {
            return null;
        }
        int order = value.compareTo(content);
        if (order == 0) {
            return this;
        }
        return order < 0 ? leftChild.subTree(value) : rightChild.subTree(value);
    }

    /**
     * A balanced tree over sorted values.
     *
     * <p>Taking the middle value as the root and recursing gives the smallest
     * possible depth, which is the contrast the tests use against inserting
     * the same values in ascending order.
     */
    public static <T extends Comparable<T>> BinarySearchTree<T> fromSorted(T[] values) {
        BinarySearchTree<T> tree = new BinarySearchTree<>();
        insertBalanced(tree, values, 0, values.length - 1);
        return tree;
    }

    private static <T extends Comparable<T>> void insertBalanced(BinarySearchTree<T> tree,
            T[] values, int low, int high) {
        if (low > high) {
            return;
        }
        int middle = low + (high - low) / 2;
        tree.insert(values[middle]);
        insertBalanced(tree, values, low, middle - 1);
        insertBalanced(tree, values, middle + 1, high);
    }

    private int countNodes(int top, int bottom, int level) {
        if (isEmpty() || top > bottom || level > bottom) {
            return 0;
        }
        int here = level >= top ? 1 : 0;
        return here + leftChild.countNodes(top, bottom, level + 1)
                + rightChild.countNodes(top, bottom, level + 1);
    }

    private List<T> valuesOn(int wanted, int level) {
        List<T> values = new ArrayList<>();
        if (isEmpty() || level > wanted) {
            return values;
        }
        if (level == wanted) {
            values.add(content);
            return values;
        }
        values.addAll(leftChild.valuesOn(wanted, level + 1));
        values.addAll(rightChild.valuesOn(wanted, level + 1));
        return values;
    }

    private void collectInOrder(List<T> values) {
        if (isEmpty()) {
            return;
        }
        leftChild.collectInOrder(values);
        values.add(content);
        rightChild.collectInOrder(values);
    }

    private void collectUpTo(int wanted, List<T> values) {
        if (isEmpty() || values.size() >= wanted) {
            return;
        }
        leftChild.collectUpTo(wanted, values);
        if (values.size() < wanted) {
            values.add(content);
        }
        rightChild.collectUpTo(wanted, values);
    }
}
