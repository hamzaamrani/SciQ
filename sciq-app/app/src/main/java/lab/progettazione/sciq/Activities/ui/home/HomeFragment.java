package lab.progettazione.sciq.Activities.ui.home;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProviders;

import com.google.android.material.textfield.TextInputEditText;
import com.nishant.math.MathView;
import com.progettazione.sciq.R;

import java.util.logging.Logger;

import lab.progettazione.sciq.Object.Expression;
import lab.progettazione.sciq.Utilities.AsyncTasks.SubmitExpression;
import lab.progettazione.sciq.Utilities.Interfaces.ExpressionInterface;
import lab.progettazione.sciq.Utilities.Utils.SharedUtils;


public class HomeFragment extends Fragment implements ExpressionInterface {

    private HomeViewModel homeViewModel;
    private SubmitExpression submitExpression;
    private SharedUtils check = new SharedUtils();

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        homeViewModel = ViewModelProviders.of(this).get(HomeViewModel.class);
        View root = inflater.inflate(R.layout.fragment_home, container, false);
        final TextView textView = root.findViewById(R.id.text_home);
        final LinearLayout preview = root.findViewById(R.id.preview);
        final TextInputEditText expression_input = root.findViewById(R.id.expression_input);
        final MathView mathView = root.findViewById(R.id.math_view);
        final Button submit_expression = root.findViewById(R.id.submit_expression);
        final ProgressBar progressBar = root.findViewById(R.id.my_progressBar);




        String asciimath_delimiter = "`";



        expression_input.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
                preview.setVisibility(View.VISIBLE);
            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                mathView.setText(asciimath_delimiter + s.toString() + asciimath_delimiter);
            }

            @Override
            public void afterTextChanged(Editable s) {

            }
        });

        submit_expression.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                submitExpression = new SubmitExpression(getContext(), progressBar);
                submitExpression.delegate = HomeFragment.this;
                if(expression_input.getText().length() > 0){
                    expression_input.setError(null);
                    if(check.userLogged(getContext())){
                        submitExpression.execute(check.getToken(getContext()), expression_input.getText().toString().trim());
                    }
                }else
                    expression_input.setError("Type something!");
            }
        });


        homeViewModel.getText().observe(getViewLifecycleOwner(), new Observer<String>() {
            @Override
            public void onChanged(@Nullable String s) {
                textView.setText(s);
            }
        });
        return root;
    }



    @Override
    public void onExpressionSuccesfull(Expression expression) {
        Log.d("submit_expression", "Request sucesfull");
        for(int i = 0; i < expression.getPlots().size(); i ++){
            Log.d("submit_expression", "Plots of the expression n° " + i + " =  " + expression.getPlots().get(i));
        }
    }

    @Override
    public void onExpressionFailure(String error) {
        Toast.makeText(getContext(), error, Toast.LENGTH_LONG).show();
    }
}
