package lab.progettazione.sciq.Object;

import android.widget.ExpandableListView;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonParser;

import org.json.JSONArray;
import org.json.JSONObject;

import java.lang.annotation.IncompleteAnnotationException;
import java.util.ArrayList;
import java.util.List;

public class Expression {
    private Boolean success;
    private String query;
    private double execution_time;
    private ArrayList<String> plots = new ArrayList<>();
    private ArrayList<String> alternate_forms = new ArrayList<>();
    private ArrayList<String> solutions  = new ArrayList<>();
    private ArrayList<String> symbolic_solutions = new ArrayList<>();
    private ArrayList<String> limits = new ArrayList<>();
    private ArrayList<String> partial_derivatives = new ArrayList<>();
    private ArrayList<String> integral = new ArrayList<>();

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
            JSONArray lista_plot = expression.getJSONArray("plots");
            for(int i = 0 ; i < lista_plot.length(); i ++){
                this.plots.add(lista_plot.getString(i));
            }
            System.out.println("Size of the plots is  = " + this.plots.size());
        }
        else
            this.plots = null;

        if(expression.has("alternate_forms")){
            JSONArray alternate = expression.getJSONArray("alternate_forms");
            for(int i = 0 ; i < alternate.length(); i ++){
                this.alternate_forms.add(alternate.getString(i));
            }
        }else
            this.alternate_forms = null;

        if(expression.has("solutions")){
            JSONArray solutions_list = expression.getJSONArray("solutions");
            for(int i = 0 ; i < solutions_list.length(); i ++){
                this.solutions.add(solutions_list.getString(i));
            }
        }else{
            this.solutions = null;
        }

        if(expression.has("symbolic_solutions")){
            JSONArray symbolics = new JSONArray();
            for(int i = 0 ; i < symbolics.length(); i ++){
                this.symbolic_solutions.add(symbolics.getString(i));
            }
        }else
            this.symbolic_solutions = null;

        if(expression.has("limits")){
            JSONArray limits = new JSONArray();
            for(int i  = 0; i < limits.length(); i ++){
                this.limits.add(limits.getString(i));
            }
        }else
            this.limits = null;

        if(expression.has("partial_derivatives")){
            JSONArray partial_derivatives = new JSONArray();
            for(int i  = 0 ; i < partial_derivatives.length(); i++){
                this.partial_derivatives.add(partial_derivatives.getString(i));
            }
        }else
            this.partial_derivatives = null;

        if(expression.has("integral")){
            JSONArray integrals = new JSONArray();
            for(int i  = 0 ; i < integrals.length(); i ++){
                this.integral.add(integrals.getString(i));
            }
        }else
            this.integral = null;


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
                ", alternate_forms=" + alternate_forms +
                ", solutions=" + solutions +
                ", symbolic_solutions=" + symbolic_solutions +
                ", limits=" + limits +
                ", partial_derivatives=" + partial_derivatives +
                ", integral=" + integral +
                '}';
    }
}
