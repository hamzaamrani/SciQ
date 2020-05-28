package lab.progettazione.sciq.Activities.ui.home;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
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

import lab.progettazione.sciq.Activities.Login.SignupActivity;
import lab.progettazione.sciq.Activities.ShowResults;
import lab.progettazione.sciq.Model.Expression;
import lab.progettazione.sciq.Utilities.AsyncTasks.SubmitExpression;
import lab.progettazione.sciq.Utilities.Interfaces.ExpressionInterface;
import lab.progettazione.sciq.Utilities.Utils.SharedUtils;


public class HomeFragment extends Fragment implements ExpressionInterface {

    private HomeViewModel homeViewModel;
    private SubmitExpression submitExpression;
    private SharedUtils check = new SharedUtils();
    private static String asciiMath_delimiter = "`";
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



        expression_input.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
                preview.setVisibility(View.VISIBLE);
            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                mathView.setText(asciiMath_delimiter + s.toString() + asciiMath_delimiter);
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
                    }else{
                        submitExpression.execute(null, expression_input.getText().toString().trim());
                    }
                }else
                    expression_input.setError("Type some kind of expression to be evaluated!");
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
    public void onExpressionSuccessful(Expression expression) {
        Log.d("submit_expression", "Request successful");
        System.out.println(expression.toString());
        Intent i  = new Intent(getContext(), ShowResults.class);
        i.putExtra("Expression", expression);
        startActivity(i);
    }

    @Override
    public void onExpressionFailure(String error) {
        if(error.equalsIgnoreCase("Limit request reached!")){
            new AlertDialog.Builder(getContext())
                    .setTitle("Limit request reached!")
                    .setMessage("Sign up or login to perform unlimited requests!")
                    .setPositiveButton("Ok, let's do it", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            Intent i  = new Intent(getContext(), SignupActivity.class);
                            i.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP| Intent.FLAG_ACTIVITY_NEW_TASK| Intent.FLAG_ACTIVITY_CLEAR_TASK);
                            startActivity(i);
                            getActivity().finish();
                        }
                    })
                    .setNegativeButton("No thanks", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            // Do nothing
                        }
                    }).show();
        }
    }
}
