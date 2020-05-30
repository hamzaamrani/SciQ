package lab.progettazione.sciq.Model;


import android.os.Parcel;
import android.os.Parcelable;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;


public class Expression implements Parcelable {
    private Boolean success;
    private String query;
    private String execution_time;
    private String id;
    private ArrayList<String> plots = new ArrayList<>();
    private ArrayList<String> alternate_forms = new ArrayList<>();
    private ArrayList<String> solutions = new ArrayList<>();
    private ArrayList<String> symbolic_solutions = new ArrayList<>();
    private ArrayList<String> limits = new ArrayList<>();
    private ArrayList<String> partial_derivatives = new ArrayList<>();
    private ArrayList<String> integral = new ArrayList<>();

    public Expression(JSONObject expression) throws Exception {

        if (expression.has("success"))
            this.success = expression.getBoolean("success");
        else
            this.success = null;

        if (expression.has("query"))
            this.query = expression.getString("query");
        else
            this.query = null;

        if (expression.has("_id"))
            this.id = expression.getString("_id");
        else
            this.id = null;


        if (expression.has("execution_time"))
            this.execution_time = expression.getString("execution_time");

        if (expression.has("plots")) {
            JSONArray lista_plot = expression.getJSONArray("plots");
            for (int i = 0; i < lista_plot.length(); i++) {
                this.plots.add(lista_plot.getString(i));
            }
            System.out.println("Size of the plots is  = " + this.plots.size());
        } else
            this.plots = null;

        if (expression.has("alternate_forms")) {
            JSONArray alternate = expression.getJSONArray("alternate_forms");
            for (int i = 0; i < alternate.length(); i++) {
                this.alternate_forms.add(alternate.getString(i));
            }
        } else
            this.alternate_forms = null;

        if (expression.has("solutions")) {
            JSONArray solutions_list = expression.getJSONArray("solutions");
            for (int i = 0; i < solutions_list.length(); i++) {
                this.solutions.add(solutions_list.getString(i));
            }
        } else {
            this.solutions = null;
        }

        if (expression.has("symbolic_solutions")) {
            JSONArray symbolics = new JSONArray();
            for (int i = 0; i < symbolics.length(); i++) {
                this.symbolic_solutions.add(symbolics.getString(i));
            }
        } else
            this.symbolic_solutions = null;

        if (expression.has("limits")) {
            JSONArray limits = new JSONArray();
            for (int i = 0; i < limits.length(); i++) {
                this.limits.add(limits.getString(i));
            }
        } else
            this.limits = null;

        if (expression.has("partial_derivatives")) {
            JSONArray partial_derivatives = new JSONArray();
            for (int i = 0; i < partial_derivatives.length(); i++) {
                this.partial_derivatives.add(partial_derivatives.getString(i));
            }
        } else
            this.partial_derivatives = null;

        if (expression.has("integral")) {
            JSONArray integrals = new JSONArray();
            for (int i = 0; i < integrals.length(); i++) {
                this.integral.add(integrals.getString(i));
            }
        } else
            this.integral = null;


    }


    protected Expression(Parcel in) {
        byte tmpSuccess = in.readByte();
        success = tmpSuccess == 0 ? null : tmpSuccess == 1;
        query = in.readString();
        execution_time = in.readString();
        id = in.readString();
        plots = in.createStringArrayList();
        alternate_forms = in.createStringArrayList();
        solutions = in.createStringArrayList();
        symbolic_solutions = in.createStringArrayList();
        limits = in.createStringArrayList();
        partial_derivatives = in.createStringArrayList();
        integral = in.createStringArrayList();
    }

    public static final Creator<Expression> CREATOR = new Creator<Expression>() {
        @Override
        public Expression createFromParcel(Parcel in) {
            return new Expression(in);
        }

        @Override
        public Expression[] newArray(int size) {
            return new Expression[size];
        }
    };

    public Boolean getSuccess() {
        return success;
    }

    public String getQuery() {
        return query;
    }

    public String getExecution_time() {
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

    public String getId() {
        return id;
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeByte((byte) (success == null ? 0 : success ? 1 : 2));
        dest.writeString(query);
        dest.writeString(execution_time);
        dest.writeString(id);
        dest.writeStringList(plots);
        dest.writeStringList(alternate_forms);
        dest.writeStringList(solutions);
        dest.writeStringList(symbolic_solutions);
        dest.writeStringList(limits);
        dest.writeStringList(partial_derivatives);
        dest.writeStringList(integral);
    }

    @Override
    public String toString() {
        return "Expression{" +
                "success=" + success +
                ", query='" + query + '\'' +
                ", execution_time='" + execution_time + '\'' +
                ", id='" + id + '\'' +
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
