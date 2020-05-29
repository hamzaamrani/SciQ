package lab.progettazione.sciq.Utilities.AsyncTasks;

import android.app.ProgressDialog;
import android.content.Context;
import android.os.AsyncTask;
import android.widget.ProgressBar;

import lab.progettazione.sciq.Utilities.API.RequestHandler;
import lab.progettazione.sciq.Utilities.Interfaces.ReturnString;

public class GetCollections extends AsyncTask<Object, String, String> {

    private Context mContext;
    private ReturnString delegate;
    private ProgressDialog progressDialog;

    public GetCollections(Context context){
        this.mContext = context;
        progressDialog = new ProgressDialog(mContext);
    }


    @Override
    protected void onPreExecute() {
        super.onPreExecute();
        progressDialog.setTitle("Retrieving collections");
        progressDialog.show();
        progressDialog.setCancelable(false);
    }



    @Override
    protected String doInBackground(Object... objects) {
        String token = (String) objects[0];
        String url = (String) objects[1];
        try{
            return RequestHandler.sendGetToken(url, token);
        }catch (Exception e ){
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
