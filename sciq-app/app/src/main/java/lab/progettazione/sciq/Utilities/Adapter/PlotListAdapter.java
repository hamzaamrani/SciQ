package lab.progettazione.sciq.Utilities.Adapter;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.util.Base64;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.progettazione.sciq.R;

import java.util.ArrayList;

public class PlotListAdapter extends RecyclerView.Adapter<PlotListAdapter.MyViewHolder> {

    private Context mContext;
    private ArrayList<String> plots;

    public PlotListAdapter(Context mContext, ArrayList<String> plotList) {
        this.mContext = mContext;
        this.plots = plotList;

    }

    @NonNull
    @Override
    public PlotListAdapter.MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view;
        LayoutInflater mInflater = LayoutInflater.from(mContext);
        view = mInflater.inflate(R.layout.plot_item, parent, false);
        return new MyViewHolder(view);
    }


    public static class MyViewHolder extends RecyclerView.ViewHolder {
        ImageView plot_image;

        public MyViewHolder(View itemView) {
            super(itemView);
            plot_image = itemView.findViewById(R.id.plot_image_view);
        }
    }


    @Override
    public int getItemCount() {
        return plots.size();
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        String base64Image = plots.get(position);
        byte[] decodedString = Base64.decode(base64Image, Base64.DEFAULT);
        Bitmap decodedByte = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.length);
        holder.plot_image.setImageBitmap(decodedByte);
    }
}
