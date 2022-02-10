/**
 * A directed line through two points, and the side test that goes with it.
 *
 * <p>Sheet 4, task 4.1. Start and end do not bound the line, they orient it.
 */
public class Line {

    private Point start;
    private Point end;

    public Line(Point start, Point end) {
        this.start = start;
        this.end = end;
    }

    public Point getStart() {
        return start;
    }

    public Point getEnd() {
        return end;
    }

    /**
     * Which side of the line the point lies on: 1 left, −1 right, 0 on the line.
     *
     * <p>The sign of the cross product of (end − start) and (point − start).
     * Geometrically it is twice the signed area of the triangle, so it is zero
     * exactly when the three points are collinear, and its sign says which way
     * the triangle is wound.
     *
     * <p>This one primitive is the whole of the convex hull in the next task,
     * and of most planar geometry besides. It needs no division, no square
     * root, and no trigonometry, which is why it is the standard predicate:
     * on integer input it is exact.
     */
    public int side(Point point) {
        double cross = (end.get(0) - start.get(0)) * (point.get(1) - start.get(1))
                - (end.get(1) - start.get(1)) * (point.get(0) - start.get(0));

        if (cross > 0) {
            return 1;
        }
        return cross < 0 ? -1 : 0;
    }

    /** Swaps start and end, which flips the sign of every side test. */
    public void invertDirection() {
        Point swap = start;
        start = end;
        end = swap;
    }

    @Override
    public String toString() {
        return start + " -- " + end;
    }
}
