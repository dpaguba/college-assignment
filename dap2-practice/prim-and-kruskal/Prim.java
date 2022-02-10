import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;

/**
 * Prim's algorithm for the minimum spanning tree.
 *
 * <p>Sheet 11, task 11.1c. Usage: {@code java Prim < BspGraphKlein.graph}. The
 * start node is the first one in the node list, as the sheet prescribes.
 *
 * <p>The tree is printed from the smaller id to the larger and sorted by weight,
 * so the output does not depend on the order the search happened to visit.
 */
public class Prim {

    public static void main(String[] args) {
        Graph graph;
        try {
            graph = Graph.fromSystemIn();
        } catch (IllegalArgumentException malformed) {
            System.out.println("FEHLER: " + malformed.getMessage());
            System.out.println("Aufruf: java Prim < <filename>");
            return;
        } catch (IOException unreadable) {
            System.out.println("FEHLER: Eingabe konnte nicht gelesen werden.");
            System.out.println("Aufruf: java Prim < <filename>");
            return;
        }

        if (graph.numNodes() == 0) {
            System.out.println("FEHLER: Leere Eingabe.");
            System.out.println("Aufruf: java Prim < <filename>");
            return;
        }

        ArrayList<Edge> tree = run(graph);

        if (tree.size() != graph.numNodes() - 1) {
            System.out.println("Graph nicht zusammenhaengend!");
            return;
        }

        int weight = 0;
        for (Edge edge : tree) {
            weight += edge.getWeight();
        }

        ArrayList<Edge> printable = new ArrayList<>();
        for (Edge edge : tree) {
            printable.add(edge.getSrc().getId() < edge.getDst().getId() ? edge : edge.getSiblingEdge());
        }
        Collections.sort(printable);

        if (printable.size() <= 20) {
            System.out.println(printable);
        }
        System.out.println("Gewicht des minimalen Spannbaums: " + weight);
    }

    /**
     * Grows one tree, always adding the cheapest edge leaving it.
     *
     * <p>Every node starts in the queue with an infinite key. Extracting the
     * minimum adds that node and the edge that reached it to the tree, and then
     * each of its neighbours still in the queue has its key lowered if this new
     * edge is cheaper than whatever reached it before.
     *
     * <p>O((n + m) log n) with a binary heap. A Fibonacci heap brings it to
     * O(m + n log n), which is the classical reason that structure was invented
     * and one of the few places it actually helps.
     *
     * <p>The correctness argument is the cut property again: the cheapest edge
     * leaving the tree crosses the cut between the tree and everything else, so
     * it belongs to some minimum spanning tree.
     *
     * <p>A node that comes out of the queue still carrying an infinite key was never
     * reached, which means the graph is not connected and the tree stays incomplete.
     */
    public static ArrayList<Edge> run(Graph graph) {
        MinPQ queue = new MinPQ();
        ArrayList<Node> nodes = graph.getNodes();

        for (int i = 0; i < nodes.size(); i++) {
            queue.insert(nodes.get(i), null, i == 0 ? 0 : Integer.MAX_VALUE);
        }

        ArrayList<Edge> tree = new ArrayList<>();

        while (!queue.isEmpty()) {
            HeapElement current = queue.extractMin();

            if (current.getWeight() == Integer.MAX_VALUE) {
                break;
            }
            if (current.getEdge() != null) {
                tree.add(current.getEdge());
            }

            for (Edge edge : current.getNode().getAdjList()) {
                Node neighbour = edge.getDst();
                if (queue.contains(neighbour) && edge.getWeight() < queue.getWeight(neighbour)) {
                    queue.decreaseDistance(neighbour, edge, edge.getWeight());
                }
            }
        }

        return tree;
    }
}
