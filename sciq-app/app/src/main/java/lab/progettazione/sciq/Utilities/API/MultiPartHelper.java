package lab.progettazione.sciq.Utilities.API;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import java.util.List;

public class MultiPartHelper {
    // This class has the purpose to provide an utility to perform multipart post
    private static final String NEWLINE = "\r\n";

    private String boundaryValue;

    private HttpURLConnection cn;

    private final String charset;

    private PrintWriter printWriter;

    private OutputStream outStream;


    /*
    requestURL = URL to send the post to
    charset = Character set, default US-ASCII
     */
    public MultiPartHelper(String requestURL, String charset, String token) throws IOException {

        boundaryValue = "===" + System.currentTimeMillis() + "===";
        this.charset = charset;
        URL url = new URL(requestURL);
        cn = (HttpURLConnection) url.openConnection();
        cn.setRequestProperty("Cookie", "access_token_cookie=" + token);
        cn.setUseCaches(false);
        cn.setDoOutput(true);
        cn.setDoInput(true);
        cn.setRequestProperty("Content-Type", "multipart/form-data; boundary=" + boundaryValue);
        outStream = cn.getOutputStream();
        printWriter = new PrintWriter(new OutputStreamWriter(outStream, charset), true);
    }

    // In case the server needs particular headers, we can handle them through this method
    /*
    name = name of the header
    value = value to assign at the header specified in name
     */
    public void setHeaderField(String name, String value) {
        printWriter.append(name + ": " + value).append(NEWLINE);
        printWriter.flush();
    }


    public void setFilePart(String fieldName, File uploadFile) throws IOException {
        String fileName = uploadFile.getName();
        printWriter.append("--" + boundaryValue).append(NEWLINE);
        printWriter.append("Content-Disposition: form-data; name=\"" + fieldName + "\"; filename=\"" + fileName + "\"").append(NEWLINE);
        printWriter.append("Content-Type: " + URLConnection.guessContentTypeFromName(fileName)).append(NEWLINE);
        printWriter.append("Content-Transfer-Encoding: binary").append(NEWLINE);
        printWriter.append(NEWLINE);
        printWriter.flush();

        FileInputStream inputStream = new FileInputStream(uploadFile);
        byte[] buffer = new byte[4096];
        int bytesRead = -1;
        while ((bytesRead = inputStream.read(buffer)) != -1) {
            outStream.write(buffer, 0, bytesRead);
        }
        outStream.flush();
        inputStream.close();

        printWriter.append(NEWLINE);
        printWriter.flush();
    }

    public void setFormField(String name, String value) {
        printWriter.append("--" + boundaryValue).append(NEWLINE);
        printWriter.append("Content-Disposition: form-data; name=\"" + name + "\"").append(NEWLINE);
        printWriter.append("Content-Type: text/plain; charset=" + charset).append(NEWLINE);
        printWriter.append(NEWLINE);
        printWriter.append(value).append(NEWLINE);
        printWriter.flush();
    }

    public void setFormField(String name, JSONObject value) {
        String object;
        object = value.toString();
        printWriter.append("--" + boundaryValue).append(NEWLINE);
        printWriter.append("Content-Disposition: form-data; name=\"" + name + "\"").append(NEWLINE);
        printWriter.append("Content-Type: text/plain; charset=" + charset).append(NEWLINE);
        printWriter.append(NEWLINE);
        printWriter.append(object).append(NEWLINE);
        printWriter.flush();
    }

    public List<String> getResponse() throws IOException {
        List<String> response = new ArrayList<String>();

        printWriter.append(NEWLINE).flush();
        printWriter.append("--" + boundaryValue + "--").append(NEWLINE);
        printWriter.close();

        // checks server's status code first
        int status = cn.getResponseCode();
        if (status == HttpURLConnection.HTTP_OK) {
            BufferedReader reader = new BufferedReader(new InputStreamReader(cn.getInputStream()));
            String line = null;
            while ((line = reader.readLine()) != null) {
                response.add(line);
            }
            reader.close();
            cn.disconnect();
        } else {
            throw new IOException("Server status: " + status);
        }

        return response;
    }
}
