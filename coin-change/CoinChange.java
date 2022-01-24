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
              // ueberpruefen, ob der int-Wert uebergegeben wird. Falls nicht, wirft die Ausnahme in der Zeile 21.
                try {
                    //wandelt String-Wert in int-Wert
                    change = Integer.parseInt(args[1]);
                }catch (IllegalArgumentException iae){
                    System.out.println( "FEHLER: Falscher Parametertyp fuer das Wechselgeld!");
                    displayExample();
                    return;
                }

                // ueberprueft, ob die bekannte Waehrung angegeben wird. Falls nicht, wirft die Ausnahme in der Zeile 59.
                if (currency.equals("Euro") || currency.equals("Mira")){
}
