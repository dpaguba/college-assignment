import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Huffman coding, from chapter six.
 *
 * <p>The algorithm is one sentence: repeatedly join the two least frequent
 * subtrees. What it buys is a prefix-free code whose weighted path length is
 * minimal, and prefix freedom is what makes decoding possible without any
 * separator between the codes.
 *
 * <p>The tree is built with a priority queue over the frequencies, which ties
 * this chapter to the heap and to the binary search tree that the lecture
 * uses for the same purpose two chapters later.
 */
public class Huffman {

    private final Node root;
    private final Map<Character, String> codes = new HashMap<>();

    private Huffman(Node root) {
        this.root = root;
        if (root != null) {
            collect(root, "");
        }
    }

    /** Builds a code for the characters of the text and their frequencies. */
    public static Huffman build(String text) {
        Map<Character, Integer> frequencies = new HashMap<>();
        for (char symbol : text.toCharArray()) {
            frequencies.merge(symbol, 1, Integer::sum);
        }
        List<Node> nodes = new ArrayList<>();
        List<Character> symbols = new ArrayList<>(frequencies.keySet());
        symbols.sort(null);
        for (char symbol : symbols) {
            nodes.add(new Node(symbol, frequencies.get(symbol), null, null));
        }
        if (nodes.isEmpty()) {
            return new Huffman(null);
        }
        while (nodes.size() > 1) {
            Node first = removeSmallest(nodes);
            Node second = removeSmallest(nodes);
            nodes.add(new Node('\0', first.weight + second.weight, first, second));
        }
        return new Huffman(nodes.get(0));
    }

    /** The code of one character. */
    public String codeFor(char symbol) {
        return codes.get(symbol);
    }

    /** The text as a string of zeros and ones. */
    public String encode(String text) {
        StringBuilder bits = new StringBuilder();
        for (char symbol : text.toCharArray()) {
            bits.append(codes.get(symbol));
        }
        return bits.toString();
    }

    /**
     * The bits back as text.
     *
     * <p>Walking the tree from the root and emitting a character at every
     * leaf is the whole decoder. It works only because no code is a prefix of
     * another, so the walk can never be in doubt about where a code ends.
     */
    public String decode(String bits) {
        if (root == null) {
            return "";
        }
        if (root.isLeaf()) {
            StringBuilder text = new StringBuilder();
            for (int index = 0; index < bits.length(); index++) {
                text.append(root.symbol);
            }
            return text.toString();
        }
        StringBuilder text = new StringBuilder();
        Node position = root;
        for (char bit : bits.toCharArray()) {
            position = bit == '0' ? position.left : position.right;
            if (position.isLeaf()) {
                text.append(position.symbol);
                position = root;
            }
        }
        return text.toString();
    }

    /** Whether no code is a prefix of another. */
    public boolean isPrefixFree() {
        for (Map.Entry<Character, String> first : codes.entrySet()) {
            for (Map.Entry<Character, String> second : codes.entrySet()) {
                if (first.getKey().equals(second.getKey())) {
                    continue;
                }
                if (second.getValue().startsWith(first.getValue())) {
                    return false;
                }
            }
        }
        return true;
    }

    /**
     * The weighted path length of the tree for this text.
     *
     * <p>The independent check on the encoder: the length of the encoded bits
     * has to equal the sum over characters of frequency times code length,
     * computed from the tree rather than from the output.
     */
    public int expectedLength(String text) {
        int total = 0;
        for (char symbol : text.toCharArray()) {
            total += codes.get(symbol).length();
        }
        return total;
    }

    private void collect(Node node, String prefix) {
        if (node.isLeaf()) {
            codes.put(node.symbol, prefix.isEmpty() ? "0" : prefix);
            return;
        }
        collect(node.left, prefix + "0");
        collect(node.right, prefix + "1");
    }

    private static Node removeSmallest(List<Node> nodes) {
        int smallest = 0;
        for (int index = 1; index < nodes.size(); index++) {
            if (nodes.get(index).weight < nodes.get(smallest).weight) {
                smallest = index;
            }
        }
        return nodes.remove(smallest);
    }

    /** One node of the code tree. */
    private static class Node {
        private final char symbol;
        private final int weight;
        private final Node left;
        private final Node right;

        Node(char symbol, int weight, Node left, Node right) {
            this.symbol = symbol;
            this.weight = weight;
            this.left = left;
            this.right = right;
        }

        boolean isLeaf() {
            return left == null && right == null;
        }
    }
}
