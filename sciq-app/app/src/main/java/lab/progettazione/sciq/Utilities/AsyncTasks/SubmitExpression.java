package lab.progettazione.sciq.Utilities.AsyncTasks;

import android.app.ProgressDialog;
import android.content.Context;
import android.os.AsyncTask;
import android.view.View;
import android.widget.ProgressBar;

import org.json.JSONObject;

import lab.progettazione.sciq.Object.Expression;
import lab.progettazione.sciq.Utilities.API.RequestHandler;
import lab.progettazione.sciq.Utilities.Interfaces.ExpressionInterface;

public class SubmitExpression extends AsyncTask<Object, String, String> {

    public ExpressionInterface delegate = null;
    private Context mContext;
    private ProgressBar progressBar;


    public SubmitExpression(Context context, ProgressBar progressBar){
        this.mContext = context;
        this.progressBar = progressBar;
    }

    @Override
    protected void onPreExecute() {
        progressBar.setVisibility(View.VISIBLE);
    }


    @Override
    protected String doInBackground(Object... objects) {
        String token = (String) objects[0];
        String expression = (String) objects[1];

        JSONObject postDataParameters = new JSONObject();
        try{
            postDataParameters.put("symbolic_expression", expression);
        }catch (Exception e){
            e.printStackTrace();
        }
        String endpoint = "/submit_expression";
        String url = "https://sciq-unimib-dev.herokuapp.com" + endpoint;
        try{
            return RequestHandler.sendPost(url, postDataParameters, token);
        }catch (Exception e){
            return e.toString();
        }
    }


    @Override
    protected void onPostExecute(String s) {
        //System.out.print("Returned " + s);
        progressBar.setVisibility(View.GONE);
        boolean success;
        try{
            JSONObject response = new JSONObject(s);
            if(response.has("success")){
                success = response.getBoolean("success");
                if(success){
                    Expression response_exp = new Expression(response);
                    System.out.println("Success =  " + response_exp.getSuccess());
                    delegate.onExpressionSuccessful(response_exp);
                }else
                    delegate.onExpressionFailure("Success false");
            }else
                delegate.onExpressionFailure("Connection error");

        }catch (Exception e){
            e.printStackTrace();
        }
    }
}
