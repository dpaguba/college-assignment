/**
 * Diese Klasse startet den Server und verbindet die Clients mit der App
 * 
 * @author Dmytro Pahuba
 * 
 */
package Server;

import java.io.*;
import java.net.*;



/**
 * Diese Klasse startet den Server und verbindet neue Clients mit der Anwendung.
 */
public class Server{
    /**
    * Port des Servers, mit dem die Clients kommunizieren.
    */
    private static int port;


    /**
     * Der Server wird gestartet.
     */
    public static void main(String[] args) throws IOException {
        if(checkPort()){
            try{
                runServer();
            }catch(IOException e){
                e.printStackTrace();
            }
        }else{
            printWrongPort();
        }   
    }

    
    /**
     * Der Server wird auf dem angegebenen Port gestartet.
     * 
     * @throws IOException, wenn die Probleme mit dem Server auftauchen.
     */
    public static void runServer() throws IOException {
        ServerSocket server = new ServerSocket(port);
        connectClients(server);         
        
    }


    /**
     * Die neuen Clients werden mit dem Server verbunden.
     * 
     * @param server:ServerSocket
     * 
     * @throws IOException, wenn die Fehler bei dem Verbindungsaufbau mit Clients auftreten.
     */

    public static void connectClients(ServerSocket server) throws IOException {    
        System.out.print("\nDer Server wurde gestartet und wartet am Port 2022 auf Anfragen vom Client.\nWenn Sie den Server beenden wollen, dann geben Sie 'J' ein: ");
        
        while(true){
            Socket client = server.accept();

            ClientInterface newClientInterface = new ClientInterface(client);
            newClientInterface.start();
        } 

        
        
    }

    
    /**
     * Diese Methode liest die Eingabe ein.
     * 
     * @throws IOException, wenn die Eingabe nicht eingelesen werden kann. 
     */
    public static String readInput() throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        String name = reader.readLine();
        return name;
    }

    /**
    * Diese Methode überprüft, ob der vom Client eingegebene Port richtig ist.
    *
    * @throws IOException, wenn die Eingabe nicht eingelesen werden kann.
    *
    * @throws NumberFormatException, wenn die Eingabe in Integer-Wert nicht umgewandelt werden kann.
    */
    public static boolean checkPort() throws NumberFormatException, IOException{
        System.out.print("Port: ");
        try{
            port = Integer.parseInt(readInput());
        }catch(NumberFormatException e){
            e.printStackTrace();
        }
        return port == 2022;
    }

    /**
     * Diese Methode teilt den Text der Fehlermeldung für besseres Verständnis mit.
     */
    public static void printWrongPort(){
        System.err.println("\nKein korrekter Port!\nAktuell ist nur Port 2022 moeglich.\n");
        printStoppedServer();
    }

    /**
     * Diese Methode signalisiert, dass der Server beendet wurde.
     */
    public static void printStoppedServer() {
        System.out.println("\nDer Server wurde beendet.");
    }

}