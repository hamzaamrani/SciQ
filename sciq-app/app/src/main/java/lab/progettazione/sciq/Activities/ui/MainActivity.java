package lab.progettazione.sciq.Activities.ui;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.MediaStore;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;

import com.google.android.material.bottomnavigation.BottomNavigationView;
import com.hbisoft.pickit.PickiT;
import com.progettazione.sciq.R;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;

import java.io.ByteArrayOutputStream;

import lab.progettazione.sciq.Activities.Login.SignupActivity;
import lab.progettazione.sciq.Utilities.Utils.SharedUtils;

public class MainActivity extends AppCompatActivity {

    private SharedUtils check = new SharedUtils();
    private PickiT pickiT;

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
    }

    // Define menu to be inflated on the action bar
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        SharedPreferences isLogged = getSharedPreferences("Logged", 0);
        if(check.userLogged(MainActivity.this)){
            MenuInflater menuInflater = getMenuInflater();
            menuInflater.inflate(R.menu.menu_home,menu);
        }
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {

        if(item.getItemId() == R.id.log_out){
            new AlertDialog.Builder(this)
                    .setTitle("Logout")
                    .setMessage("Do you want to log out?")
                    .setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialogInterface, int i) {
                            SharedPreferences isLogged = getSharedPreferences("Logged", 0);
                            SharedPreferences.Editor login = isLogged.edit();
                            login.clear();
                            login.putBoolean("isLogged", false );
                            login.apply();

                            SharedPreferences pref = getSharedPreferences("Info", MODE_PRIVATE);
                            SharedPreferences.Editor edit_pref = pref.edit();
                            edit_pref.clear();
                            edit_pref.apply();

                            Context context = MainActivity.this;
                            Class destinationActivity = SignupActivity.class;
                            Intent logOutIntent = new Intent(context, destinationActivity);
                            logOutIntent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP| Intent.FLAG_ACTIVITY_NEW_TASK| Intent.FLAG_ACTIVITY_CLEAR_TASK);
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
        if(codiceRisultato == Activity.RESULT_OK){
            switch (codiceRichiesta) {
                case 100:
                    Uri tempUri = null;
                    try{
                        Bitmap bp = (Bitmap) data.getExtras().get("data");
                        tempUri = getImageUri(getApplicationContext(), bp);
                    }catch (Exception e){
                        e.printStackTrace();
                    }
                    if(tempUri != null){
                        //case_camera = true;
                        pickiT.getPath(tempUri, Build.VERSION.SDK_INT);
                    }
                    break;
            }
        }

    }


    public Uri getImageUri(Context inContext, Bitmap inImage) {
        ByteArrayOutputStream bytes = new ByteArrayOutputStream();
        inImage.compress(Bitmap.CompressFormat.JPEG, 100, bytes);
        String path = MediaStore.Images.Media.insertImage(inContext.getContentResolver(), inImage, "Title", null);
        return Uri.parse(path);
    }

}
