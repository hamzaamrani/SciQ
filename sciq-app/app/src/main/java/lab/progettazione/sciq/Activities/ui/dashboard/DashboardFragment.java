package lab.progettazione.sciq.Activities.ui.dashboard;

import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.cardview.widget.CardView;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProviders;

import com.progettazione.sciq.R;

import lab.progettazione.sciq.Activities.ui.ShowCollections;
import lab.progettazione.sciq.Utilities.Utils.SharedUtils;


public class DashboardFragment extends Fragment {

    private DashboardViewModel dashboardViewModel;
    private SharedUtils check = new SharedUtils();


    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        dashboardViewModel =
                ViewModelProviders.of(this).get(DashboardViewModel.class);
        View root = inflater.inflate(R.layout.fragment_dashboard, container, false);
        final TextView textView = root.findViewById(R.id.text_dashboard);

        final LinearLayout if_logged = root.findViewById(R.id.if_logged);
        final LinearLayout if_not_logged = root.findViewById(R.id.if_not_logged);


        if (check.userLogged(getContext())) {
            if_logged.setVisibility(View.VISIBLE);
        } else {
            if_not_logged.setVisibility(View.VISIBLE);
        }

        final CardView my_applications = root.findViewById(R.id.my_applications);
        final CardView my_collections = root.findViewById(R.id.my_collections);
        final CardView community = root.findViewById(R.id.community);


        my_applications.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

            }
        });

        my_collections.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent i = new Intent(getContext(), ShowCollections.class);
                startActivity(i);
            }
        });

        community.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

            }
        });


        dashboardViewModel.getText().observe(getViewLifecycleOwner(), new Observer<String>() {
            @Override
            public void onChanged(@Nullable String s) {
                textView.setText(s);
            }
        });
        return root;
    }
}
