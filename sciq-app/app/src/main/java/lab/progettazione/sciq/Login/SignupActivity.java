package lab.progettazione.sciq.Login;

import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import com.progettazione.sciq.R;

import lab.progettazione.sciq.HomeActivity;
import lab.progettazione.sciq.Utilities.AsyncTasks.SignUpPostAsyncTask;
import lab.progettazione.sciq.Utilities.Interfaces.ReturnString;

import org.json.JSONObject;

public class SignupActivity extends AppCompatActivity implements ReturnString {

    private Button signup;
    private SignUpPostAsyncTask signupAsynctask;
    private EditText username_signup;
    private EditText password_1_signup;
    private EditText password_2_signup;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signup);

        Button go_to_login;

        signup = findViewById(R.id.signup_button);
        username_signup = findViewById(R.id.input_name_signup);
        password_1_signup = findViewById(R.id.input_password_signup);
        password_2_signup = findViewById(R.id.input_password_signup2);
        go_to_login = findViewById(R.id.go_to_login);

        signup.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(!password_1_signup.getText().toString().equals("") && !password_2_signup.getText().toString().equals("") && !username_signup.getText().toString().equals("")){
                    if (!password_1_signup.getText().toString().equals(password_2_signup.getText().toString())) {
                        Toast.makeText(getApplicationContext(), "Password must be equals!", Toast.LENGTH_LONG).show();
                    } else {
                        JSONObject postDataParams = new JSONObject();
                        try {
                            postDataParams.put("username", username_signup.getText().toString().trim());
                            postDataParams.put("password1", password_1_signup.getText().toString().trim());
                            postDataParams.put("password2", password_2_signup.getText().toString().trim());
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                        signupAsynctask = new SignUpPostAsyncTask(SignupActivity.this);
                        signupAsynctask.delegate = SignupActivity.this;
                        signupAsynctask.execute("http://sciq-unimib-dev.herokuapp.com/signup", postDataParams);
                    }
                }else{
                    if(password_1_signup.getText().toString().equals(""))
                        password_1_signup.setError("Required!");
                    else
                        password_1_signup.setError(null);
                    if(password_2_signup.getText().toString().equals(""))
                        password_2_signup.setError("Required!");
                    else
                        password_2_signup.setError(null);
                    if(username_signup.getText().toString().equals(""))
                        username_signup.setError("Required!");
                    else
                        username_signup.setError(null);
                }


            }
        });


        go_to_login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent go_login = new Intent(getApplicationContext(), LoginActivity.class);
                startActivity(go_login);
            }
        });


    }

    @Override
    public void processFinish(String output) {
        Log.d("SignUp-Response", output);
        if(output.contains("rror")){
            Toast.makeText(this, output, Toast.LENGTH_SHORT).show();
            if(output.equalsIgnoreCase("Error! Username Already taken!"))
                username_signup.setError("Username already taken!");
            else
                username_signup.setError(null);
        }else {
            //Successful signUp
            new AlertDialog.Builder(this)
                    .setTitle("User created")
                    .setMessage("Directly log into application?")
                    .setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            SharedPreferences isLogged = getSharedPreferences("IsLogged", 0);
                            SharedPreferences.Editor login = isLogged.edit();
                            login.clear();
                            login.putBoolean("isLogged", true );
                            login.apply();

                            Intent go_home = new Intent(getApplicationContext(), HomeActivity.class);
                            go_home.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP| Intent.FLAG_ACTIVITY_NEW_TASK| Intent.FLAG_ACTIVITY_CLEAR_TASK);
                            startActivity(go_home);
                            finish();
                        }
                    })
                    .setNegativeButton("No", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            //DO NOTHING

                        }
                    }).show();

        }
    }
}
