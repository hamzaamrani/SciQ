package lab.progettazione.sciq.Utilities.Adapter;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.google.android.flexbox.AlignItems;
import com.google.android.flexbox.FlexDirection;
import com.google.android.flexbox.FlexWrap;
import com.google.android.flexbox.FlexboxLayoutManager;
import com.google.android.flexbox.JustifyContent;
import com.progettazione.sciq.R;

import java.util.ArrayList;

import lab.progettazione.sciq.Model.Collection;

import static java.lang.String.valueOf;

public class CollectionAdapter extends RecyclerView.Adapter<CollectionAdapter.MyViewHolder> {

    private Context mContext;
    private ArrayList<Collection> collectionList;

    public CollectionAdapter(Context context, ArrayList<Collection> collectionList){
        this.mContext = context;
        this.collectionList = collectionList;
    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view;
        LayoutInflater mIN = LayoutInflater.from(mContext);
        view = mIN.inflate(R.layout.collection_item, parent, false);
        return new MyViewHolder(view);
    }

    public static class MyViewHolder extends RecyclerView.ViewHolder{
        private TextView title_collection;
        private TextView collection_count;
        private RecyclerView expression_list;
        private Boolean expanded;

        public MyViewHolder(View itemView){
            super(itemView);
            title_collection = itemView.findViewById(R.id.title_collection);
            expression_list = itemView.findViewById(R.id.lista_expression);
            collection_count = itemView.findViewById(R.id.expression_count);
            expanded = false;
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
        holder.collection_count.setText(valueOf(collectionList.get(position).getLista_expression().size()));

        if(collectionList.get(position).getLista_expression().size() > 0){
            ExpressionAdapter expressionAdapter = new ExpressionAdapter(mContext, collectionList.get(position).getLista_expression());
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
                if(collectionList.get(position).getLista_expression().size() > 0){
                    if(!holder.getExpanded()){
                        holder.setExpanded(true);
                        holder.expression_list.setVisibility(View.VISIBLE);
                    }else{
                        holder.setExpanded(false);
                        holder.expression_list.setVisibility(View.GONE);
                    }
                }
            }
        });
    }
}
