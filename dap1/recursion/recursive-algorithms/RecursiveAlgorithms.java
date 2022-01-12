import java.util.ArrayList;
import java.util.List;

/**
 * The recursive algorithms of chapter five: the pots, the ship, the stairs.
 *
 * <p>The three examples are chosen to be different shapes of recursion. The
 * pots (the towers of Hanoi in the lecture's telling) recurse twice and
 * produce a sequence of moves. The stairs recurse twice and produce a count,
 * which is why the answer is the Fibonacci sequence. Loading the ship is
 * backtracking: a branch that fails is abandoned and the next choice tried.
 */
public class RecursiveAlgorithms {

    /** How many moves the puzzle needs for the given number of discs. */
    public static int hanoiMoves(int discs) {
        if (discs <= 0) {
            return 0;
        }
        return 2 * hanoiMoves(discs - 1) + 1;
    }

    /** The moves themselves, each as a pair of pegs. */
    public static List<int[]> hanoi(int discs) {
        List<int[]> moves = new ArrayList<>();
        move(discs, 1, 3, 2, moves);
        return moves;
    }

    private static void move(int discs, int from, int to, int spare, List<int[]> moves) {
        if (discs <= 0) {
            return;
        }
        move(discs - 1, from, spare, to, moves);
        moves.add(new int[] {from, to});
        move(discs - 1, spare, to, from, moves);
    }

    /**
     * Whether the produced moves obey the rule that no disc rests on a
     * smaller one.
     *
     * <p>Checked by replaying the moves onto three stacks, which is an
     * independent test of the recursion: the count and the sequence are
     * produced by different code paths and both have to agree with the rules.
     */
    public static boolean hanoiIsLegal(int discs) {
        List<List<Integer>> pegs = new ArrayList<>();
        for (int peg = 0; peg < 3; peg++) {
            pegs.add(new ArrayList<>());
        }
        for (int disc = discs; disc >= 1; disc--) {
            pegs.get(0).add(disc);
        }
        for (int[] step : hanoi(discs)) {
            List<Integer> from = pegs.get(step[0] - 1);
            List<Integer> to = pegs.get(step[1] - 1);
            if (from.isEmpty()) {
                return false;
            }
            int disc = from.remove(from.size() - 1);
            if (!to.isEmpty() && to.get(to.size() - 1) < disc) {
                return false;
            }
            to.add(disc);
        }
        return pegs.get(2).size() == discs;
    }

    /** How many ways there are to climb the stairs in steps of one or two. */
    public static int stairWays(int steps) {
        if (steps < 0) {
            return 0;
        }
        if (steps == 0) {
            return 1;
        }
        return stairWays(steps - 1) + stairWays(steps - 2);
    }

    /** The same with steps of any size up to the given maximum. */
    public static int stairWaysUpTo(int steps, int largestStep) {
        if (steps < 0) {
            return 0;
        }
        if (steps == 0) {
            return 1;
        }
        int ways = 0;
        for (int step = 1; step <= largestStep; step++) {
            ways += stairWaysUpTo(steps - step, largestStep);
        }
        return ways;
    }

    /**
     * Whether the containers can be loaded without tilting the ship past the
     * allowed divergence.
     *
     * <p>Each container goes to port or to starboard, so the search tree is
     * binary and the divergence is the running difference between the two
     * sides. A branch is abandoned as soon as the divergence exceeds the
     * limit, which is what makes this backtracking rather than enumeration.
     */
    public static boolean existsBalance(int[] containers, int position, int divergence,
            int allowed) {
        if (Math.abs(divergence) > allowed) {
            return false;
        }
        if (position == containers.length) {
            return true;
        }
        return existsBalance(containers, position + 1, divergence + containers[position], allowed)
                || existsBalance(containers, position + 1, divergence - containers[position],
                        allowed);
    }

    /**
     * The same question answered by trying every assignment of sides.
     *
     * <p>An independent oracle: the bits of a counter decide port or
     * starboard, and the running divergence is checked after each container,
     * so nothing about the backtracking is reused.
     */
    public static boolean existsBalanceBruteForce(int[] containers, int allowed) {
        int patterns = 1 << containers.length;
        for (int pattern = 0; pattern < patterns; pattern++) {
            int divergence = 0;
            boolean fine = true;
            for (int index = 0; index < containers.length; index++) {
                divergence += ((pattern >> index) & 1) == 1 ? containers[index]
                        : -containers[index];
                if (Math.abs(divergence) > allowed) {
                    fine = false;
                    break;
                }
            }
            if (fine) {
                return true;
            }
        }
        return false;
    }

    /** Whether the ship ends exactly level, which the sheet asks for. */
    public static boolean existsTotalBalance(int[] containers, int position, int divergence) {
        if (position == containers.length) {
            return divergence == 0;
        }
        return existsTotalBalance(containers, position + 1, divergence + containers[position])
                || existsTotalBalance(containers, position + 1, divergence - containers[position]);
    }

    /**
     * The same with three holds and a limit on how many containers each takes.
     *
     * <p>The middle hold does not affect the divergence, so it is a place to
     * put containers that would otherwise unbalance the ship. That makes the
     * search tree ternary and the limits the only thing that prunes it.
     */
    public static boolean existsBalanceWith3Limited(int[] containers, int position,
            int divergence, int[] loads, int containerLimit) {
        if (position == containers.length) {
            return divergence == 0;
        }
        for (int hold = 0; hold < 3; hold++) {
            if (loads[hold] >= containerLimit) {
                continue;
            }
            loads[hold]++;
            int change = hold == 0 ? containers[position] : hold == 1 ? 0 : -containers[position];
            if (existsBalanceWith3Limited(containers, position + 1, divergence + change, loads,
                    containerLimit)) {
                loads[hold]--;
                return true;
            }
            loads[hold]--;
        }
        return false;
    }
}
