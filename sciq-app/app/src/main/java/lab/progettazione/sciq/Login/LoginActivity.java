package lab.progettazione.sciq.Login;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import com.google.android.material.textfield.TextInputEditText;
import com.progettazione.sciq.R;

import org.json.JSONObject;

import lab.progettazione.sciq.Utilities.AsyncTasks.LoginPostAsyncTask;
import lab.progettazione.sciq.Utilities.Interfaces.ReturnString;

public class LoginActivity extends AppCompatActivity implements ReturnString {

    private TextInputEditText input_name_login, input_password_login;
    private Button login_button;
    LoginPostAsyncTask loginPostAsyncTask;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        input_name_login = findViewById(R.id.input_name_login);
        input_password_login = findViewById(R.id.input_password_login);
        login_button = findViewById(R.id.login_button);



        login_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(!input_name_login.getText().toString().equals("") && !input_password_login.getText().toString().equals("")){
                    // All the fields are filled
                    String username = input_name_login.getText().toString();
                    String password = input_password_login.getText().toString();
                    JSONObject postLoginParameters = new JSONObject();
                    try{
                        postLoginParameters.put("username", username);
                        postLoginParameters.put("password", password);
                    }catch (Exception e){
                        e.printStackTrace();
                    }

                    loginPostAsyncTask = new LoginPostAsyncTask(LoginActivity.this);
                    loginPostAsyncTask.delegate = LoginActivity.this;
                    loginPostAsyncTask.execute("http://sciq-unimib-dev.herokuapp.com/login", postLoginParameters);

                }else{
                    if(input_name_login.getText().toString().equals(""))
                        input_name_login.setError("Required!");
                    else
                        input_name_login.setError(null);

                    if(input_password_login.getText().toString().equals(""))
                        input_password_login.setError("Required!");
                    else
                        input_password_login.setError(null);
                }
            }
        });

    }

    @Override
    public void processFinish(String output) {
        try{
            JSONObject login_response = new JSONObject(output);
            if(login_response.has("access_token")){
                Log.d("Access Token", login_response.getString("access_token"));
                input_password_login.setError(null);
                input_name_login.setError(null);
            }else{
                Toast.makeText(getApplicationContext(), login_response.getString("results"), Toast.LENGTH_LONG).show();
                input_name_login.setError("Username could be wrong");
                input_password_login.setError("Password could be wrong");
            }
        }catch (Exception e){
            e.printStackTrace();
        }


    }
}
