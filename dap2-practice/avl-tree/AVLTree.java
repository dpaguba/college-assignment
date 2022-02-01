/**
 * A binary search tree that rebalances itself after every insertion.
 *
 * <p>Sheet 8, task 8.2. Same shape as {@code SearchTree} from the previous
 * task, plus the two rotations and the balance check.
 *
 * <p>The invariant: at every node the heights of the two subtrees differ by at
 * most one. It bounds the height by about 1.44 log n, which is what turns the
 * O(h) operations of a search tree into O(log n) ones on every input, including
 * sorted input where a plain search tree degenerates into a list.
 *
 * <p>Heights count nodes here: an absent subtree is 0 and a leaf is 1, matching
 * the expected outputs on the sheet.
 */
public class AVLTree {

    private int value;
    private AVLTree left;
    private AVLTree right;
    private int height;
    private boolean empty = true;

    public AVLTree() {
    }

    public AVLTree(int[] array) {
        for (int element : array) {
            System.out.println("Fuege " + element + " in AVL-Baum ein.");
            add(element);
            assert isBalanced() : "the AVL invariant is broken after inserting " + element;
        }
    }

    public int getHeight() {
        return empty ? 0 : height;
    }

    private static int heightOf(AVLTree tree) {
        return tree == null ? 0 : tree.getHeight();
    }

    /**
     * Inserts a value and restores the balance invariant on the way back up.
     *
     * <p>A single insertion can only unbalance the nodes on the path from the
     * root to the new leaf, and rebalancing the lowest such node restores the
     * whole tree. That is the reason one or two rotations always suffice, and
     * why the operation stays O(log n).
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
                left = new AVLTree();
            }
            left.add(newValue);
        } else if (newValue > value) {
            if (right == null) {
                right = new AVLTree();
            }
            right.add(newValue);
        } else {
            return;
        }

        updateHeight();
        balance();
    }

    /**
     * Repairs this node if its subtrees differ in height by more than one.
     *
     * <p>Four cases, decided by which side is heavy and which side of that
     * child is heavy in turn. Left-left and right-right need one rotation;
     * left-right and right-left need the inner child rotated out of the way
     * first, because a single rotation would only move the problem across.
     */
    private void balance() {
        int leftHeight = heightOf(left);
        int rightHeight = heightOf(right);

        if (leftHeight - rightHeight > 1) {
            System.out.println("Linker Teilbaum von \"" + value + "\" hat Hoehe " + leftHeight
                    + ". Rechter Teilbaum hat Hoehe " + rightHeight + ".");

            if (heightOf(left.left) >= heightOf(left.right)) {
                System.out.println("Fuehre Rechts-Rotation durch");
                rotateRight();
            } else {
                System.out.println("Fuehre Links-Rechts-Rotation durch");
                left.rotateLeft();
                rotateRight();
            }
        } else if (rightHeight - leftHeight > 1) {
            System.out.println("Rechter Teilbaum von \"" + value + "\" hat Hoehe " + rightHeight
                    + ". Linker Teilbaum hat Hoehe " + leftHeight + ".");

            if (heightOf(right.right) >= heightOf(right.left)) {
                System.out.println("Fuehre Links-Rotation durch");
                rotateLeft();
            } else {
                System.out.println("Fuehre Rechts-Links-Rotation durch");
                right.rotateRight();
                rotateLeft();
            }
        }
    }

    /**
     * Rotates the left child up into this position.
     *
     * <p>Nodes are not moved, their contents are: this object stays the parent's
     * child, so no parent pointer has to be updated. The value of the left child
     * is copied here and the old contents are pushed into a new right child.
     */
    private void rotateRight() {
        AVLTree pivot = left;

        AVLTree movedDown = new AVLTree();
        movedDown.value = value;
        movedDown.empty = false;
        movedDown.left = pivot.right;
        movedDown.right = right;
        movedDown.updateHeight();

        value = pivot.value;
        left = pivot.left;
        right = movedDown;
        updateHeight();
    }

    /** Mirror image of {@link #rotateRight()}. */
    private void rotateLeft() {
        AVLTree pivot = right;

        AVLTree movedDown = new AVLTree();
        movedDown.value = value;
        movedDown.empty = false;
        movedDown.right = pivot.left;
        movedDown.left = left;
        movedDown.updateHeight();

        value = pivot.value;
        right = pivot.right;
        left = movedDown;
        updateHeight();
    }

    private void updateHeight() {
        height = 1 + Math.max(heightOf(left), heightOf(right));
    }

    /** Checks the invariant everywhere, used by the assertions. */
    public boolean isBalanced() {
        if (empty) {
            return true;
        }
        if (Math.abs(heightOf(left) - heightOf(right)) > 1) {
            return false;
        }
        return (left == null || left.isBalanced()) && (right == null || right.isBalanced());
    }

    /**
     * Prints the values in ascending order: left subtree, node, right subtree.
     */
    public void inOrder() {
        StringBuilder line = new StringBuilder();
        inOrder(line);
        System.out.println(line.toString().trim());
    }

    /**
     * Prints the node before its subtrees, the order that rebuilds the same tree
     * when replayed as insertions.
     */
    public void preOrder() {
        StringBuilder line = new StringBuilder();
        preOrder(line);
        System.out.println(line.toString().trim());
    }

    /**
     * Prints both subtrees before the node, the order to use when the visit
     * destroys the node.
     */
    public void postOrder() {
        StringBuilder line = new StringBuilder();
        postOrder(line);
        System.out.println(line.toString().trim());
    }

    private void inOrder(StringBuilder line) {
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

    private void preOrder(StringBuilder line) {
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

    private void postOrder(StringBuilder line) {
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
