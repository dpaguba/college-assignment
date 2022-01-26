public class Eratosthenes {
    public static void main(String[] args) throws Exception{
        // Zuerst wird erwartet, dass die Parameteranzahl der vorgesehenen entspricht.
        try {
            /*
            Zuerst betrachtet man den Fall, wenn nur eine Zahl uebergegeben werden soll.
            Wenn's nicht der Fall ist, wird die Fehlermeldung(Zeile 63 - 65) ausgegeben
             */
            if (args.length == 1){
                /*
                Die Gueltigkeit der uebergegebenen Parameter laesst sich durch dieses try-catch Block ueberpruefen.
                 */
                try {
                    /*
                    Falls der Parameter zum Integer-Wert nicht umgewandelt werden kann,
                    erwartet man hier Fehlermeldung (Zeile 29 - 30)
                     */
                    int point = Integer.parseInt(args[0]);
                    /*
                    Als Primzahlen wird in unserem Fall nur die Menge der natuerlichen Zahlen betrachtet.
                    Hat der Parameter einen negativen Wert, wird die Fehlermeldung (Zeile 29 - 30) ausgegeben.
                    Somit betrachten wir nur die positiven Zahlen.
                     */
                    if (point > 0){
                        System.out.print(countPrim(point));
                    }else {
                        throw new IllegalArgumentException();
                    }
                  
