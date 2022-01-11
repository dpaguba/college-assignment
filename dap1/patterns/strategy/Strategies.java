/**
 * Choosing a strategy while the program runs.
 *
 * <p>The traversal is written once. Which computation it performs is decided
 * by the object handed to it, so a caller can pick by name, by configuration,
 * or by anything else, and the list never learns what was chosen.
 */
public class Strategies {

    /** Runs a counting strategy chosen by name and returns its result. */
    public static int applyNamed(DoublyLinkedList<Integer> list, String name) {
        if (name.equals("count zeros")) {
            CountXStrategy strategy = new CountXStrategy(0);
            list.traverse(strategy);
            return strategy.count();
        }
        if (name.equals("count between one and five")) {
            CountInIntervalStrategy strategy = new CountInIntervalStrategy(1, 5);
            list.traverse(strategy);
            return strategy.count();
        }
        if (name.equals("average of positives")) {
            AverageOfPositivesStrategy strategy = new AverageOfPositivesStrategy();
            list.traverse(strategy);
            return (int) strategy.average();
        }
        throw new IllegalArgumentException("unknown strategy: " + name);
    }
}
