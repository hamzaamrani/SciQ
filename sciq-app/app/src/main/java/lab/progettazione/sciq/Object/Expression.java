package lab.progettazione.sciq.Object;

import android.widget.ExpandableListView;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonParser;

import org.json.JSONArray;
import org.json.JSONObject;

import java.lang.annotation.IncompleteAnnotationException;
import java.util.ArrayList;

public class Expression {
    private Boolean success;
    private String query;
    private double execution_time;
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

        if(expression.has("query"))
            this.query = expression.getString("query");
        else
            this.query = null;

        if(expression.has("execution_time"))
            this.execution_time = (double) expression.get("execution_time");

        if(expression.has("plots")){


            int i;
            for(i = 0; i < plots.size(); i ++){
                this.plots.add(plots.get(i).toString());
            }
            System.out.println("There are " + i + "plots");
        }
        else
            this.plots = null;

    }

    public Boolean getSuccess() {
        return success;
    }

    public String getQuery() {
        return query;
    }

    public double getExecution_time() {
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

    @Override
    public String toString() {
        return "Expression{" +
                "success=" + success +
                ", query='" + query + '\'' +
                ", execution_time=" + execution_time +
                ", plots=" + plots +
                ", alternate_forms=" + alternate_forms +
                ", solutions=" + solutions +
                ", symbolic_solutions=" + symbolic_solutions +
                ", limits=" + limits +
                ", partial_derivatives=" + partial_derivatives +
                ", integral=" + integral +
                '}';
    }
}
