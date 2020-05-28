package lab.progettazione.sciq.Activities;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.RecyclerView;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.MenuItem;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import com.google.android.flexbox.AlignItems;
import com.google.android.flexbox.FlexDirection;
import com.google.android.flexbox.FlexWrap;
import com.google.android.flexbox.FlexboxLayoutManager;
import com.google.android.flexbox.JustifyContent;
import com.progettazione.sciq.R;

import java.text.Normalizer;

import io.github.kexanie.library.MathView;
import lab.progettazione.sciq.Model.Expression;
import lab.progettazione.sciq.Utilities.Adapter.FormulaListAdapter;
import lab.progettazione.sciq.Utilities.Adapter.PlotListAdapter;

import static java.lang.String.valueOf;

public class ShowResults extends AppCompatActivity {

    private Expression current_expression;
    private MathView latex_query;
    private TextView execution_response;
    private TextView execution_time;

    private static String latex_delimiter_start = "\\(";
    private static String latex_delimiter_end = "\\)";

    private PlotListAdapter plotListAdapter;
    private RecyclerView lista_plots;
    private ImageView expand_plots;
    private TextView no_plots;

    private FormulaListAdapter solutionsAdapter;
    private ImageView expand_solutions;
    private RecyclerView lista_solutions;
    private TextView no_solution;

    private FormulaListAdapter symbolicSolutionAdapter;
    private ImageView expand_symbolic_solutions;
    private RecyclerView  lista_symbolic_solutions;
    private TextView no_symbolic_solutions;


    private FormulaListAdapter limitAdapter;
    private ImageView expand_limits;
    private RecyclerView lista_limits;
    private TextView no_limits;


    private FormulaListAdapter partialDerivativesAdapter;
    private ImageView expand_partial_derivatives;
    private RecyclerView lista_partial_derivatives;
    private TextView no_partial_derivatives;

    private FormulaListAdapter integralAdapter;
    private ImageView expand_integral;
    private RecyclerView lista_integral;
    private TextView no_integral;

    private Boolean plot_expanded = false;
    private Boolean solution_expanded = false;
    private Boolean symbolic_solution_expanded = false;
    private Boolean limit_expanded = false;
    private Boolean partial_derivative_expanded = false;
    private Boolean integral_expanded = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_show_results);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        getSupportActionBar().setDisplayShowHomeEnabled(true);
        getSupportActionBar().setTitle("Results");

        Intent i = getIntent();
        current_expression = i.getParcelableExtra("Expression");

        latex_query = findViewById(R.id.latex_query);
        execution_response = findViewById(R.id.execution_response);
        execution_time = findViewById(R.id.execution_time);

        lista_plots = findViewById(R.id.lista_plots);
        expand_plots = findViewById(R.id.expand_plots);
        no_plots = findViewById(R.id.no_plots);

        expand_solutions = findViewById(R.id.expand_solutions);
        lista_solutions = findViewById(R.id.lista_solutions);
        no_solution = findViewById(R.id.no_solution);

        expand_symbolic_solutions = findViewById(R.id.expand_symbolic_solutions);
        lista_symbolic_solutions = findViewById(R.id.lista_symbolic_solutions);
        no_symbolic_solutions = findViewById(R.id.no_symbolic_solution);

        expand_limits = findViewById(R.id.expand_limits);
        lista_limits = findViewById(R.id.lista_limits);
        no_limits = findViewById(R.id.no_limits);

        expand_partial_derivatives = findViewById(R.id.expand_partial_derivatives);
        lista_partial_derivatives = findViewById(R.id.lista_partial_derivatives);
        no_partial_derivatives = findViewById(R.id.no_partial_derivatives);

        expand_integral = findViewById(R.id.expand_integral);
        lista_integral = findViewById(R.id.lista_integral);
        no_integral = findViewById(R.id.no_integral);

        latex_query.setText(latex_delimiter_start + current_expression.getQuery() + latex_delimiter_end);
        execution_response.setText(valueOf(current_expression.getSuccess()).toUpperCase());
        execution_time.setText(current_expression.getExecution_time());




        //If there are integral
        if(current_expression != null && current_expression.getIntegral() != null){
            integralAdapter = new FormulaListAdapter(this, current_expression.getIntegral());
            FlexboxLayoutManager layoutManager = new FlexboxLayoutManager(getApplicationContext());
            layoutManager.setFlexDirection(FlexDirection.ROW);
            layoutManager.setJustifyContent(JustifyContent.SPACE_AROUND);
            layoutManager.setFlexWrap(FlexWrap.WRAP);
            layoutManager.setAlignItems(AlignItems.FLEX_START);
            lista_integral.setLayoutManager(layoutManager);
            lista_integral.setAdapter(integralAdapter);
        }

        //If there are partial_derivatives
        if(current_expression != null && current_expression.getPartial_derivatives() != null){
            partialDerivativesAdapter = new FormulaListAdapter(this, current_expression.getPartial_derivatives());
            FlexboxLayoutManager layoutManager = new FlexboxLayoutManager(getApplicationContext());
            layoutManager.setFlexDirection(FlexDirection.ROW);
            layoutManager.setJustifyContent(JustifyContent.SPACE_AROUND);
            layoutManager.setFlexWrap(FlexWrap.WRAP);
            layoutManager.setAlignItems(AlignItems.FLEX_START);
            lista_partial_derivatives.setLayoutManager(layoutManager);
            lista_partial_derivatives.setAdapter(partialDerivativesAdapter);
        }

        //If there are limits
        if(current_expression != null && current_expression.getLimits() != null){
            limitAdapter = new FormulaListAdapter(this, current_expression.getLimits());
            FlexboxLayoutManager layoutManager = new FlexboxLayoutManager(getApplicationContext());
            layoutManager.setFlexDirection(FlexDirection.ROW);
            layoutManager.setJustifyContent(JustifyContent.SPACE_AROUND);
            layoutManager.setFlexWrap(FlexWrap.WRAP);
            layoutManager.setAlignItems(AlignItems.FLEX_START);
            lista_limits.setLayoutManager(layoutManager);
            lista_limits.setAdapter(limitAdapter);
        }

        //If there are symbolic solutions
        if(current_expression != null && current_expression.getSymbolic_solutions() != null){
            symbolicSolutionAdapter = new FormulaListAdapter(this, current_expression.getSymbolic_solutions());
            FlexboxLayoutManager layoutManager = new FlexboxLayoutManager(getApplicationContext());
            layoutManager.setFlexDirection(FlexDirection.ROW);
            layoutManager.setJustifyContent(JustifyContent.SPACE_AROUND);
            layoutManager.setFlexWrap(FlexWrap.WRAP);
            layoutManager.setAlignItems(AlignItems.FLEX_START);
            lista_symbolic_solutions.setLayoutManager(layoutManager);
            lista_symbolic_solutions.setAdapter(symbolicSolutionAdapter);
        }

        //If there are solutions
        if(current_expression !=  null && current_expression.getSolutions() != null){
            solutionsAdapter = new FormulaListAdapter(this, current_expression.getSolutions());
            FlexboxLayoutManager layoutManager = new FlexboxLayoutManager(getApplicationContext());
            layoutManager.setFlexDirection(FlexDirection.ROW);
            layoutManager.setJustifyContent(JustifyContent.SPACE_AROUND);
            layoutManager.setFlexWrap(FlexWrap.WRAP);
            layoutManager.setAlignItems(AlignItems.FLEX_START);
            lista_solutions.setLayoutManager(layoutManager);
            lista_solutions.setAdapter(solutionsAdapter);
        }

        // If there are plots!
        if(current_expression != null && current_expression.getPlots() != null){
            plotListAdapter = new PlotListAdapter(this, current_expression.getPlots());
            FlexboxLayoutManager layoutManager = new FlexboxLayoutManager(getApplicationContext());
            layoutManager.setFlexDirection(FlexDirection.ROW);
            layoutManager.setJustifyContent(JustifyContent.SPACE_AROUND);
            layoutManager.setFlexWrap(FlexWrap.WRAP);
            layoutManager.setAlignItems(AlignItems.FLEX_START);
            lista_plots.setLayoutManager(layoutManager);
            lista_plots.setAdapter(plotListAdapter);
        }


        expand_integral.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(integral_expanded){
                    if(current_expression.getIntegral() != null && current_expression.getIntegral().size()>0){
                        lista_integral.setVisibility(View.GONE);
                    }else{
                        no_integral.setVisibility(View.GONE);
                    }
                    integral_expanded = false;
                    expand_integral.setImageDrawable(getDrawable(R.drawable.ic_arrow_drop_down_24dp));
                }else{
                    if(current_expression.getIntegral()!= null && current_expression.getIntegral().size() > 0){
                        lista_integral.setVisibility(View.VISIBLE);
                        Log.d("Integral", "There are integral =  " + current_expression.getIntegral().size());
                    }else{
                        no_integral.setVisibility(View.VISIBLE);
                        Log.d("Integral", "There are not integral");
                    }
                    integral_expanded = true;
                    expand_integral.setImageDrawable(getDrawable(R.drawable.ic_arrow_drop_up_24dp));
                }
            }
        });


        expand_partial_derivatives.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(partial_derivative_expanded){
                    if(current_expression.getPartial_derivatives() != null && current_expression.getPartial_derivatives().size()>0){
                        lista_partial_derivatives.setVisibility(View.GONE);
                    }else{
                        no_partial_derivatives.setVisibility(View.GONE);
                    }
                    partial_derivative_expanded = false;
                    expand_partial_derivatives.setImageDrawable(getDrawable(R.drawable.ic_arrow_drop_down_24dp));
                }else{
                    if(current_expression.getPartial_derivatives()!= null && current_expression.getPartial_derivatives().size() > 0){
                        lista_partial_derivatives.setVisibility(View.VISIBLE);
                        Log.d("Partial Derivatives", "There are partial derivatives =  " + current_expression.getPartial_derivatives().size());
                    }else{
                        no_partial_derivatives.setVisibility(View.VISIBLE);
                        Log.d("Partial Derivatives", "There are not partial derivatives");
                    }
                    partial_derivative_expanded = true;
                    expand_partial_derivatives.setImageDrawable(getDrawable(R.drawable.ic_arrow_drop_up_24dp));
                }
            }
        });

        expand_limits.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(limit_expanded){
                    if(current_expression.getLimits() != null && current_expression.getLimits().size()>0){
                        lista_limits.setVisibility(View.GONE);
                    }else{
                        no_limits.setVisibility(View.GONE);
                    }
                    limit_expanded = false;
                    expand_limits.setImageDrawable(getDrawable(R.drawable.ic_arrow_drop_down_24dp));
                }else{
                    if(current_expression.getLimits()!= null && current_expression.getLimits().size() > 0){
                        lista_limits.setVisibility(View.VISIBLE);
                        Log.d("Limits", "There are limits =  " + current_expression.getLimits().size());
                    }else{
                        no_limits.setVisibility(View.VISIBLE);
                        Log.d("Limits", "There are not limits");
                    }
                    limit_expanded = true;
                    expand_limits.setImageDrawable(getDrawable(R.drawable.ic_arrow_drop_up_24dp));
                }
            }
        });

        expand_symbolic_solutions.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(symbolic_solution_expanded){
                    if(current_expression.getSymbolic_solutions() != null && current_expression.getSymbolic_solutions().size()>0){
                        lista_symbolic_solutions.setVisibility(View.GONE);
                    }else{
                        no_symbolic_solutions.setVisibility(View.GONE);
                    }
                    symbolic_solution_expanded = false;
                    expand_symbolic_solutions.setImageDrawable(getDrawable(R.drawable.ic_arrow_drop_down_24dp));
                }else{
                    if(current_expression.getSymbolic_solutions()!= null && current_expression.getSymbolic_solutions().size() > 0){
                        lista_symbolic_solutions.setVisibility(View.VISIBLE);
                        Log.d("Symbolic Solutions", "There are symb solutions =  " + current_expression.getSymbolic_solutions().size());
                    }else{
                        no_symbolic_solutions.setVisibility(View.VISIBLE);
                        Log.d("Symbolic Solutions", "There are not symb solutions");
                    }
                    symbolic_solution_expanded = true;
                    expand_symbolic_solutions.setImageDrawable(getDrawable(R.drawable.ic_arrow_drop_up_24dp));
                }
            }
        });

        expand_solutions.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(solution_expanded){
                    if(current_expression.getSolutions() != null && current_expression.getSolutions().size()>0){
                        lista_solutions.setVisibility(View.GONE);
                    }else{
                        no_solution.setVisibility(View.GONE);
                    }
                    solution_expanded = false;
                    expand_solutions.setImageDrawable(getDrawable(R.drawable.ic_arrow_drop_down_24dp));
                }else{
                    if(current_expression.getSolutions()!= null && current_expression.getSolutions().size() > 0){
                        lista_solutions.setVisibility(View.VISIBLE);
                        Log.d("Solutions", "There are solutions =  " + current_expression.getSolutions().size());
                    }else{
                        no_solution.setVisibility(View.VISIBLE);
                        Log.d("Solutions", "There are not solutions");
                    }
                    solution_expanded = true;
                    expand_solutions.setImageDrawable(getDrawable(R.drawable.ic_arrow_drop_up_24dp));
                }
            }
        });

        expand_plots.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(plot_expanded){
                    if(current_expression.getPlots() != null && current_expression.getPlots().size() > 0){
                        lista_plots.setVisibility(View.GONE);
                    }else{
                        no_plots.setVisibility(View.GONE);
                    }
                    plot_expanded = false;
                    expand_plots.setImageDrawable(getDrawable(R.drawable.ic_arrow_drop_down_24dp));
                }else{
                    if(current_expression.getPlots() != null && current_expression.getPlots().size() > 0){
                        Log.d("Plot", "There are plot =  " + current_expression.getPlots().size());
                        lista_plots.setVisibility(View.VISIBLE);
                    }else{
                        Log.d("Plot", "No plot to show");
                        no_plots.setVisibility(View.VISIBLE);
                    }
                    plot_expanded = true;
                    expand_plots.setImageDrawable(getDrawable(R.drawable.ic_arrow_drop_up_24dp));
                }

            }
        });
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        int res_id = item.getItemId();
        if(res_id == android.R.id.home) {
            super.onBackPressed();
        }
        return true;
    }
}
