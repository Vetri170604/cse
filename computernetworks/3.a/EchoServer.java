import java.io.*;
import java.net.*;

public class EchoServer {
    public static void main(String[] args) {
        int port = 65432;  // Port number for the server
        try (ServerSocket serverSocket = new ServerSocket(port)) {
            System.out.println("Server is listening on port " + port);

            while (true) {
                try (Socket socket = serverSocket.accept();
                     BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                     PrintWriter out = new PrintWriter(socket.getOutputStream(), true)) {

                    System.out.println("Client connected");

                    String message;
                    while ((message = in.readLine()) != null) {
                        System.out.println("Received: " + message);
                        out.println(message);  // Echo the message back to the client
                    }
                } catch (IOException e) {
                    System.out.println("Client connection error: " + e.getMessage());
                }
            }
        } catch (IOException e) {
            System.out.println("Server error: " + e.getMessage());
        }
    }
}
