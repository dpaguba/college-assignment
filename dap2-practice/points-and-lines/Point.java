import java.util.Locale;

/**
 * A point in R^d, stored as double coordinates.
 *
 * <p>Sheet 4, task 4.1. The constructor takes any number of coordinates through
 * varargs, so the same class serves the two-dimensional geometry of this sheet
 * and anything higher.
 */
public class Point {

    private final double[] coordinates;

    /** Takes the coordinates in order; any dimension is allowed, including zero. */
    public Point(double... coordinates) {
        this.coordinates = coordinates.clone();
    }

    /** The i-th coordinate. */
    public double get(int i) {
        return coordinates[i];
    }

    /** How many coordinates this point has. */
    public int dimension() {
        return coordinates.length;
    }

    /**
     * Coordinates in brackets, two decimals, comma separated.
     *
     * <p>Locale.ROOT is not decoration: the default locale on a German system
     * formats 13.12 as "13,12", which would break every line of the expected
     * output and every comma-separated list along with it.
     */
    @Override
    public String toString() {
        StringBuilder text = new StringBuilder("(");
        for (int i = 0; i < coordinates.length; i++) {
            if (i > 0) {
                text.append(", ");
            }
            text.append(String.format(Locale.ROOT, "%.2f", coordinates[i]));
        }
        return text.append(')').toString();
    }
}
