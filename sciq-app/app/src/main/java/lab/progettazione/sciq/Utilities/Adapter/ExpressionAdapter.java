package lab.progettazione.sciq.Utilities.Adapter;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;
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
    private static String latex_delimiter_start = "\\(";
    private static String latex_delimiter_end = "\\)";
    private ExpressionItemListener expressionItemListener;
    private ExpressionDeleted deleted;

    public ExpressionAdapter(Context context, ArrayList<Expression> expressionList, ExpressionItemListener listener, ExpressionDeleted deleted){
        this.mContext = context;
        this.expressionList = expressionList;
        this.expressionItemListener = listener;
        this.deleted = deleted;
    }

    public static class MyViewHolder extends RecyclerView.ViewHolder{
        MathView expression_view;
        ImageButton view_expression;
        ImageView delete_expression;

        public MyViewHolder(View itemView){
            super(itemView);
            expression_view = itemView.findViewById(R.id.query_title);
            view_expression = itemView.findViewById(R.id.view_expression);
            delete_expression = itemView.findViewById(R.id.delete_expression);
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
        holder.expression_view.setText(latex_delimiter_start + title + latex_delimiter_end);
        holder.view_expression.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //Toast.makeText(mContext, "Clicked on = " + expressionList.get(position).getQuery(), Toast.LENGTH_LONG).show();
                expressionItemListener.onClickViewExpression(v, position, expressionList.get(position));
            }
        });

        holder.delete_expression.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                AlertDialog.Builder builder = new AlertDialog.Builder(mContext);
                builder.setTitle("Delete expression?")
                        .setPositiveButton("yes", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                deleted.onDeleteExpression(v, position, expressionList.get(position));
                            }
                        }).setNegativeButton("no", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        // do nothing
                    }
                }).show();
            }
        });
    }

    @Override
    public int getItemCount() {
        return expressionList.size();
    }


    public interface ExpressionItemListener{
        void onClickViewExpression(View v, int position, Expression expression);
    }

    public interface  ExpressionDeleted{
        void onDeleteExpression(View v, int position, Expression expression);
    }

}
