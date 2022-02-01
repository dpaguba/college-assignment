import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

/**
 * Builds one AVL tree per line of a CSV file read from standard input.
 *
 * <p>Sheet 8, task 8.2. Usage:
 * {@code java AVLTreeApplication [in|pre|post] < sample2.csv}. Insertions and
 * rotations are printed as they happen, then the height, the traversal, and a
 * line of ten dashes.
 */
public class AVLTreeApplication {

    public static void main(String[] args) {
        String traversal = null;

        if (args.length > 1) {
            System.out.println("FEHLER: Zu viele Parameter.");
            usage();
            return;
        }
        if (args.length == 1) {
            if (!isTraversal(args[0])) {
                System.out.println("FEHLER: Unbekannte Traversierung: " + args[0]);
                usage();
                return;
            }
            traversal = args[0];
        }

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
            System.out.println("FEHLER: Leere Eingabe. Die Datei muss mindestens eine Zeile "
                    + "mit durch Kommas getrennte Integer enthalten.");
            usage();
            return;
        }

        int firstNumberLine = 0;
        if (isTraversal(lines.get(0))) {
            if (traversal == null) {
                traversal = lines.get(0);
            }
            firstNumberLine = 1;

            if (lines.size() == 1) {
                System.out.println("FEHLER: Traversierung, aber keine Integer gefunden. Die Datei "
                        + "muss mindestens eine Zeile mit durch Kommas getrennte Integer enthalten.");
                usage();
                return;
            }
        } else if (lines.get(0).matches("[a-zA-Z]+")) {
            System.out.println("FEHLER: Unbekannte Traversierung: " + lines.get(0));
            usage();
            return;
        }

        if (traversal == null) {
            traversal = "in";
        }

        for (int i = firstNumberLine; i < lines.size(); i++) {
            int[] values;
            try {
                values = parse(lines.get(i));
            } catch (NumberFormatException notIntegers) {
                System.out.println("FEHLER: Zeilen duerfen nur aus Integern bestehen.");
                usage();
                return;
            }

            AVLTree tree = new AVLTree(values);
            System.out.println("Hoehe: " + tree.getHeight());

            switch (traversal) {
                case "pre" -> tree.preOrder();
                case "post" -> tree.postOrder();
                default -> tree.inOrder();
            }

            System.out.println("-".repeat(10));
        }
    }

    private static boolean isTraversal(String candidate) {
        return candidate.equals("in") || candidate.equals("pre") || candidate.equals("post");
    }

    private static int[] parse(String line) {
        String[] parts = line.split(",");
        int[] values = new int[parts.length];
        for (int i = 0; i < parts.length; i++) {
            values[i] = Integer.parseInt(parts[i].trim());
        }
        return values;
    }

    private static void usage() {
        System.out.println("Aufruf: java AVLTreeApplication < <filename>");
    }
}
