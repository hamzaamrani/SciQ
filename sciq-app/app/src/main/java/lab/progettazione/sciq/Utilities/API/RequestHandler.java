package lab.progettazione.sciq.Utilities.API;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.CookieManager;
import java.net.HttpURLConnection;
import java.net.URL;

import javax.net.ssl.HttpsURLConnection;


public class RequestHandler {
    static final String COOKIES_HEADER = "Set-Cookie";
    static final String COOKIE = "Cookie";
    static CookieManager msCookieManager = new CookieManager();


    public static String sendPost(String r_url, JSONObject postDataParams, String token) throws Exception {
        URL url = new URL(r_url);

        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setReadTimeout(200000);
        conn.setConnectTimeout(200000);
        conn.setRequestMethod("POST");

        if (token != null) {
            conn.setRequestProperty("Cookie", "access_token_cookie=" + token);
            System.out.println("Token not null, equal to = " + token);
        }


        conn.setRequestProperty("Content-Type", "application/json;charset=UTF-8");
        conn.setDoInput(true);
        conn.setDoOutput(true);
        System.out.println("JSONObject within request handler" + postDataParams);
        OutputStream os = conn.getOutputStream();
        os.write(postDataParams.toString().getBytes("UTF-8"));
        os.close();

        //READING RESPONSE
        int responseCode = conn.getResponseCode(); // To Check for 200
        System.out.println(responseCode);
        if (responseCode == HttpURLConnection.HTTP_OK) {
            BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()));
            StringBuffer sb = new StringBuffer();
            String line = "";
            while ((line = in.readLine()) != null) {
                sb.append(line);
                break;
            }
            in.close();
            System.out.println("Returning " + sb.toString());
            return sb.toString();
        } else {
            String err;
            if (responseCode == 404) {
                err = "Connection Error!";
                return err;
            } else {
                if (responseCode == 429) {
                    return "Limit exceeded";
                } else {
                    err = "Connection error!";
                    return err;
                }

            }
        }
    }


    public static String sendGetToken(String url, String token) throws IOException {
        System.out.print("*************" + url + " TOKEN : " + token);
        URL obj = new URL(url);
        HttpsURLConnection con = (HttpsURLConnection) obj.openConnection();
        System.out.println(token);
        con.setRequestProperty("Cookie", "access_token_cookie=" + token);
        con.setRequestMethod("GET");
        int responseCode = con.getResponseCode();
        System.out.println(url);
        System.out.println("\nResponse Code : " + responseCode);
        if (responseCode == HttpURLConnection.HTTP_OK) { // connection ok
            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
            String inputLine;
            StringBuffer response = new StringBuffer();
            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();
            return response.toString();
        } else {
            return "Error in get request";
        }
    }
}
