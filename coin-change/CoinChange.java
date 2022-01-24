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
                  //ueberprueft, ob der fuers Wechselgeld keine negative Zahl ist. Falls nicht, wirft die Ausnahme in der Zeile 45.
                    if (change >= 0){
                        // betrachtet man der Fall, wenn der Wert Euro als Waehrung uebergegeben wird.
                        if (currency.equals("Euro")){
                            int [] nominalValue = {200,100,50,20,10,5,2,1};
                            //Ausgabe
                            System.out.println("Auszugebendes Wechselgeld: " + change + " Eurocent");
                            int [] result = change(change, nominalValue);
                            System.out.println("Ausgegebenes Wechselgeld: " + change + " Eurocent");
                        }else {
                            int [] nominalValue = {200,100,50,20,10,9,7,5,2,1};
                            // Ausgabe fuer Mira
                            System.out.println("Auszugebendes Wechselgeld: " + change + " Mira");
                            int [] result = change(change, nominalValue);
                            System.out.println("Ausgegebenes Wechselgeld: " + change + " Mira");
                        }
                      }else {
                        System.out.println("FEHLER: Wechselgeld darf nicht negativ sein!");
                        displayExample();
                        return;
                      }
                }else {
                    throw new Exception();
                }
            }else {
                throw new RuntimeException();
            }
        }catch (RuntimeException re){
            System.out.println("FEHLER: Falsche Parameteranzahl!");
            displayExample();
        }catch (Exception e){
          System.out.println("FEHLER: Unbekannte Waehrung " + args[0] + "!");
            displayExample();
        }
    }
  
  private static int [] change(int changeValue, int [] nominalValue){
        if (changeValue == 0){
            return new int[nominalValue.length];
        }else {
            int position = 0;
            int [] result = new int[nominalValue.length];

            while (changeValue != 0){

                if (changeValue >= nominalValue[position]){
                    if (changeValue % nominalValue[position] == 0){
                        result[position] = changeValue / nominalValue[position];
                        changeValue -= nominalValue[position] * result[position];
                        System.out.println("(" + nominalValue[position] + "," + result[position] + "," + changeValue + ")");
                        break;
}
