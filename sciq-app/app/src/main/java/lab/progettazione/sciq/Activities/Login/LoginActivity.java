package lab.progettazione.sciq.Activities.Login;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.google.android.material.textfield.TextInputEditText;
import com.progettazione.sciq.R;

import org.json.JSONObject;

import java.util.Date;

import lab.progettazione.sciq.Activities.ui.MainActivity;
import lab.progettazione.sciq.Utilities.AsyncTasks.LoginPostAsyncTask;
import lab.progettazione.sciq.Utilities.Interfaces.ReturnString;

public class LoginActivity extends AppCompatActivity implements ReturnString {

    private TextInputEditText input_name_login, input_password_login;
    private Button login_button;
    LoginPostAsyncTask loginPostAsyncTask;
    private TextView no_login;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        input_name_login = findViewById(R.id.input_name_login);
        input_password_login = findViewById(R.id.input_password_login);
        login_button = findViewById(R.id.login_button);
        no_login = findViewById(R.id.no_login);


        login_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (!input_name_login.getText().toString().equals("") && !input_password_login.getText().toString().equals("")) {
                    // All the fields are filled
                    String username = input_name_login.getText().toString();
                    String password = input_password_login.getText().toString();
                    JSONObject postLoginParameters = new JSONObject();
                    try {
                        postLoginParameters.put("username", username);
                        postLoginParameters.put("password", password);
                    } catch (Exception e) {
                        e.printStackTrace();
                    }

                    loginPostAsyncTask = new LoginPostAsyncTask(LoginActivity.this);
                    loginPostAsyncTask.delegate = LoginActivity.this;
                    loginPostAsyncTask.execute("http://sciq-unimib.herokuapp.com/login", postLoginParameters);

                } else {
                    if (input_name_login.getText().toString().equals(""))
                        input_name_login.setError("Required!");
                    else
                        input_name_login.setError(null);

                    if (input_password_login.getText().toString().equals(""))
                        input_password_login.setError("Required!");
                    else
                        input_password_login.setError(null);
                }
            }
        });

        no_login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                SharedPreferences isLogged = getSharedPreferences("Logged", 0);
                SharedPreferences.Editor login = isLogged.edit();
                login.clear();
                login.putBoolean("isLogged", false);
                login.apply();
                Intent i = new Intent(LoginActivity.this, MainActivity.class);
                startActivity(i);
            }
        });

    }

    @Override
    public void processFinish(String output) {
        if (output.equalsIgnoreCase("Connection error!")) {
            Toast.makeText(this, "Something went wrong, check your connection", Toast.LENGTH_LONG).show();
        } else {
            try {
                JSONObject login_response = new JSONObject(output);
                if (login_response.has("access_token")) {
                    String tkn = login_response.getString("access_token");

                    //Todo encrypt preferences
                    SharedPreferences pref = getSharedPreferences("Info", MODE_PRIVATE);
                    SharedPreferences.Editor edit_pref = pref.edit();
                    edit_pref.clear();
                    edit_pref.putString("token", tkn);
                    edit_pref.apply();

                    SharedPreferences isLogged = getSharedPreferences("Logged", 0);
                    SharedPreferences.Editor login = isLogged.edit();
                    login.clear();
                    login.putBoolean("isLogged", true);
                    login.putLong("lastLogin", new Date().getTime());
                    login.apply();

                    input_password_login.setError(null);
                    input_name_login.setError(null);
                    Intent i = new Intent(LoginActivity.this, MainActivity.class);
                    startActivity(i);
                } else {
                    Toast.makeText(getApplicationContext(), login_response.getString("results"), Toast.LENGTH_LONG).show();
                    input_name_login.setError("Username could be wrong");
                    input_password_login.setError("Password could be wrong");
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }


    }
}
