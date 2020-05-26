package lab.progettazione.sciq.Activities.Login;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;

import androidx.appcompat.app.AppCompatActivity;

import com.progettazione.sciq.R;

import java.util.Date;

import lab.progettazione.sciq.Activities.MainActivity;

public class SplashActivity extends AppCompatActivity {

    private static int SPLASH_TIME_OUT = 1200;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash);

        String username, token;
        final Class destination_activity;

        // Check if the user is already logged into SciQ
        SharedPreferences user_logged = getSharedPreferences("Logged", MODE_PRIVATE);
        boolean logged = user_logged.getBoolean("logged", false);
        Log.d("UserLogged", "User logged = " + logged);

        //If user is logged check if the old token is already valid

        if (logged) {
            Long last_login = user_logged.getLong("lastLogin", MODE_PRIVATE);
            Long this_login = new Date().getTime();
            //Check how much time passed since last login
            Long diff = this_login - last_login;
            long diffHours = diff / (60 * 60 * 1000) % 24;
            long diffDays = diff / (24 * 60 * 60 * 1000);
            if (!(diffDays > 0) && !(diffHours > 8)) {
                Log.d("UserLogged", "Last login within eight hours!");
                // Token is still valid
                destination_activity = MainActivity.class;
            } else {
                Log.d("UserLogged", "Token expired");
                destination_activity = SignupActivity.class;
            }
        } else {
            Log.d("UserLogged", "User has not logged in yet");
            destination_activity = SignupActivity.class;
        }

        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                Intent next_activity = new Intent(SplashActivity.this, destination_activity);
                //Set flags to avoid user get back to this activity with OS back button
                next_activity.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                startActivity(next_activity);
                overridePendingTransition(R.anim.fade_in, R.anim.fade_out);
                finish();
            }
        }, SPLASH_TIME_OUT);
    }
}
