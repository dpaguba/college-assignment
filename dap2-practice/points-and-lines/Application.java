/**
 * Test driver for {@link Point}, {@link Line} and {@link PointsGenerator}.
 *
 * <p>Sheet 4, task 4.1. Two ways to call it:
 * {@code java Application n seed} generates n random points in [0, 100]^2, and
 * {@code java Application x1 y1 x2 y2 x3 y3 ...} reads them from the command
 * line. The first two points span a line, and every further point is reported
 * as left of it, right of it, or on it.
 */
public class Application {

    public static void main(String[] args) {
        Point[] points = readPoints(args, "Application");
        if (points == null) {
            return;
        }

        Line line = new Line(points[0], points[1]);
        System.out.println("Vergleiche Punkte mit der Geraden " + line);

        for (int i = 2; i < points.length; i++) {
            int side = line.side(points[i]);

            if (side > 0) {
                System.out.println("Punkt " + points[i] + " liegt links der Linie.");
            } else if (side < 0) {
                System.out.println("Punkt " + points[i] + " liegt rechts der Linie.");
            } else {
                System.out.println("Punkt " + points[i] + " liegt auf der Linie.");
                if (isBetween(points[0], points[1], points[i])) {
                    System.out.println("Punkt " + points[i] + " liegt zwischen "
                            + points[0] + " und " + points[1]);
                }
            }
        }
    }

    /**
     * True when k lies on the segment between i and j.
     *
     * <p>The three points are assumed collinear, which is what makes the test
     * this cheap: comparing coordinate ranges is enough, no projection needed.
     * Both coordinates have to be checked, because a vertical segment has a
     * constant x and a horizontal one a constant y.
     */
    public static boolean isBetween(Point i, Point j, Point k) {
        return Math.min(i.get(0), j.get(0)) <= k.get(0) && k.get(0) <= Math.max(i.get(0), j.get(0))
                && Math.min(i.get(1), j.get(1)) <= k.get(1) && k.get(1) <= Math.max(i.get(1), j.get(1));
    }

    /**
     * Parses the two accepted argument forms, or prints the error and returns null.
     *
     * <p>Shared with {@link SimpleConvexHull}, which takes exactly the same
     * arguments and differs only in the program name inside the help text.
     *
     * <p>The coordinate form needs an even count and more than two points, so at
     * least six numbers. Four would be a line with nothing left to compare to it.
     */
    public static Point[] readPoints(String[] args, String programName) {
        if (args.length == 2) {
            int count;
            try {
                count = Integer.parseInt(args[0]);
            } catch (NumberFormatException notAnInteger) {
                System.out.println("Falscher Parameter! Nur Integer groesser 2 sind erlaubt.");
                usage(programName);
                return null;
            }

            if (count <= 2) {
                System.out.println("Anzahl der Punkte muss groesser als 2 sein.");
                usage(programName);
                return null;
            }

            int seed;
            try {
                seed = Integer.parseInt(args[1]);
            } catch (NumberFormatException notAnInteger) {
                System.out.println("Falscher Parameter! Als Seed sind nur Integer erlaubt.");
                usage(programName);
                return null;
            }

            return new PointsGenerator(0, 100, seed).generate(count);
        }

        if (args.length > 4 && args.length % 2 == 0) {
            Point[] points = new Point[args.length / 2];
            try {
                for (int i = 0; i < points.length; i++) {
                    points[i] = new Point(Double.parseDouble(args[2 * i]),
                            Double.parseDouble(args[2 * i + 1]));
                }
            } catch (NumberFormatException notANumber) {
                System.out.println("Es war nicht moeglich, alle Punkte einzulesen.");
                usage(programName);
                return null;
            }
            return points;
        }

        System.out.println("Falsche Parameteranzahl!");
        usage(programName);
        return null;
    }

    private static void usage(String programName) {
        System.out.println("Aufruf mit : java " + programName + " numberOfPoints seed");
        System.out.println("oder mit gerader Anzahl Koordinaten: java " + programName
                + " p1x p1y p2x p2y ...");
        System.out.println("Bsp: java " + programName + " 100 1337");
    }
}
