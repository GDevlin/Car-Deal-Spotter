package dcu.ca400.devlin.glen.cardealspotter;

import android.content.Context;
import android.content.Intent;
import android.support.annotation.NonNull;
import android.support.constraint.ConstraintLayout;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import java.text.DecimalFormat;
import java.util.ArrayList;

public class RecyclerViewAdapter extends RecyclerView.Adapter<RecyclerViewAdapter.ViewHolder> {

    private static final String TAG = "RecyclerViewAdapter";

    private ArrayList<ArrayList <String>> cars;
    Context listContext;

    public RecyclerViewAdapter(ArrayList<ArrayList <String>> new_cars, Context listContext) {
        Log.d("recycler cars", String.valueOf(cars));
        cars = new_cars;
        this.listContext = listContext;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.layout_list_items, parent, false);
        ViewHolder viewHolder = new ViewHolder(view);
        return viewHolder;
    }


    @Override
    public void onBindViewHolder(@NonNull final ViewHolder holder, final int position) {
        Log.d(TAG, "onBindViewHolder: called.");

        holder.carMakeTextView.setText(cars.get(position).get(2));
        holder.carModelTextView.setText(cars.get(position).get(3));
        String carYear = cars.get(position).get(4).substring(0,4);
        holder.yearTextView.setText(carYear);
        holder.colourTextView.setText(capitaliseWord(cars.get(position).get(9)));
        holder.engineSizeTextView.setText(cars.get(position).get(8));
        holder.fuelTypeTextView.setText(cars.get(position).get(7));
        holder.countyTextView.setText(cars.get(position).get(13));
        holder.priceTextView.setText("Price: " + convertNumberToCurrency(cars.get(position).get(5)));
        //int estValuePosition = cars.size() - 2;
        Float estimatedValueFloat = Float.parseFloat(cars.get(position).get(16));
        int estimatedValueInt = (int) Math.round(estimatedValueFloat);
        String estValueString = String.valueOf(estimatedValueInt);
        holder.estValueTextView.setText("Estimated Value: " + convertNumberToCurrency(estValueString));
        //int priceDiffPosition = cars.size() - 1;
        holder.priceDiffTextView.setText("Savings: " + convertNumberToCurrency(cars.get(position).get(17)));
        holder.parent_layout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //Toast.makeText(listContext, "This car was clicked", Toast.LENGTH_SHORT).show();
                Intent viewCarIntent = new Intent(view.getContext(), ViewCar.class);
                viewCarIntent.putExtra("Car Features", cars.get(position));
                listContext.startActivity(viewCarIntent);

            }
        });
    }

    @Override
    public int getItemCount() {
        return cars.size();
    }

    public class ViewHolder extends RecyclerView.ViewHolder {

        TextView carMakeTextView;
        TextView carModelTextView;
        TextView yearTextView;
        TextView colourTextView;
        TextView engineSizeTextView;
        TextView fuelTypeTextView;
        TextView priceTextView;
        TextView estValueTextView;
        TextView priceDiffTextView;
        TextView countyTextView;

        ConstraintLayout parent_layout;
        public ViewHolder(View itemView) {
            super(itemView);
            carMakeTextView = itemView.findViewById(R.id.carMakeTextView);
            carModelTextView = itemView.findViewById(R.id.carModelTextView);
            yearTextView = itemView.findViewById(R.id.yearTextView);
            colourTextView = itemView.findViewById(R.id.colourTextView);
            engineSizeTextView = itemView.findViewById(R.id.engineSizeTextView);
            fuelTypeTextView = itemView.findViewById(R.id.fuelTypeTextView);
            priceTextView = itemView.findViewById(R.id.priceTextView);
            estValueTextView = itemView.findViewById(R.id.estValueTextView);
            priceDiffTextView = itemView.findViewById(R.id.priceDiffTextView);
            countyTextView = itemView.findViewById(R.id.countyTextView);
            parent_layout = itemView.findViewById(R.id.parent_layout);
        }
    }

    public void clearAdapter() {
        final int size = cars.size();
        cars.clear();
        notifyItemRangeRemoved(0, size);
    }

    public String convertNumberToCurrency(String number){
        float numFloat = Float.parseFloat(number);
        int numInt = (int) numFloat;
        DecimalFormat properfomat = new DecimalFormat("#");
        properfomat.setGroupingUsed(true);
        properfomat.setGroupingSize(3);
        return String.valueOf("€" + properfomat.format(Math.abs(numInt)));
    }

    public String capitaliseWord(String word){
        return word.substring(0,1).toUpperCase() + word.substring(1).toLowerCase();
    }
}
