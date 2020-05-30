package lab.progettazione.sciq.Activities.ui;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.fragment.app.Fragment;
import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;

import com.google.android.material.bottomnavigation.BottomNavigationView;
import com.progettazione.sciq.R;

import lab.progettazione.sciq.Activities.Login.SignupActivity;
import lab.progettazione.sciq.Utilities.Utils.SharedUtils;

import static android.Manifest.permission.WRITE_EXTERNAL_STORAGE;
import static androidx.constraintlayout.widget.Constraints.TAG;

public class MainActivity extends AppCompatActivity {

    private SharedUtils check = new SharedUtils();


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        BottomNavigationView navView = findViewById(R.id.nav_view);
        // Passing each menu ID as a set of Ids because each
        // menu should be considered as top level destinations.
        AppBarConfiguration appBarConfiguration = new AppBarConfiguration.Builder(
                R.id.navigation_home, R.id.navigation_dashboard, R.id.navigation_notifications)
                .build();
        NavController navController = Navigation.findNavController(this, R.id.nav_host_fragment);
        NavigationUI.setupActionBarWithNavController(this, navController, appBarConfiguration);
        NavigationUI.setupWithNavController(navView, navController);

        // Check Permission for read storage because we will need them further
        if (checkSelfPermission(WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED) {
            Log.v(TAG, "Permission is granted");
        } else {
            Log.v(TAG, "Permission is revoked");
            ActivityCompat.requestPermissions(MainActivity.this, new String[]{WRITE_EXTERNAL_STORAGE}, 1);
        }

    }

    // Define menu to be inflated on the action bar
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        SharedPreferences isLogged = getSharedPreferences("Logged", 0);
        if (check.userLogged(MainActivity.this)) {
            MenuInflater menuInflater = getMenuInflater();
            menuInflater.inflate(R.menu.menu_home, menu);
        }
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {

        if (item.getItemId() == R.id.log_out) {
            new AlertDialog.Builder(this)
                    .setTitle("Logout")
                    .setMessage("Do you want to log out?")
                    .setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialogInterface, int i) {
                            SharedPreferences isLogged = getSharedPreferences("Logged", 0);
                            SharedPreferences.Editor login = isLogged.edit();
                            login.clear();
                            login.putBoolean("isLogged", false);
                            login.apply();

                            SharedPreferences pref = getSharedPreferences("Info", MODE_PRIVATE);
                            SharedPreferences.Editor edit_pref = pref.edit();
                            edit_pref.clear();
                            edit_pref.apply();

                            Context context = MainActivity.this;
                            Class destinationActivity = SignupActivity.class;
                            Intent logOutIntent = new Intent(context, destinationActivity);
                            logOutIntent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                            startActivity(logOutIntent);
                            finish();
                        }
                    })
                    .setNegativeButton("No", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialogInterface, int i) {
                            // Do nothing
                        }
                    }).show();
        }

        return true;
    }

    //ON RESULT CAMERA ACTION
    @Override
    protected void onActivityResult(int codiceRichiesta, int codiceRisultato, Intent data) {
        super.onActivityResult(codiceRichiesta, codiceRisultato, data);

        for (Fragment fragment : getSupportFragmentManager().getPrimaryNavigationFragment().getChildFragmentManager().getFragments()) {
            fragment.onActivityResult(codiceRichiesta, codiceRisultato, data);
        }


    }


}
