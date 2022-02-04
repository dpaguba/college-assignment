import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Scanner;

/**
 * Shortest path between two nodes, read from a .graph file on standard input.
 *
 * <p>Sheet 10, task 10.2. Usage:
 * {@code java DijkstraApplication < BspGraphKlein0-4.graph}. The first line
 * holds the start and goal ids, every following line one edge as
 * {@code src,dst,weight}.
 *
 * <p>Needs the graph classes from the previous task. Compile with
 * {@code javac -sourcepath ../graph-class -d out *.java}.
 */
public class DijkstraApplication {

    public static void main(String[] args) {
        List<String> lines = new ArrayList<>();
        try (Scanner scanner = new Scanner(System.in)) {
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine().trim();
                if (!line.isEmpty()) {
                    lines.add(line);
                }
            }
        }

        if (lines.isEmpty()) {
            fail("Leere Eingabe.");
            return;
        }

        int source;
        int target;
        try {
            String[] query = lines.get(0).split(",");
            if (query.length != 2) {
                throw new NumberFormatException();
            }
            source = Integer.parseInt(query[0].trim());
            target = Integer.parseInt(query[1].trim());
        } catch (NumberFormatException malformed) {
            fail("Fehlerhafte Angabe von Start- und Zielknoten.");
            return;
        }

        Graph graph = new Graph();
        for (int i = 1; i < lines.size(); i++) {
            String[] parts = lines.get(i).split(",");
            if (parts.length != 3) {
                fail("Kanten konnten nicht eingelesen werden.");
                return;
            }

            int from;
            int to;
            int weight;
            try {
                from = Integer.parseInt(parts[0].trim());
                to = Integer.parseInt(parts[1].trim());
                weight = Integer.parseInt(parts[2].trim());
            } catch (NumberFormatException malformed) {
                fail("Kanten konnten nicht eingelesen werden.");
                return;
            }

            if (weight <= 0) {
                fail("Alle Kantengewichte muessen groesser 0 sein.");
                return;
            }

            graph.addNode(from);
            graph.addNode(to);

            if (!graph.addEdge(from, to, weight)) {
                fail("Graph enthaelt doppelte Kanten.");
                return;
            }
        }

        if (!graph.contains(source) || !graph.contains(target)) {
            fail("Start- oder Zielknoten sind nicht im Graph enthalten.");
            return;
        }

        DijkstraResult result = dijkstra(graph, source, target);

        if (result == null) {
            System.out.println("Es wurde kein Pfad von Knoten " + source + " zu Knoten "
                    + target + " gefunden.");
            return;
        }

        StringBuilder path = new StringBuilder();
        for (Node node : result.getPath().getNodes()) {
            if (path.length() > 0) {
                path.append(", ");
            }
            path.append(node.getId());
        }

        System.out.println("Kuerzester Pfad " + path + " mit Laenge " + result.getLength()
                + " gefunden.");
    }

    /**
     * Dijkstra's algorithm, stopping as soon as the target is settled.
     *
     * <p>Keep tentative distances in a min-priority queue, repeatedly settle the
     * nearest unsettled node, and relax its outgoing edges. O((n + m) log n)
     * with a binary heap.
     *
     * <p>Settling the nearest unsettled node is safe because all weights are
     * positive: any other route to it would have to leave through a node that is
     * already at least as far away, so it could only be longer. Introduce one
     * negative edge and that argument collapses, which is why Bellman-Ford
     * exists.
     *
     * <p>The search stops when the target comes out of the queue rather than
     * when the queue empties. The distance of a settled node is final, so
     * everything after that point would be computed for nothing.
     *
     * @return the path as a graph plus its length, or null when the target is unreachable
     *
     * <p>The predecessors are walked back from the target so that the result carries
     * the route and not only its length.
     */
    public static DijkstraResult dijkstra(Graph g, int src, int dst) {
        HashMap<Integer, Integer> distance = new HashMap<>();
        HashMap<Integer, Integer> predecessor = new HashMap<>();
        HashSet<Integer> settled = new HashSet<>();

        MinPQ queue = new MinPQ();
        distance.put(src, 0);
        queue.insert(g.getNode(src), 0);

        while (!queue.isEmpty()) {
            HeapElement current = queue.extractMin();
            int id = current.getNode().getId();

            if (!settled.add(id)) {
                continue;
            }
            if (id == dst) {
                break;
            }

            for (Edge edge : current.getNode().getAdjList()) {
                int neighbour = edge.getDst().getId();
                if (settled.contains(neighbour)) {
                    continue;
                }

                int candidate = current.getDistance() + edge.getWeight();
                Integer known = distance.get(neighbour);

                if (known == null || candidate < known) {
                    distance.put(neighbour, candidate);
                    predecessor.put(neighbour, id);
                    queue.insert(edge.getDst(), candidate);
                }
            }
        }

        if (!distance.containsKey(dst)) {
            return null;
        }

        ArrayList<Integer> reversed = new ArrayList<>();
        for (Integer step = dst; step != null; step = predecessor.get(step)) {
            reversed.add(step);
            if (step == src) {
                break;
            }
        }

        Graph path = new Graph();
        for (int i = reversed.size() - 1; i >= 0; i--) {
            path.addNode(reversed.get(i));
        }
        for (int i = reversed.size() - 1; i > 0; i--) {
            int from = reversed.get(i);
            int to = reversed.get(i - 1);
            path.addEdge(from, to, distance.get(to) - distance.get(from));
        }

        return new DijkstraResult(path, distance.get(dst));
    }

    private static void fail(String message) {
        System.out.println("FEHLER: " + message);
        System.out.println("Aufruf: java DijkstraApplication < <filename>");
    }
}
