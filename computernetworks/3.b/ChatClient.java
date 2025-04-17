import java.io.*;
import java.net.*;
import java.util.Scanner;

public class ChatClient {
    private static final String SERVER_ADDRESS = "127.0.0.1";
    private static final int PORT = 65432;

    public static void main(String[] args) {
        try (Socket socket = new Socket(SERVER_ADDRESS, PORT);
             PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
             Scanner in = new Scanner(socket.getInputStream());
             Scanner userInput = new Scanner(System.in)) {

            System.out.println("Connected to chat server");

            // Thread to read messages from server
            new Thread(() -> {
                while (in.hasNextLine()) {
                    String serverMessage = in.nextLine();
                    System.out.println("Server: " + serverMessage);
                }
            }).start();

            // Main thread for sending messages
            while (userInput.hasNextLine()) {
                String userMessage = userInput.nextLine();
                out.println(userMessage);
            }
        } catch (IOException e) {
            System.out.println("Client error: " + e.getMessage());
        }
    }
}
