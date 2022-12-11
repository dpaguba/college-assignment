package Server;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.HttpURLConnection;
import java.net.Socket;
import java.net.URL;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;

public class ClientInterface extends Thread {

    // private Socket client;
    private DataInputStream input;
    private DataOutputStream output;
    // private SocketAddress clientAddress;
    


    public ClientInterface(Socket client){
        
        

        // this.client = client;
        try{
            this.input = new DataInputStream(client.getInputStream());
            this.output = new DataOutputStream(client.getOutputStream());
            // this.clientAddress = client.getRemoteSocketAddress();

            this.output.writeUTF("Darf ich TCP-Verbindung aufbauen?");
            
            if(this.input.readUTF().equals("Ja.")){
                this.output.writeUTF("Danke!");
            }else{
                System.out.println("Fehler beim Verbindungsaufbau!");
            }
        }catch(IOException e){
            System.err.println("Fehler beim Verbindungsaufbau!");
        }
    }

    public void run() {
        ArrayList<String> commands = new ArrayList<String>();
        commands.add("ECHO");
        commands.add("HISTORY");
        commands.add("PING");
        commands.add("GET");
        commands.add("HOLIDAYS");
        commands.add("EXIT");
        ArrayList<String> commandHistoryList = new ArrayList<String>();

        try {
            while(true){

                output.writeUTF("\n$ ");
                String userInput = input.readUTF();

                if(userInput.toUpperCase().startsWith("CURRENT")){
                    if(userInput.toUpperCase().equals("CURRENT TIME")){
                        commandHistoryList.add(userInput.toUpperCase());
                        output.writeUTF(getCurrentTime());
                    } else if(userInput.toUpperCase().equals("CURRENT DATE")){
                        commandHistoryList.add(userInput.toUpperCase());
                        output.writeUTF(getCurrentDate());
                    }else{
                        output.writeUTF(print400Error());
                    }
                }else if(userInput.toUpperCase().startsWith("LATEST")){
                    if(userInput.toUpperCase().equals("LATEST NEWS")){
                        commandHistoryList.add(userInput.toUpperCase());
                        output.writeUTF(getLatestNews());
                    }else{
                        output.writeUTF(print400Error());
                    }
                }else{
                    String [] strings = userInput.split(" ");

                    if(checkIfCommand(commands, strings[0].toUpperCase())){
                        if(userInput.toUpperCase().startsWith("ECHO")){
                            commandHistoryList.add(strings[0].toUpperCase());
                            output.writeUTF(getEcho(strings));
                        }
                        
                        if(userInput.toUpperCase().equals("PING")){
                            commandHistoryList.add(userInput.toUpperCase());
                            output.writeUTF("PONG");
                        }
                        
                        if(userInput.toUpperCase().startsWith("HISTORY")){
                            commandHistoryList.add(strings[0].toUpperCase());
                            if(strings.length == 1){
                                output.writeUTF(getHistory(commandHistoryList, null));
                            }else{
                                try {
                                    int length = Integer.parseInt(strings[1]);
                                    output.writeUTF(getHistory(commandHistoryList, length));
                                } catch (Exception e) {
                                    output.writeUTF(print400Error());
                                }
                                
                            }
                        }

                        if(userInput.toUpperCase().startsWith("HOLIDAYS")){
                            commandHistoryList.add(strings[0].toUpperCase());
                            try {
                                int year = Integer.parseInt(strings[1]);
                                output.writeUTF(getHolidays(year));
                            } catch (Exception e) {
                                output.writeUTF(print400Error());
                            }
                        }

                        if(userInput.toUpperCase().startsWith("GET")){
                            /* 
                            0 - get
                            1 - host
                            2 - path
                            */ 
                            commandHistoryList.add(strings[0].toUpperCase());
                            if(strings.length == 2){
                                output.writeUTF(getRequestResponse(strings[1], "/"));
                            }else if(strings.length == 3){
                                if(strings[2].startsWith("/")){
                                    output.writeUTF(getRequestResponse(strings[1], strings[2]));
                                }else{
                                    output.writeUTF(print500Error());
                                }
                            }else{
                                output.writeUTF(print500Error());
                            }
                            
                        }

                        if(userInput.toUpperCase().equals("EXIT")){
                            output.writeUTF("Die Verbindung zum Server wurde beendet.");
                        }
                    }else{
                        output.writeUTF(print400Error());
                    }

                }                
                
            }
        } catch (IOException e) {
            // this exception occurs each time if client disconnects
            
        }
    }

    public static String getCurrentTime() {
        DateFormat dateFormat = new SimpleDateFormat("HH:mm:ss");
        Calendar cal = Calendar.getInstance();
        return dateFormat.format(cal.getTime());
    }

    public static String getCurrentDate() {
        DateFormat dateFormat = new SimpleDateFormat("dd.MM.yyyy");
        Calendar cal = Calendar.getInstance();
        return dateFormat.format(cal.getTime());
    }

    public static String getHistory(ArrayList<String> list, int... num) {
        // TODO: handle exceptions like Arraysindexoutofbound

        if(list.isEmpty() || (num != null && num[0] < 1)){

            return print400Error();
        }else{
            String history = "";
            if(num == null || num[0] == list.size()){
                for (int i = 0; i < list.size() - 1; i++) {
                    history += (i == list.size() - 2) ? list.get(i).toUpperCase() : list.get(i).toUpperCase() + "\n";
                }
            }else{
                if(num[0] < list.size()){
                    for (int i = list.size() - num[0] - 1; i < list.size() - 1; i++) {
                        history += (i == list.size() - 2) ? list.get(i).toUpperCase() : list.get(i).toUpperCase() + "\n";
                    }
                }else{
                    return print400Error();
                }
                
            }
            return history;
        }
        
        
    }

   
    public static String getEcho(String [] strings) {
        String str = "";
        for (int i = 1; i < strings.length; i++) {
            str += (i == strings.length - 1) ? strings[i] : strings[i] + " " ;
        }
        
        return str.trim();
    }

    public static boolean checkIfCommand(ArrayList<String> commands, String userInput) {
        for (String string : commands) {
            if(string.equals(userInput)){
                return true;
            }
        }
        return false;
    }

    public static String getRequestResponse(String host, String path) throws IOException{

        try (Socket socket = new Socket(host, 80)) {
            PrintWriter wtr = new PrintWriter(socket.getOutputStream());

            // create GET request
            if(path.equals("/")){
                wtr.print("GET / HTTP/1.1\r\n");
            }else{
                wtr.print("GET " + path + " HTTP/1.1\r\n");
            }
            
            wtr.print("Host: " + host + "\r\n");
            wtr.print("\r\n");
            wtr.flush();
            socket.shutdownOutput();

            String str = "";
            String outstr;
            
            BufferedReader bufRead = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            while ((outstr = bufRead.readLine()) != null) {
                str += outstr + "\n";
            }
            
            socket.shutdownInput();

            return str;
        }catch(Exception e){
            return print400Error();
        }
        
    }

    public static String getLatestNews() {
        
        BufferedReader reader;
        String line;
        StringBuffer responseContent = new StringBuffer();
        try {
            HttpURLConnection connection;
            URL url = new URL("https://www.tagesschau.de/api2/");
            connection = (HttpURLConnection) url.openConnection();

            // Request setup
            connection.setRequestMethod("GET");
            connection.setConnectTimeout(5000);
            connection.setReadTimeout(5000);

            int status = connection.getResponseCode();

            if(status > 299){
                reader = new BufferedReader(new InputStreamReader(connection.getErrorStream()));
                while((line = reader.readLine()) != null){
                    responseContent.append(line);
                }
                reader.close();
            }else{
                int lineQuantity = 0;
                reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                while((line = reader.readLine()) != null && lineQuantity  < 100){
                    responseContent.append(line);
                    lineQuantity++;
                }
                reader.close();
            }
            connection.disconnect();
            return responseContent.toString() + "\n\nWenn Sie mehr Nachrichten lesen möchten, können Sie folgenden Link in Ihrem Browser aufrufen:\nhttps://www.tagesschau.de/api2/";
        } catch (IOException e) {
            e.printStackTrace();
        }
        return "";
        
    }

    public static String getHolidays(int year) {
        BufferedReader reader;
        String line;
        StringBuffer responseContent = new StringBuffer();
        try {
            HttpURLConnection connection;
            URL url = new URL("https://feiertage-api.de/api/?jahr=" + year + "&nur_land=NW");
            connection = (HttpURLConnection) url.openConnection();

            // Request setup
            connection.setRequestMethod("GET");
            connection.setConnectTimeout(5000);
            connection.setReadTimeout(5000);

            int status = connection.getResponseCode();

            if(status > 299){
                reader = new BufferedReader(new InputStreamReader(connection.getErrorStream()));
                while((line = reader.readLine()) != null){
                    responseContent.append(line);
                }
                reader.close();
            }else{
                int lineQuantity = 0;
                reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                while((line = reader.readLine()) != null && lineQuantity  < 100){
                    responseContent.append(line);
                    lineQuantity++;
                }
                reader.close();
            }
            connection.disconnect();
            return responseContent.toString();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return "";
        
    }

    public static String print400Error() {
        return "400 BAD REQUEST";
    }

    public static String print500Error() {
        return "500 INTERNAL SERVER ERROR";
    }


}
