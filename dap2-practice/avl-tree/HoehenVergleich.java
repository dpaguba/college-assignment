import java.util.Random;

/**
 * Answers the question the sheet ends with: where is the height difference largest?
 *
 * <p>Not part of the submission. Needs {@code SearchTree} from the previous
 * task: compile with
 * {@code javac -sourcepath ../binary-tree-traversal -d out HoehenVergleich.java}.
 *
 * <p>Output is redirected away while the trees are built, because AVLTree
 * prints its insertions and rotations by design.
 */
public class HoehenVergleich {

    public static void main(String[] args) {
        int size = args.length > 0 ? Integer.parseInt(args[0]) : 1000;

        int[] ascending = new int[size];
        for (int i = 0; i < size; i++) {
            ascending[i] = i;
        }

        int[] random = ascending.clone();
        Random rng = new Random(20260830);
        for (int i = size - 1; i > 0; i--) {
            int j = rng.nextInt(i + 1);
            int swap = random[i];
            random[i] = random[j];
            random[j] = swap;
        }

        System.out.printf("%-12s %14s %10s%n", "Eingabe", "SearchTree", "AVLTree");
        report("aufsteigend", ascending);
        report("zufaellig", random);
        System.out.println();
        System.out.println("Der Unterschied ist bei sortierter Eingabe am groessten: der");
        System.out.println("Suchbaum entartet dann zur Liste, der AVL-Baum nicht.");
    }

    private static void report(String label, int[] values) {
        SearchTree plain = new SearchTree(values);

        java.io.PrintStream real = System.out;
        System.setOut(new java.io.PrintStream(java.io.OutputStream.nullOutputStream()));
        AVLTree balanced = new AVLTree(values);
        System.setOut(real);

        System.out.printf("%-12s %14d %10d%n", label, plain.getHeight(), balanced.getHeight());
    }
}
