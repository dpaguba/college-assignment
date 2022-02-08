/**
 * Exercises {@link Graph}, since task 10.1 asks for no main method.
 */
public class GraphDemo {

    public static void main(String[] args) {
        Graph graph = new Graph();

        for (int id = 0; id < 4; id++) {
            if (!graph.addNode(id)) {
                throw new AssertionError("a fresh id was rejected");
            }
        }
        if (graph.addNode(2)) {
            throw new AssertionError("a duplicate id was accepted");
        }

        if (!graph.addEdge(0, 1, 4) || !graph.addEdge(0, 2, 1) || !graph.addEdge(2, 3, 7)) {
            throw new AssertionError("an edge between existing nodes was rejected");
        }
        if (graph.addEdge(0, 1, 9)) {
            throw new AssertionError("a second edge to the same destination was accepted");
        }
        if (graph.addEdge(0, 99, 1)) {
            throw new AssertionError("an edge to a missing node was accepted");
        }

        System.out.println("Knoten: " + graph.numNodes());
        System.out.println("Kanten: " + graph);
        System.out.println("contains(3) = " + graph.contains(3) + ", contains(9) = " + graph.contains(9));
        System.out.println("Adjazenzliste von 0: " + graph.getNode(0).getAdjList());

        try {
            new Edge(graph.getNode(0), graph.getNode(1), 0);
            throw new AssertionError("a weight of 0 was accepted");
        } catch (IllegalArgumentException expected) {
            System.out.println("Gewicht 0 wird abgelehnt: " + expected.getMessage());
        }
    }
}
