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
                    }catch (IllegalArgumentException q1){
                    System.out.print("Falscher Parameter! Nur Integer groesser 0 sind erlaubt.\nAufruf mit : java DAP2.Praktikum.Eratosthenes n [-o]\nEs wird die Anzahl der Primzahlen aus dem Bereich [2,n] berechnet.\nMit -o werden diese Zahlen auch ausgegeben.\nBsp: java DAP2.Praktikum.Eratosthenes 100 -o");
                }

                // An dieser Stelle erwartet man die Eingabe: n -o
            }else if (args.length == 2){
                try {
                    /*
                    Falls der Parameter zum Integer-Wert nicht umgewandelt werden kann,
                    erwartet man hier Fehlermeldung (57-59)

                    Falls nur ein Parameter eingetippt wird, erwartet man die Zahl.
                    Dem String-Wert wird "" zugewiesen. Koennte der Wert zum int-Wert nicht zugewiesen werden,
                    erwartet man die Fehlermeldung (Zeile 57-59)

                    Werden zwei Parameter eingegeben, dann erwartet man, dass der zweite Wert dem Ausdruck "-o"
                    entspricht und der erste Parameter weist man zum int-Wert.
                     */
                  

# Modified 2025-08-11 10:24:29