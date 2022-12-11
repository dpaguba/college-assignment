/**
 * Diese Klasse fuehrt die Kommunikation mit dem Server.
 * 
 * @author Dmytro Pahuba
 * 
 */
package Client;

import java.io.*;
import java.net.*;
import java.util.Scanner;

public class Client {
    private static String serverIP;
    private static int serverPort;

    /**
     * Diese Methode startet den Client.
     * 
     * Vor dem Start des Clients muss der Server gestartet sein.
     */
    public static void main(String[] args) throws IOException {
        if(checkServerIP()){
            if(checkServerPort()){
                try{
                    Socket client = new Socket(serverIP, serverPort);
        
                    DataInputStream input = new DataInputStream(client.getInputStream());
                    DataOutputStream output = new DataOutputStream(client.getOutputStream());
                    Scanner scanner = new Scanner(System.in);

                    if(input.readUTF().equals("Darf ich TCP-Verbindung aufbauen?")){

                        output.writeUTF("Ja.");

                        if(input.readUTF().equals("Danke!")){
                            printConnectionSuccessed();

                            listen(input, output, scanner);
                        }
                    }

                    client.close();                    
                }catch(UnknownHostException | ConnectException e){
                    System.err.println("\nFehler beim Verbindungsaufbau! Es konnte keine TCP-Verbindung zum Server mit \nder IP-Adresse " + serverIP + " (Port: " + serverPort +") hergestellt werden.");
                    printClientStop();
                }catch(IOException e){
                    e.printStackTrace();
                }
            }else{
                printWrongPortError();
            }
        }else{
            printIpError();
        }

    }

     /**
     * Kommunikation mit dem Server:
     * Erhalten von Nachrichten des Servers,
     * Senden von Benutzereingaben.
     * 
     * @param input - DataInputStream zum empfangen von Nachrichten des Servers.
     * @param output - DataOutputStream zum senden von Nachrichten an den Server.
     * @param scanner - Scanner zum lesen von Benutzereingaben.
     * 
     * @throws IOException, wenn Fehler bei der Kommunikation mit dem Server auftreten
     */
    public static void listen(DataInputStream input, DataOutputStream output, Scanner scanner) throws IOException {
        while(true){
            System.out.print(input.readUTF());
            String scannedStr = scanner.nextLine();

            if(scannedStr.toUpperCase().equals("EXIT")){
                output.writeUTF(scannedStr);
                System.out.println(input.readUTF());
                printClientStop();
                break;
            }else{
                output.writeUTF(scannedStr);
                System.out.println(input.readUTF());
            }
        }
    }

    /**
    * Diese Methode überprüft, ob die vom Client eingegebene IP richtig ist.
    *
    * @throws IOException, wenn die Eingabe nicht eingelesen werden kann.
    */
    public static boolean checkServerIP() throws IOException {
        String [] listIP = {"localhost", "127.0.0.1"};

        System.out.print("IP-Adresse: ");
        try {
            String input = readInput();
            setServerIP(input);
            for (int i = 0; i < listIP.length; i++) {
                for (String string : listIP) {
                    if(string.equals(input)){
                        return true;
                    }
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return false;

    }

    /**
    * Diese Methode überprüft, ob die vom Client eingegebene IP richtig ist.
    *
    * @throws IOException, wenn die Eingabe nicht eingelesen werden kann.
    *
    * @throws NumberFormatException, wenn die Eingabe in Integer-Wert nicht umgewandelt werden kann.
    */
    public static boolean checkServerPort() throws IOException {
        System.out.print("Port: ");
        try {
            int input = Integer.parseInt(readInput());
            // serverPort = input;
            setServerPort(input);
            return 2022 == input;
        } catch (NumberFormatException e) {
            e.printStackTrace();
        }
        return false;
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
     * Diese Methode signalisiert, dass der Fehler bei dem Verbindungsaufbau aufgetreten ist.
     */
    public static void printConnectionError() {
        System.out.println("\nFehler beim Verbindungsaufbau! Es konnte keine TCP-Verbindung zum Server mit \nder IP-Adresse localhost (Port: 2022) hergestellt werden.");
        printClientStop();
    }

    /**
     * Diese Methode signalisiert, dass die falsche IP-Adresse eingegeben wurde.
     */
    public static void printIpError() {
        System.out.println("\nFalsche IP-Adresse!\nAktuell ist nur die IPv4-Adresse 127.0.0.1 und die Eingabe localhost moeglich.");
        printClientStop();
    }

    /**
     * Diese Methode signalisiert, dass der falsche Port eingegeben wurde.
     */
    public static void printWrongPortError(){
        System.err.println("\nKein korrekter Port!\nAktuell ist nur Port 2022 moeglich.\n");
        printClientStop();
    }

    /**
     * Diese Methode signalisiert, dass der Client beendet wurde.
     */
    public static void printClientStop() {
        System.out.println("\nDer Client wurde beendet.");
    }

    /**
     * Diese Methode signalisiert, dass die TCP-Verbindung aufgebaut wurde.
     */
    public static void printConnectionSuccessed() {
        System.out.println("\nEine TCP-Verbindung zum Server mit IP-Adresse " + getServerIP() + " (Port: " + getServerPort() +") wurde\nhergestellt. Sie koennen nun Ihre Anfragen an den Server stellen.");  
    }

    /**
     * Diese Methode weist den neuen Wert der IP-Adresse zu.
     * 
     * @param serverIP:String - neuer Wert für die IP-Adresse.
     */
    public static void setServerIP(String serverIP) {
        Client.serverIP = serverIP;
    }

    /**
     * Diese Methode liefert den Wert der IP-Adresse zurück.
     */
    public static String getServerIP() {
        return serverIP;
    }

    /**
     * Diese Methode weist den neuen Wert vom Port zu.
     * 
     * @param serverPort:String - neuer Wert für den Port.
     */
    public static void setServerPort(int serverPort) {
        Client.serverPort = serverPort;
    }

    /**
     * Diese Methode liefert den Wert vom Port zurück.
     */
    public static int getServerPort() {
        return serverPort;
    }
    
    
}
