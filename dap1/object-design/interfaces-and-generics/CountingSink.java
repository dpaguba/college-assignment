/** An implementation that supplies only the label. */
public class CountingSink implements Sink {

    @Override
    public String label() {
        return "counted";
    }
}
