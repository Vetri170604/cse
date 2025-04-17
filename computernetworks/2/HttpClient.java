import java.io.*;
import java.net.*;

public class HttpClient {
    public static void main(String[] args) {
        // The URL to download
        String url = "http://example.com";
        // The port for HTTP (usually 80)
        int port = 80;

        try {
            // Parse the URL
            URL parsedUrl = new URL(url);
            String host = parsedUrl.getHost();
            String path = parsedUrl.getPath().isEmpty() ? "/" : parsedUrl.getPath();

            // Create a socket connection to the server
            Socket socket = new Socket(host, port);

            // Send the HTTP GET request
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            out.println("GET " + path + " HTTP/1.1");
            out.println("Host: " + host);
            out.println("Connection: close");
            out.println(); // End of HTTP headers

            // Read the HTTP response
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            String line;
            boolean isHeader = true;
            StringBuilder content = new StringBuilder();

            while ((line = in.readLine()) != null) {
                if (isHeader) {
                    if (line.isEmpty()) {
                        isHeader = false; // End of headers
                    }
                } else {
                    content.append(line).append("\n");
                }
            }

            // Close the socket
            in.close();
            out.close();
            socket.close();

            // Save the content to a file
            try (PrintWriter fileOut = new PrintWriter(new FileWriter("downloaded_page.html"))) {
                fileOut.write(content.toString());
            }

            System.out.println("Web page downloaded and saved as 'downloaded_page.html'");
        } catch (IOException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
