import java.io.*;
import java.net.*;

public class EchoClient {
    public static void main(String[] args) {
        String host = "127.0.0.1";  // Server address
        int port = 65432;           // Port number for the server

        try (Socket socket = new Socket(host, port);
             BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
             PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
             BufferedReader userInput = new BufferedReader(new InputStreamReader(System.in))) {

            System.out.println("Connected to server");

            String message;
            while (true) {
                System.out.print("Enter message to send (or 'exit' to quit): ");
                message = userInput.readLine();
                if (message.equalsIgnoreCase("exit")) {
                    break;
                }
                out.println(message);
                String response = in.readLine();
                System.out.println("Received back: " + response);
            }
        } catch (IOException e) {
            System.out.println("Client error: " + e.getMessage());
        }
    }
}
