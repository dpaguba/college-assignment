import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;

/**
 * Single source shortest paths, negative weights allowed.
 *
 * <p>Sheet 12, task 12.1. Both parts: the improved version that stops as soon
 * as a round changes nothing, and the handling of negative cycles.
 */
public class BellmanFord {

    /**
     * Shortest path weights from s to every node.
     *
     * <p>Relax every edge, n − 1 times. After round k every shortest path using
     * at most k edges has been found, and a shortest path in a graph without
     * negative cycles uses at most n − 1 edges, so n − 1 rounds suffice.
     *
     * <p>The improvement over the textbook version is the early exit: if a full
     * round changes nothing, no later round can change anything either, because
     * every relaxation depends on a value that changed in the round before. On
     * most inputs that ends the loop long before n − 1.
     *
     * <p>O(n·m) in the worst case, against Dijkstra's O(m log n). The price buys
     * negative edges, which Dijkstra cannot handle at all: its argument for
     * settling the nearest node assumes no edge can make a path shorter.
     *
     * <p>Negative cycles are detected by one extra round. Anything that still
     * improves lies on or after such a cycle, and every node reachable from it
     * has no finite shortest path, so MIN_WEIGHT is propagated forward from
     * there. Note the direction: being reachable *from* the cycle is what
     * matters, not lying on it.
     *
     * @param adjLists outgoing edges per node
     * @param s the source
     * @return weights, MAX_WEIGHT when unreachable, MIN_WEIGHT when unbounded
     */
    public static int[] bellmanFord(List<Edge>[] adjLists, int s) {
        int nodeCount = adjLists.length;
        int[] distance = new int[nodeCount];

        for (int i = 0; i < nodeCount; i++) {
            distance[i] = ShortestPaths.MAX_WEIGHT;
        }
        distance[s] = 0;

        for (int round = 0; round < nodeCount - 1; round++) {
            boolean changed = false;

            for (List<Edge> edges : adjLists) {
                for (Edge edge : edges) {
                    if (distance[edge.src] == ShortestPaths.MAX_WEIGHT) {
                        continue;
                    }
                    int candidate = distance[edge.src] + edge.weight;
                    if (candidate < distance[edge.dst]) {
                        distance[edge.dst] = candidate;
                        changed = true;
                    }
                }
            }

            if (!changed) {
                return distance;
            }
        }

        List<Integer> affected = new ArrayList<>();
        for (List<Edge> edges : adjLists) {
            for (Edge edge : edges) {
                if (distance[edge.src] == ShortestPaths.MAX_WEIGHT) {
                    continue;
                }
                if (distance[edge.src] + edge.weight < distance[edge.dst]) {
                    affected.add(edge.dst);
                }
            }
        }

        if (!affected.isEmpty()) {
            boolean[] unbounded = new boolean[nodeCount];
            Deque<Integer> queue = new ArrayDeque<>(affected);
            for (int node : affected) {
                unbounded[node] = true;
            }

            while (!queue.isEmpty()) {
                int node = queue.poll();
                distance[node] = ShortestPaths.MIN_WEIGHT;
                for (Edge edge : adjLists[node]) {
                    if (!unbounded[edge.dst]) {
                        unbounded[edge.dst] = true;
                        queue.add(edge.dst);
                    }
                }
            }
        }

        return distance;
    }
}
