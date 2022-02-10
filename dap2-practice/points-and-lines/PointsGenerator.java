import java.util.Random;

/**
 * Generates random two-dimensional points in a square.
 *
 * <p>Sheet 4, task 4.1. The seed is part of the constructor so that a run can be
 * repeated exactly, which is the only reason the expected outputs on the sheet
 * are checkable at all.
 */
public class PointsGenerator {

    private final double min;
    private final double max;
    private final Random rng;

    public PointsGenerator(double min, double max, int seed) {
        this.min = min;
        this.max = max;
        this.rng = new Random(seed);
    }

    /**
     * Returns the requested number of points from [min, max]^2.
     *
     * <p>The x coordinate of each point is drawn before its y coordinate, and
     * the points are drawn in order. Both facts are part of the interface here:
     * change either and the same seed produces a different point set.
     */
    public Point[] generate(int count) {
        Point[] points = new Point[count];

        for (int i = 0; i < count; i++) {
            double x = (rng.nextDouble() * (max - min) + min);
            double y = (rng.nextDouble() * (max - min) + min);
            points[i] = new Point(x, y);
        }

        return points;
    }
}
