package lab.progettazione.sciq.Utilities.AsyncTasks;

import android.content.Context;
import android.os.AsyncTask;

import org.json.JSONObject;

import lab.progettazione.sciq.Utilities.API.RequestHandler;
import lab.progettazione.sciq.Utilities.Interfaces.ReturnString;

public class DeleteExpression extends AsyncTask<Object, String, String> {

    private ReturnString delegate;
    private Context mContext;


    public DeleteExpression(Context context){
        this.mContext = context;
    }

    @Override
    protected String doInBackground(Object... objects) {
        String url = (String) objects[0];
        String token = (String) objects[1];
        JSONObject postDataParameters = (JSONObject) objects[2];
        try{
            return RequestHandler.sendPost(url, postDataParameters, token);
        }catch (Exception e){
            e.printStackTrace();
            return e.toString();
        }
    }

    @Override
    protected void onPostExecute(String s) {
        delegate.processFinish(s);
    }



    public void setDelegate(ReturnString delegate) {
        this.delegate = delegate;
    }
}
