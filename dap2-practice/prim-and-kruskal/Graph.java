import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;

/**
 * An undirected weighted graph. Sheet 11, provided class, reimplemented.
 *
 * <p>Every edge is stored twice, once in each endpoint's adjacency list, with
 * the two halves linked as siblings.
 */
public class Graph {

    private final ArrayList<Node> nodes = new ArrayList<>();

    public Graph() {
    }

    public boolean contains(int id) {
        return getNode(id) != null;
    }

    /**
     * Adds a node unless the id is taken.
     *
     * @return true when the node was added
     */
    public boolean addNode(int id) {
        if (contains(id)) {
            return false;
        }
        nodes.add(new Node(id));
        return true;
    }

    public Node getNode(int id) {
        for (Node node : nodes) {
            if (node.getId() == id) {
                return node;
            }
        }
        return null;
    }

    public ArrayList<Node> getNodes() {
        return nodes;
    }

    public int numNodes() {
        return nodes.size();
    }

    /**
     * Adds an undirected edge as two linked halves.
     *
     * @return true when both nodes exist and the edge was new
     */
    public boolean addEdge(int srcid, int dstid, int weight) {
        Node source = getNode(srcid);
        Node destination = getNode(dstid);

        if (source == null || destination == null || source.adjacent(destination)) {
            return false;
        }

        Edge forward = new Edge(source, destination, weight);
        Edge backward = new Edge(destination, source, weight);
        forward.setSiblingEdge(backward);
        backward.setSiblingEdge(forward);

        source.addEdge(forward);
        destination.addEdge(backward);
        return true;
    }

    /**
     * Every undirected edge once, oriented from the smaller id to the larger.
     *
     * <p>Taking both halves would make Kruskal look at each edge twice. The
     * second look is harmless, since the endpoints are already in one set by
     * then, but it doubles the sort.
     */
    public ArrayList<Edge> getEdges() {
        ArrayList<Edge> edges = new ArrayList<>();
        for (Node node : nodes) {
            for (Edge edge : node.getAdjList()) {
                if (edge.getSrc().getId() < edge.getDst().getId()) {
                    edges.add(edge);
                }
            }
        }
        return edges;
    }

    /**
     * Reads a graph from standard input, one edge per line as {@code u,v,w}.
     *
     * @throws IllegalArgumentException when a line is malformed or an edge repeats
     */
    public static Graph fromSystemIn() throws IllegalArgumentException, IOException {
        Graph graph = new Graph();

        try (BufferedReader reader = new BufferedReader(new InputStreamReader(System.in))) {
            String line;
            while ((line = reader.readLine()) != null) {
                line = line.trim();
                if (line.isEmpty()) {
                    continue;
                }

                String[] parts = line.split(",");
                if (parts.length != 3) {
                    throw new IllegalArgumentException("Kanten konnten nicht eingelesen werden.");
                }

                int from = Integer.parseInt(parts[0].trim());
                int to = Integer.parseInt(parts[1].trim());
                int weight = Integer.parseInt(parts[2].trim());

                graph.addNode(from);
                graph.addNode(to);

                if (!graph.addEdge(from, to, weight)) {
                    throw new IllegalArgumentException("Graph enthaelt doppelte Kanten.");
                }
            }
        } catch (NumberFormatException notANumber) {
            throw new IllegalArgumentException("Kanten konnten nicht eingelesen werden.");
        }

        return graph;
    }

    @Override
    public String toString() {
        return getEdges().toString();
    }
}
