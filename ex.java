import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class ex implements Runnable{
    public static void main(String[] args) throws IOException {
        ex obj = new ex();
        Thread th = new Thread(obj);
        th.start();
        System.out.println("Im out");
        System.out.println("Input ");
        // String str = readInput();
        // System.out.println(str + " from main");

    }

    @Override
    public void run() {
        System.out.print("\nDer Server wurde gestartet und wartet am Port 2022 auf Anfragen vom Client.\nWenn Sie den Server beenden wollen, dann geben Sie 'J' ein: ");
        try {
            String str = readInput();
            System.out.println(str);
        } catch (IOException e) {
            
            System.out.println("Im here");
        }
        
    }

    public static String readInput() throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        String name = reader.readLine();
        return name;
    }
}
