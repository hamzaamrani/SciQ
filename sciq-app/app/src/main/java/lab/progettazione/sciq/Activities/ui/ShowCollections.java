package lab.progettazione.sciq.Activities.ui;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.RecyclerView;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.MenuItem;

import com.google.android.flexbox.AlignItems;
import com.google.android.flexbox.FlexDirection;
import com.google.android.flexbox.FlexWrap;
import com.google.android.flexbox.FlexboxLayoutManager;
import com.google.android.flexbox.JustifyContent;
import com.progettazione.sciq.R;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;

import lab.progettazione.sciq.Model.Collection;
import lab.progettazione.sciq.Utilities.Adapter.CollectionAdapter;
import lab.progettazione.sciq.Utilities.AsyncTasks.GetCollections;
import lab.progettazione.sciq.Utilities.Interfaces.ReturnString;
import lab.progettazione.sciq.Utilities.Utils.SharedUtils;

public class ShowCollections extends AppCompatActivity implements ReturnString {

    private GetCollections getCollections;
    private SharedUtils check = new SharedUtils();
    private String token;
    private ArrayList<Collection> collection_list = new ArrayList<>();
    private CollectionAdapter collectionAdapter;
    private RecyclerView lista_collections;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_show_collections);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        getSupportActionBar().setDisplayShowHomeEnabled(true);
        getSupportActionBar().setTitle("My collections");

        lista_collections = findViewById(R.id.lista_collections);

        token = check.getToken(this);
        getCollections = new GetCollections(this);
        getCollections.setDelegate(this);
        String endpoint = "collections";
        getCollections.execute(token, "https://sciq-unimib-dev.herokuapp.com/" + endpoint);

    }

    @Override
    public void processFinish(String output) {
        Log.d("Collections", output);
        try{
            JSONObject response = new JSONObject(output);
            if(response.has("collections")){
                JSONArray list_collections = new JSONArray();
                for(int i = 0 ; i < list_collections.length(); i ++){
                    JSONObject collection = list_collections.getJSONObject(i);
                    Collection current_collection = new Collection(collection);
                    collection_list.add(current_collection);
                }
            }
        }catch (Exception e ){
            e.printStackTrace();
        }

        collectionAdapter = new CollectionAdapter(getApplicationContext(), collection_list);
        FlexboxLayoutManager layoutManager = new FlexboxLayoutManager(getApplicationContext());
        layoutManager.setFlexDirection(FlexDirection.ROW);
        layoutManager.setJustifyContent(JustifyContent.SPACE_AROUND);
        layoutManager.setFlexWrap(FlexWrap.WRAP);
        layoutManager.setAlignItems(AlignItems.FLEX_START);
        lista_collections.setLayoutManager(layoutManager);
        lista_collections.setAdapter(collectionAdapter);

    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        int res_id = item.getItemId();
        if(res_id == android.R.id.home) {
            super.onBackPressed();
        }
        return true;
    }
}
