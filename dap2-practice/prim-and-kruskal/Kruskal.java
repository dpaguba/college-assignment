import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;

/**
 * Kruskal's algorithm for the minimum spanning tree.
 *
 * <p>Sheet 11, task 11.1b. Usage: {@code java Kruskal < BspGraphKlein.graph}.
 */
public class Kruskal {

    public static void main(String[] args) {
        Graph graph;
        try {
            graph = Graph.fromSystemIn();
        } catch (IllegalArgumentException malformed) {
            System.out.println("FEHLER: " + malformed.getMessage());
            System.out.println("Aufruf: java Kruskal < <filename>");
            return;
        } catch (IOException unreadable) {
            System.out.println("FEHLER: Eingabe konnte nicht gelesen werden.");
            System.out.println("Aufruf: java Kruskal < <filename>");
            return;
        }

        if (graph.numNodes() == 0) {
            System.out.println("FEHLER: Leere Eingabe.");
            System.out.println("Aufruf: java Kruskal < <filename>");
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

        if (tree.size() <= 20) {
            System.out.println(tree);
        }
        System.out.println("Gewicht des minimalen Spannbaums: " + weight);
    }

    /**
     * Sorts the edges and takes every one that joins two different components.
     *
     * <p>O(m log m) for the sort, which dominates: the union-find operations are
     * almost constant. Prim's algorithm does the same job in O(m log n) and the
     * difference between the two is which structure they grow. Kruskal grows a
     * forest that only becomes connected at the end; Prim grows one tree from
     * the start.
     *
     * <p>Both are correct for the same reason, the cut property: for any way of
     * splitting the nodes into two groups, the lightest edge crossing the split
     * is in some minimum spanning tree. Kruskal's next accepted edge is exactly
     * the lightest edge crossing the cut between the component it joins and the
     * rest.
     *
     * <p>Ties are broken by node id in the edge comparator, so the result is
     * reproducible even when several trees have the same weight.
     */
    public static ArrayList<Edge> run(Graph graph) {
        ArrayList<Edge> edges = graph.getEdges();
        Collections.sort(edges);

        UnionFind components = new UnionFind(graph.getNodes());
        ArrayList<Edge> tree = new ArrayList<>();

        for (Edge edge : edges) {
            Node from = edge.getSrc();
            Node to = edge.getDst();

            if (!components.find(from).equals(components.find(to))) {
                tree.add(edge);
                components.union(from, to);
            }

            if (components.getSetCount() == 1) {
                break;
            }
        }

        return tree;
    }
}
