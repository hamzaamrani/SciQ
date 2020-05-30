package lab.progettazione.sciq.Utilities.AsyncTasks;

import android.app.ProgressDialog;
import android.content.Context;
import android.os.AsyncTask;

import org.json.JSONObject;

import lab.progettazione.sciq.Utilities.API.RequestHandler;
import lab.progettazione.sciq.Utilities.Interfaces.ReturnString;

public class LoginPostAsyncTask extends AsyncTask<Object, String, String> {

    Context context;
    ProgressDialog progressDialog;
    public ReturnString delegate;

    public LoginPostAsyncTask(Context context) {
        this.context = context;
        progressDialog = new ProgressDialog(context);
        progressDialog.setCancelable(false);

    }

    @Override
    protected void onPreExecute() {
        super.onPreExecute();
        progressDialog.setMessage("Connecting...");
        progressDialog.show();
    }

    @Override
    protected String doInBackground(Object... objects) {
        String url = (String) objects[0];
        JSONObject postDataParameters = (JSONObject) objects[1];
        try {
            return RequestHandler.sendPost(url, postDataParameters, null);
        } catch (Exception e) {
            e.printStackTrace();
            return ("Exception: " + e.getMessage());
        }
    }

    @Override
    protected void onPostExecute(String s) {
        progressDialog.dismiss();
        delegate.processFinish(s);
    }
}
