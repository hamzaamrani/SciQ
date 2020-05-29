package lab.progettazione.sciq.Model;

import android.os.Parcel;
import android.os.Parcelable;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;

public class Collection implements Parcelable {

    private String nome;
    private String info;
    private ArrayList<Expression> lista_expression = new ArrayList<>();

    public Collection(JSONObject collection_item) throws Exception {

        this.nome = collection_item.getString("name");
        this.info = collection_item.getString("info");
        JSONArray expressions = collection_item.getJSONArray("expressions");
        if(expressions.length() > 0){
            for(int i = 0 ; i < expressions.length(); i ++){
                Expression current_expression = new Expression(expressions.getJSONObject(i));
                this.lista_expression.add(current_expression);
            }
        }else{
            this.lista_expression = null;
        }
    }

    protected Collection(Parcel in) {
        nome = in.readString();
        info = in.readString();
        lista_expression = in.createTypedArrayList(Expression.CREATOR);
    }

    public static final Creator<Collection> CREATOR = new Creator<Collection>() {
        @Override
        public Collection createFromParcel(Parcel in) {
            return new Collection(in);
        }

        @Override
        public Collection[] newArray(int size) {
            return new Collection[size];
        }
    };

    @Override
    public String toString() {
        return "Collection{" +
                "nome='" + nome + '\'' +
                ", info='" + info + '\'' +
                ", lista_expression=" + lista_expression +
                '}';
    }

    public String getNome() {
        return nome;
    }

    public String getInfo() {
        return info;
    }

    public ArrayList<Expression> getLista_expression() {
        return lista_expression;
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeString(nome);
        dest.writeString(info);
        dest.writeTypedList(lista_expression);
    }
}
