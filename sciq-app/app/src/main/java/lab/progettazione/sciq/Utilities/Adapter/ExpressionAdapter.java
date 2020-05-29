package lab.progettazione.sciq.Utilities.Adapter;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.progettazione.sciq.R;

import java.util.ArrayList;

import io.github.kexanie.library.MathView;
import lab.progettazione.sciq.Model.Expression;

public class ExpressionAdapter extends RecyclerView.Adapter<ExpressionAdapter.MyViewHolder> {

    private Context mContext;
    private ArrayList<Expression> expressionList;

    public ExpressionAdapter(Context context, ArrayList<Expression> expressionList){
        this.mContext = context;
        this.expressionList = expressionList;
    }

    public static class MyViewHolder extends RecyclerView.ViewHolder{
        MathView expression_view;
        Button view_expression;

        public MyViewHolder(View itemView){
            super(itemView);
            expression_view = itemView.findViewById(R.id.query_title);
            view_expression = itemView.findViewById(R.id.view_expression);
        }
    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view;
        LayoutInflater mInflater = LayoutInflater.from(mContext);
        view = mInflater.inflate(R.layout.expression_item, parent, false);
        return new MyViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        String title = expressionList.get(position).getQuery();
        holder.expression_view.setText(title);
        holder.view_expression.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(mContext, "Clicked on = " + expressionList.get(position).getQuery(), Toast.LENGTH_LONG).show();
            }
        });
    }

    @Override
    public int getItemCount() {
        return expressionList.size();
    }


}
