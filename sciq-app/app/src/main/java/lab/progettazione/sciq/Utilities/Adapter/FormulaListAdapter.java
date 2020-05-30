package lab.progettazione.sciq.Utilities.Adapter;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.progettazione.sciq.R;

import java.util.ArrayList;

import io.github.kexanie.library.MathView;

public class FormulaListAdapter extends RecyclerView.Adapter<FormulaListAdapter.MyViewHolder> {

    private Context mContext;
    private ArrayList<String> mathMlList;

    public FormulaListAdapter(Context context, ArrayList<String> expressionList) {
        this.mContext = context;
        this.mathMlList = expressionList;
    }


    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view;
        LayoutInflater mInflater = LayoutInflater.from(mContext);
        view = mInflater.inflate(R.layout.formula_item, parent, false);
        return new MyViewHolder(view);
    }

    public static class MyViewHolder extends RecyclerView.ViewHolder {
        MathView mathView;

        public MyViewHolder(View itemView) {
            super(itemView);
            mathView = itemView.findViewById(R.id.formula_view);
        }
    }

    @Override
    public int getItemCount() {
        return mathMlList.size();
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        String mathML = mathMlList.get(position);
        holder.mathView.setText(mathML);
    }
}
