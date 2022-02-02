import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

/**
 * Test harness for the two shortest path algorithms of sheet 12.
 *
 * <p>Usage: {@code java ShortestPaths bf < datei.graph} for Bellman-Ford from
 * node 0, or {@code java ShortestPaths fw < datei.graph} for Floyd-Warshall.
 *
 * <p>The file holds n on the first line, m on the second, and then m lines of
 * {@code u v w}. The course provided this program; it was not in the material
 * that survived, so this is a reimplementation from the format the sheet
 * describes.
 */
public class ShortestPaths {

    /** No path exists. */
    public static final int MAX_WEIGHT = Integer.MAX_VALUE;

    /** A path exists but its weight is unbounded below, through a negative cycle. */
    public static final int MIN_WEIGHT = Integer.MIN_VALUE;

    public static void main(String[] args) throws IOException {
        if (args.length != 1 || (!args[0].equals("bf") && !args[0].equals("fw"))) {
            System.out.println("FEHLER: Aufruf mit java ShortestPaths bf|fw < datei.graph");
            return;
        }

        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        int nodeCount = Integer.parseInt(reader.readLine().trim());
        int edgeCount = Integer.parseInt(reader.readLine().trim());

        @SuppressWarnings("unchecked")
        List<Edge>[] adjLists = new List[nodeCount];
        for (int i = 0; i < nodeCount; i++) {
            adjLists[i] = new ArrayList<>();
        }

        int[][] matrix = new int[nodeCount][nodeCount];
        for (int i = 0; i < nodeCount; i++) {
            for (int j = 0; j < nodeCount; j++) {
                matrix[i][j] = i == j ? 0 : MAX_WEIGHT;
            }
        }

        for (int read = 0; read < edgeCount; read++) {
            StringTokenizer parts = new StringTokenizer(reader.readLine());
            int from = Integer.parseInt(parts.nextToken());
            int to = Integer.parseInt(parts.nextToken());
            int weight = Integer.parseInt(parts.nextToken());

            adjLists[from].add(new Edge(from, to, weight));
            matrix[from][to] = Math.min(matrix[from][to], weight);
        }

        if (args[0].equals("bf")) {
            int[] distances = BellmanFord.bellmanFord(adjLists, 0);
            for (int i = 0; i < nodeCount; i++) {
                System.out.println("d(0, " + i + ") = " + format(distances[i]));
            }
        } else {
            int[][] distances = FloydWarshall.floydWarshall(matrix);
            for (int i = 0; i < nodeCount; i++) {
                StringBuilder row = new StringBuilder();
                for (int j = 0; j < nodeCount; j++) {
                    if (row.length() > 0) {
                        row.append(' ');
                    }
                    row.append(String.format("%6s", format(distances[i][j])));
                }
                System.out.println(row);
            }
        }
    }

    /** The two sentinels are printed as symbols, since their numeric values are noise. */
    static String format(int distance) {
        if (distance == MAX_WEIGHT) {
            return "INF";
        }
        return distance == MIN_WEIGHT ? "-INF" : String.valueOf(distance);
    }
}

/** A directed weighted edge, as given by the course in this file. */
class Edge {

    final int src;
    final int dst;
    final int weight;

    Edge(int src, int dst, int weight) {
        this.src = src;
        this.dst = dst;
        this.weight = weight;
    }

    @Override
    public String toString() {
        return src + "->" + dst + "(" + weight + ")";
    }
}
