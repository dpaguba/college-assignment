/**
 * A binary search tree built by insertion, with the three traversals.
 *
 * <p>Sheet 8, task 8.1a. Nodes are objects and an absent child is null, which is
 * the representation the sheet describes.
 *
 * <p>The height is kept as an attribute and updated on the way back out of each
 * insertion, so reading it is O(1) instead of O(n). A leaf has height 1 and an
 * absent subtree has height 0. The sheet's hint says a leaf has height 0, but
 * every expected output on the sheet is one larger than that convention gives,
 * so the outputs win.
 */
public class SearchTree {

    private int value;
    private SearchTree left;
    private SearchTree right;
    private int height;
    private boolean empty = true;

    /** An empty tree. */
    public SearchTree() {
    }

    /** Inserts the values in exactly the order given. */
    public SearchTree(int[] array) {
        for (int element : array) {
            add(element);
        }
    }

    /**
     * Inserts a value at the position the search property dictates.
     *
     * <p>Smaller values go left, larger go right, equal ones are dropped. O(h),
     * and h is O(n) in the worst case: inserting a sorted sequence produces a
     * chain, which is exactly what the second line of the sample file shows and
     * what {@code AVLTree} exists to prevent.
     */
    public void add(int newValue) {
        if (empty) {
            value = newValue;
            empty = false;
            height = 1;
            return;
        }

        if (newValue < value) {
            if (left == null) {
                left = new SearchTree();
            }
            left.add(newValue);
        } else if (newValue > value) {
            if (right == null) {
                right = new SearchTree();
            }
            right.add(newValue);
        }

        height = 1 + Math.max(heightOf(left), heightOf(right));
    }

    /** Height in nodes: 0 for an absent subtree, 1 for a leaf. */
    public int getHeight() {
        return empty ? 0 : height;
    }

    protected static int heightOf(SearchTree tree) {
        return tree == null ? 0 : tree.getHeight();
    }

    /** Left subtree, right subtree, and the value between them: sorted order. */
    public void inOrder() {
        StringBuilder line = new StringBuilder();
        inOrder(line);
        System.out.println(line.toString().trim());
    }

    /** The value first: the order that rebuilds the same tree when replayed. */
    public void preOrder() {
        StringBuilder line = new StringBuilder();
        preOrder(line);
        System.out.println(line.toString().trim());
    }

    /** The value last: children are finished before their parent. */
    public void postOrder() {
        StringBuilder line = new StringBuilder();
        postOrder(line);
        System.out.println(line.toString().trim());
    }

    protected void inOrder(StringBuilder line) {
        if (empty) {
            return;
        }
        if (left != null) {
            left.inOrder(line);
        }
        line.append(value).append(' ');
        if (right != null) {
            right.inOrder(line);
        }
    }

    protected void preOrder(StringBuilder line) {
        if (empty) {
            return;
        }
        line.append(value).append(' ');
        if (left != null) {
            left.preOrder(line);
        }
        if (right != null) {
            right.preOrder(line);
        }
    }

    protected void postOrder(StringBuilder line) {
        if (empty) {
            return;
        }
        if (left != null) {
            left.postOrder(line);
        }
        if (right != null) {
            right.postOrder(line);
        }
        line.append(value).append(' ');
    }
}
