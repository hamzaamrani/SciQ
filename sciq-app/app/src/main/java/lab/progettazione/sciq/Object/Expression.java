package lab.progettazione.sciq.Object;

import android.widget.ExpandableListView;

import org.json.JSONArray;
import org.json.JSONObject;

import java.lang.annotation.IncompleteAnnotationException;
import java.util.ArrayList;

public class Expression {
    private Boolean success;
    private String query;
    private float execution_time;
    private ArrayList<String> plots;
    private ArrayList<String> alternate_forms;
    private ArrayList<String> solutions;
    private ArrayList<String> symbolic_solutions;
    private ArrayList<String> limits;
    private ArrayList<String> partial_derivatives;
    private ArrayList<String> integral;

    public Expression(JSONObject expression) throws Exception{

        if(expression.has("success"))
            this.success = expression.getBoolean("success");
        else
            this.success = null;

        /*if(expression.has("query"))
            this.query = expression.getString("query");
        else
            this.query = null;

        if(expression.has("execution_time"))
            this.execution_time = (float) expression.get("execution_time");

        if(expression.has("plots"))
            this.plots = (ArrayList<String>) expression.get("plots");
        else
            this.plots = null;*/

    }

    public Boolean getSuccess() {
        return success;
    }

    public String getQuery() {
        return query;
    }

    public float getExecution_time() {
        return execution_time;
    }

    public ArrayList<String> getPlots() {
        return plots;
    }

    public ArrayList<String> getAlternate_forms() {
        return alternate_forms;
    }

    public ArrayList<String> getSolutions() {
        return solutions;
    }

    public ArrayList<String> getSymbolic_solutions() {
        return symbolic_solutions;
    }

    public ArrayList<String> getLimits() {
        return limits;
    }

    public ArrayList<String> getPartial_derivatives() {
        return partial_derivatives;
    }

    public ArrayList<String> getIntegral() {
        return integral;
    }
}
