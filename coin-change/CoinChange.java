public class CoinChange {
  
  public static void main(String[] args) {

        try{
            /*
            Erste if-Schleife ueberprueft, ob die richtige Parameteranzahl geliefert wird. Falls nicht, greift die
            Ausnahme in der Zeile 56.
             */
            if (args.length == 2){
                //Variable fuer die Waehrung
                String currency = args[0];
                //Variable fuer das Wechselgeld
                int change;
}
