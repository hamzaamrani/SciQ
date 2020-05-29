package lab.progettazione.sciq.Activities.ui;

import androidx.appcompat.app.AppCompatActivity;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;

import com.progettazione.sciq.R;

import java.util.ArrayList;
import java.util.Collection;

import lab.progettazione.sciq.Utilities.AsyncTasks.GetCollections;
import lab.progettazione.sciq.Utilities.Interfaces.ReturnString;
import lab.progettazione.sciq.Utilities.Utils.SharedUtils;

public class ShowCollections extends AppCompatActivity implements ReturnString {

    private GetCollections getCollections;
    private SharedUtils check;
    private String token;
    private ArrayList<Collection> collections;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_show_collections);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        getSupportActionBar().setDisplayShowHomeEnabled(true);
        getSupportActionBar().setTitle("My collections");

        token = check.getToken(this);
        getCollections = new GetCollections(this);
        getCollections.setDelegate(this);
        String endpoint = "collections";
        getCollections.execute(token, "https://sciq-unimib-dev.herokuapp.com/" + endpoint);

    }

    @Override
    public void processFinish(String output) {
        Log.d("Collections", output);
    }
}
