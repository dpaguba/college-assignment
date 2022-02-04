import java.util.LinkedList;

/**
 * The naive convex hull: test every pair of points as a candidate edge.
 *
 * <p>Sheet 4, task 4.2. Same arguments as {@code Application}:
 * {@code java SimpleConvexHull n seed} or a list of coordinates.
 *
 * <p>Needs the classes from the previous task. Compile with
 * {@code javac -sourcepath ../points-and-lines -d out SimpleConvexHull.java}
 * and run with {@code java -cp out SimpleConvexHull 5 678}.
 */
public class SimpleConvexHull {

    public static void main(String[] args) {
        Point[] points = Application.readPoints(args, "SimpleConvexHull");
        if (points == null) {
            return;
        }

        LinkedList<Point> hull = new SimpleConvexHull().computeHull(points);

        StringBuilder line = new StringBuilder();
        for (Point point : hull) {
            if (line.length() > 0) {
                line.append(" -- ");
            }
            line.append(point);
        }
        System.out.println(line);
    }

    /**
     * Returns the hull points in order around the boundary.
     *
     * <p>The method from the lecture, and it is deliberately the slow one. Every
     * ordered pair of points spans a candidate edge, and the pair belongs to the
     * hull exactly when all remaining points lie on one side of it. Testing one
     * pair costs O(n), and there are O(n²) pairs, so the whole thing is O(n³).
     *
     * <p>Graham scan and the divide and conquer hull both do it in O(n log n),
     * and the sorted hull in this repository is one of them. The value of the
     * cubic version is that it is obviously correct: it is the definition of a
     * hull edge, written out.
     *
     * <p>The edges are recorded as a successor per point, and the boundary is then
     * read off by walking them once around. The guard on the list length stops a
     * degenerate input, every point on one line, from looping for ever.
     */
    public LinkedList<Point> computeHull(Point[] points) {
        int count = points.length;

        int[] successor = new int[count];
        java.util.Arrays.fill(successor, -1);
        int firstDestination = -1;

        for (int i = 0; i < count; i++) {
            for (int j = i + 1; j < count; j++) {
                if (samePlace(points[i], points[j])) {
                    continue;
                }

                int from = -1;
                int to = -1;
                if (isHullEdge(points, i, j)) {
                    from = i;
                    to = j;
                } else if (isHullEdge(points, j, i)) {
                    from = j;
                    to = i;
                }

                if (from >= 0) {
                    System.out.println("Neue Aussenkante gefunden: " + new Line(points[from], points[to]));
                    successor[from] = to;
                    if (firstDestination < 0) {
                        firstDestination = to;
                    }
                }
            }
        }

        LinkedList<Point> hull = new LinkedList<>();
        if (firstDestination < 0) {
            return hull;
        }

        int current = firstDestination;
        do {
            hull.add(points[current]);
            current = successor[current];
        } while (current >= 0 && current != firstDestination && hull.size() <= count);

        return hull;
    }

    /**
     * True when every other point lies to the right of the directed edge.
     *
     * <p>Points exactly on the line are allowed, but only if they lie between
     * the two endpoints. A collinear point outside the segment means one of the
     * endpoints is not extreme, so the edge belongs to the interior of a longer
     * hull edge and has to be rejected. That is the whole handling of collinear
     * input, and it is what keeps only the outermost points of a shared line.
     */
    private boolean isHullEdge(Point[] points, int from, int to) {
        Line line = new Line(points[from], points[to]);

        for (int k = 0; k < points.length; k++) {
            if (k == from || k == to) {
                continue;
            }

            int side = line.side(points[k]);
            if (side > 0) {
                return false;
            }
            if (side == 0 && !Application.isBetween(points[from], points[to], points[k])) {
                return false;
            }
        }

        return true;
    }

    private boolean samePlace(Point first, Point second) {
        return first.get(0) == second.get(0) && first.get(1) == second.get(1);
    }
}
