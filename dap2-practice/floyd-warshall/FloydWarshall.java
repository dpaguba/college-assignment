/**
 * All pairs shortest paths.
 *
 * <p>Sheet 12, task 12.2. Both parts: the plain algorithm and the handling of
 * negative cycles.
 *
 * <p>Needs the constants from {@code ShortestPaths}. Compile with
 * {@code javac -sourcepath ../bellman-ford -d out FloydWarshall.java}.
 */
public class FloydWarshall {

    /**
     * The full distance matrix, in Theta(n³) time and Theta(n²) space.
     *
     * <p>The loop order is the algorithm. The outer loop over k means: allow
     * paths whose interior nodes all come from {0..k}. Each cell then asks
     * whether going through k beats what was known without it. Putting k inside
     * would ask the same question before the answers it depends on exist, and
     * the result would silently be wrong on some inputs.
     *
     * <p>It is dynamic programming over subsets of allowed intermediate nodes,
     * with the third dimension of the table dropped because row k of the new
     * layer equals row k of the old one. That is why the update can be done in
     * place.
     *
     * <p>Running Dijkstra from every node is O(n·m log n) and beats this on
     * sparse graphs, but it cannot take negative edges. Running Bellman-Ford n
     * times can, at O(n²·m), which is worse on dense graphs and is what the
     * sheet explicitly forbids.
     *
     * <p>A negative diagonal entry after the main loop means node i lies on a
     * negative cycle. Every pair that can route through such a node has no
     * finite distance, so it is marked MIN_WEIGHT in a final pass.
     */
    public static int[][] floydWarshall(int[][] adjMatrix) {
        int nodeCount = adjMatrix.length;
        int[][] distance = new int[nodeCount][nodeCount];

        for (int i = 0; i < nodeCount; i++) {
            System.arraycopy(adjMatrix[i], 0, distance[i], 0, nodeCount);
        }

        for (int k = 0; k < nodeCount; k++) {
            for (int i = 0; i < nodeCount; i++) {
                if (distance[i][k] == ShortestPaths.MAX_WEIGHT) {
                    continue;
                }
                for (int j = 0; j < nodeCount; j++) {
                    if (distance[k][j] == ShortestPaths.MAX_WEIGHT) {
                        continue;
                    }
                    int candidate = distance[i][k] + distance[k][j];
                    if (candidate < distance[i][j]) {
                        distance[i][j] = candidate;
                    }
                }
            }
        }

        for (int k = 0; k < nodeCount; k++) {
            if (distance[k][k] >= 0) {
                continue;
            }
            for (int i = 0; i < nodeCount; i++) {
                for (int j = 0; j < nodeCount; j++) {
                    if (distance[i][k] != ShortestPaths.MAX_WEIGHT
                            && distance[k][j] != ShortestPaths.MAX_WEIGHT) {
                        distance[i][j] = ShortestPaths.MIN_WEIGHT;
                    }
                }
            }
        }

        return distance;
    }
}
