package lab.progettazione.sciq.Utilities.AsyncTasks;

import android.app.ProgressDialog;
import android.content.Context;
import android.os.AsyncTask;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

import lab.progettazione.sciq.Utilities.API.MultiPartHelper;
import lab.progettazione.sciq.Utilities.Interfaces.ReturnString;

public class SendImage extends AsyncTask<Object, String, String> {

    private Context mContext;
    private ReturnString delegate;
    private ProgressDialog progressDialog;

    public SendImage(Context context) {
        this.mContext = context;
    }

    @Override
    protected void onPreExecute() {
        progressDialog = new ProgressDialog(mContext);
        progressDialog.setTitle("Elaborating image..");
        progressDialog.show();
    }

    @Override
    protected String doInBackground(Object... objects) {
        ArrayList<String> paths;
        String token;

        try {
            paths = (ArrayList<String>) objects[0];
            token = paths.get(0);
            MultiPartHelper multiPartHelper = new MultiPartHelper("https://sciq-unimib.herokuapp.com/sendfile", "UTF-8", token);
            multiPartHelper.setFilePart("file2upload", new File(paths.get(1)));
            List<String> response = multiPartHelper.getResponse();
            return response.get(0);
        } catch (Exception e) {
            e.printStackTrace();
            return e.toString();
        }

    }


    @Override
    protected void onPostExecute(String s) {
        progressDialog.dismiss();
        delegate.processFinish(s);
    }

    public void setDelegate(ReturnString delegate) {
        this.delegate = delegate;
    }
}