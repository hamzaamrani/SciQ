package com.example.sciq.Login;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.sciq.R;
import com.example.sciq.Utilities.AsyncTasks.LoginAsyncTask;
import com.example.sciq.Utilities.Interfaces.ReturnString;

import org.json.JSONObject;

public class SignupActivity extends AppCompatActivity implements ReturnString {

    private Button signup;
    private LoginAsyncTask loginAsyncTask;
    private EditText username_signup;
    private EditText password_1_signup;
    private EditText password_2_signup;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        signup = findViewById(R.id.signup_button);
        username_signup = findViewById(R.id.input_name_signup);
        password_1_signup = findViewById(R.id.input_password_signup);
        password_2_signup = findViewById(R.id.input_password_signup2);


        signup.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (password_1_signup.getText().equals(password_2_signup.getText())) {
                    Toast.makeText(getApplicationContext(), "Password must be the same!", Toast.LENGTH_LONG).show();
                } else {
                    JSONObject postDataParams = new JSONObject();
                    try {
                        postDataParams.put("username", username_signup.getText().toString().trim());
                        postDataParams.put("password1", password_1_signup.getText().toString().trim());
                        postDataParams.put("password2", password_2_signup.getText().toString().trim());
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                    loginAsyncTask = new LoginAsyncTask(SignupActivity.this);
                    loginAsyncTask.delegate = SignupActivity.this;
                    loginAsyncTask.execute("http://sciq-unimib-dev.herokuapp.com/signup", postDataParams);
                }
            }
        });


    }

    @Override
    public void processFinish(String output) {
        Toast.makeText(this, output, Toast.LENGTH_LONG).show();
    }
}
