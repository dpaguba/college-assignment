import java.util.ArrayList;
import java.util.HashMap;

/**
 * Disjoint sets as a list of lists, with a map from node to its list.
 *
 * <p>Sheet 11, task 11.1a. The representative of a set is the first node in its
 * list.
 *
 * <p>The map is what makes {@code find} O(1) instead of a search through every
 * list. {@code union} is O(size of the smaller list) if the smaller one is the
 * one copied over, which is the union-by-size rule and bounds the total cost of
 * m unions by O(m log m): a node's list can only double in size each time it is
 * moved, so it moves at most log n times.
 *
 * <p>The classic union-find with parent pointers, union by rank and path
 * compression is faster still, at inverse Ackermann per operation, which is
 * effectively constant. The sheet prescribes the list version, and it is easier
 * to see what a set actually is.
 */
public class UnionFind {

    private final ArrayList<ArrayList<Node>> sets = new ArrayList<>();
    private final HashMap<Node, ArrayList<Node>> setOf = new HashMap<>();

    public UnionFind(ArrayList<Node> nodes) {
        for (Node node : nodes) {
            makeSet(node);
        }
    }

    /** Creates a set holding only this node. */
    public void makeSet(Node x) {
        ArrayList<Node> set = new ArrayList<>();
        set.add(x);
        sets.add(set);
        setOf.put(x, set);
    }

    /** The representative of the set containing x, in constant time. */
    public Node find(Node x) {
        ArrayList<Node> set = setOf.get(x);
        return set == null ? null : set.get(0);
    }

    /**
     * Merges the two sets, appending the smaller list to the larger one.
     *
     * <p>Which list survives matters: appending the larger to the smaller would
     * mean updating more map entries and would lose the logarithmic bound.
     */
    public void union(Node x, Node y) {
        ArrayList<Node> first = setOf.get(x);
        ArrayList<Node> second = setOf.get(y);

        if (first == null || second == null || first == second) {
            return;
        }

        ArrayList<Node> larger = first.size() >= second.size() ? first : second;
        ArrayList<Node> smaller = larger == first ? second : first;

        for (Node node : smaller) {
            larger.add(node);
            setOf.put(node, larger);
        }

        sets.remove(smaller);
    }

    public HashMap<Node, ArrayList<Node>> getHashMap() {
        return setOf;
    }

    /** How many disjoint sets are left, which is the number of components. */
    public int getSetCount() {
        return sets.size();
    }
}
