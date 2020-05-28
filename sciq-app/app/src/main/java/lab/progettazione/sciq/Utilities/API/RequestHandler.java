package lab.progettazione.sciq.Utilities.API;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.CookieManager;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

import javax.net.ssl.HttpsURLConnection;


public class RequestHandler {
    static final String COOKIES_HEADER = "Set-Cookie";
    static final String COOKIE = "Cookie";
    static CookieManager msCookieManager = new CookieManager();


    public static String sendPost(String r_url, JSONObject postDataParams, String token) throws Exception {
        URL url = new URL(r_url);

        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setReadTimeout(20000);
        conn.setConnectTimeout(20000);
        conn.setRequestMethod("POST");

        if(token != null){
            conn.setRequestProperty("Cookie","access_token_cookie="+token);
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
                if(responseCode == 429){
                    return "Limit exceeded";
                }else{
                    err = "Username or Password invalid";
                    return err;
                }

            }
        }
    }
}
