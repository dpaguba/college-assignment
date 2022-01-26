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
                  
