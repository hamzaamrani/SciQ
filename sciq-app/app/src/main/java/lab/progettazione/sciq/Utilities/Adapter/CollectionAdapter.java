package lab.progettazione.sciq.Utilities.Adapter;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.google.android.flexbox.AlignItems;
import com.google.android.flexbox.FlexDirection;
import com.google.android.flexbox.FlexWrap;
import com.google.android.flexbox.FlexboxLayoutManager;
import com.google.android.flexbox.JustifyContent;
import com.progettazione.sciq.R;

import org.json.JSONObject;

import java.util.ArrayList;

import lab.progettazione.sciq.Model.Collection;
import lab.progettazione.sciq.Model.Expression;
import lab.progettazione.sciq.Utilities.AsyncTasks.DeleteExpression;
import lab.progettazione.sciq.Utilities.Interfaces.ReturnString;
import lab.progettazione.sciq.Utilities.Utils.SharedUtils;

import static java.lang.String.valueOf;

public class CollectionAdapter extends RecyclerView.Adapter<CollectionAdapter.MyViewHolder> implements ReturnString {
    private Context mContext;
    private ArrayList<Collection> collectionList;
    private ExpressionAdapter.ExpressionItemListener listener;
    private SharedUtils check;
    ExpressionAdapter expressionAdapter;


    public CollectionAdapter(Context context, ArrayList<Collection> collectionList, ExpressionAdapter.ExpressionItemListener listener) {
        this.mContext = context;
        this.collectionList = collectionList;
        this.listener = listener;
    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view;
        LayoutInflater mIN = LayoutInflater.from(mContext);
        view = mIN.inflate(R.layout.collection_item, parent, false);
        return new MyViewHolder(view);
    }


    public static class MyViewHolder extends RecyclerView.ViewHolder {
        private TextView title_collection;
        private TextView collection_count;
        private TextView collection_info;
        private Boolean expanded;
        private LinearLayout if_expression;
        private RecyclerView expression_list;

        public MyViewHolder(View itemView) {
            super(itemView);

            title_collection = itemView.findViewById(R.id.title_collection);
            expression_list = itemView.findViewById(R.id.lista_expression);
            collection_count = itemView.findViewById(R.id.expression_count);
            if_expression = itemView.findViewById(R.id.if_expression);
            collection_info = itemView.findViewById(R.id.collection_info);
            expanded = false;
        }

        public RecyclerView getExpression_list() {
            return expression_list;
        }

        public void setExpression_list(RecyclerView expression_list) {
            this.expression_list = expression_list;
        }

        public void setExpanded(Boolean expanded) {
            this.expanded = expanded;
        }

        public Boolean getExpanded() {
            return expanded;
        }

    }

    @Override
    public int getItemCount() {
        return collectionList.size();
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        String title = collectionList.get(position).getNome();
        holder.title_collection.setText(title.toUpperCase());
        holder.collection_info.setText(collectionList.get(position).getInfo());
        if (collectionList.get(position).getLista_expression() != null) {
            holder.collection_count.setText(valueOf(collectionList.get(position).getLista_expression().size()));
        } else {
            holder.collection_count.setText(valueOf(0));
        }

        if (collectionList.get(position).getLista_expression() != null && collectionList.get(position).getLista_expression().size() > 0) {
            expressionAdapter = new ExpressionAdapter(mContext, collectionList.get(position).getLista_expression(), listener, new ExpressionAdapter.ExpressionDeleted() {
                @Override
                public void onDeleteExpression(View v, int expr_pos, Expression expression, Collection collection) {
                    System.out.println("Clicked on collection =  " + collectionList.get(position).getNome() + " that is equals to " + collection.getNome());
                    System.out.println("Clicked on Expression = " + collectionList.get(position).getLista_expression().get(expr_pos).getQuery() + " that is equals to " + expression.getQuery());
                    notifyItemChanged(position);
                    JSONObject postData = new JSONObject();
                    try {
                        postData.put("id_expr", expression.getId());
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                    check = new SharedUtils();
                    DeleteExpression deleteExpression = new DeleteExpression(mContext);
                    deleteExpression.setDelegate(CollectionAdapter.this);
                    deleteExpression.execute("https://sciq-unimib.herokuapp.com/delete_expression", check.getToken(mContext), postData);

                }
            }, collectionList.get(position));
            FlexboxLayoutManager layoutManager = new FlexboxLayoutManager(mContext);
            layoutManager.setFlexDirection(FlexDirection.ROW);
            layoutManager.setJustifyContent(JustifyContent.SPACE_AROUND);
            layoutManager.setFlexWrap(FlexWrap.WRAP);
            layoutManager.setAlignItems(AlignItems.FLEX_START);
            holder.expression_list.setLayoutManager(layoutManager);
            holder.expression_list.setAdapter(expressionAdapter);
        }


        holder.title_collection.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (collectionList.get(position).getLista_expression() != null && collectionList.get(position).getLista_expression().size() > 0) {
                    System.out.println("Premuto, ci sono expression, expanded = " + holder.getExpanded());
                    if (!holder.getExpanded()) {
                        holder.setExpanded(true);
                        holder.if_expression.setVisibility(View.VISIBLE);
                    } else {
                        holder.setExpanded(false);
                        holder.if_expression.setVisibility(View.GONE);
                    }
                } else
                    System.out.println("Premuto, non ci sono expression");
            }
        });
    }


    @Override
    public void processFinish(String output) {
        System.out.println("Fine delete " + output);
    }
}
