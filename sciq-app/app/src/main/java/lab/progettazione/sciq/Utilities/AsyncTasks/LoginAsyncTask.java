package lab.progettazione.sciq.Utilities.AsyncTasks;

import android.app.ProgressDialog;
import android.content.Context;
import android.os.AsyncTask;

import lab.progettazione.sciq.API.RequestHandler;
import lab.progettazione.sciq.Utilities.Interfaces.ReturnString;

import org.json.JSONObject;

public class LoginAsyncTask extends AsyncTask<Object, String, String> {

    private Context mContext;
    private ProgressDialog progressBar;
    public ReturnString delegate;

    public LoginAsyncTask(Context context) {
        this.mContext = context;
        progressBar = new ProgressDialog(mContext);
        progressBar.setCancelable(false);
    }

    @Override
    protected void onPreExecute() {
        super.onPreExecute();
        progressBar.setMessage("Connecting...");
        progressBar.show();

    }

    @Override
    protected String doInBackground(Object... objects) {
        String url = (String) objects[0];
        JSONObject postDataParameters = (JSONObject) objects[1];
        try {
            return RequestHandler.sendPost(url, postDataParameters);
        } catch (Exception e) {
            e.printStackTrace();
            return ("Exception: " + e.getMessage());
        }
    }

    @Override
    protected void onPostExecute(String s) {
        JSONObject response = null;
        progressBar.dismiss();
        if (s != null) {
            try {
                response = new JSONObject(s);
            } catch (Exception e) {
                e.printStackTrace();
            }
            if (response != null && response.has("results")) {
                delegate.processFinish("User created! You can login now");
            } else {
                String error = "Error! ";
                try {
                    error += response.getString("error");
                } catch (Exception e) {
                    e.printStackTrace();
                }
                delegate.processFinish(error);
            }
        } else
            delegate.processFinish("Connection error");
    }
}
