package dcu.ca400.devlin.glen.cardealspotter;

import android.graphics.Color;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.Arrays;

public class Browse_Cars_Activity extends AppCompatActivity {

    private TextView carMakeTextView;

    private static final String TAG = "Browse_Cars_Activity";

    private ArrayList<ArrayList<String>> cars;// = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_browse__cars_);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        toolbar.setTitle("Browse Cars");
        toolbar.setTitleTextColor(Color.WHITE);
        setSupportActionBar(toolbar);

        Log.d(TAG, "Oncreate started");

        carMakeTextView = (TextView) findViewById(R.id.carMakeTextView);
        String string_of_cars = getIntent().getStringExtra("LIST_CARS_URL");
        Log.d("string of cars", String.valueOf(string_of_cars));

        cars = new ArrayList<>();
        cars.clear();

        breakDownCarsStrings(string_of_cars);
        Log.d("Browsing cars", String.valueOf(cars));
        initRecyclerView();
    }

    @Override
    protected void onRestart() {
        super.onRestart();
    }

    @Override
    public void onBackPressed() {
        super.onBackPressed();
    }


    //Break down the cars string into an array of cars
    //Pass this arraylist to recyclerview
    private void breakDownCarsStrings(String string_of_cars){
            Log.d("check string", string_of_cars);
            String[] each_car_as_string = string_of_cars.split("\\{");
            ArrayList<String> cars_seperated = new ArrayList<String>(Arrays.asList(each_car_as_string));
            Log.d("Array", String.valueOf(cars_seperated));

        try {
            for (int i = 0; i < cars_seperated.size(); i++) {
                ArrayList<String> temp_car_list = new ArrayList<String>(Arrays.asList(cars_seperated.get(i).split("\\|")));
                String estimatedValue = temp_car_list.get(temp_car_list.size() - 2);
                String priceDiffValue = temp_car_list.get(temp_car_list.size() - 1);
                String county = temp_car_list.get(temp_car_list.size() - 1);

                ArrayList<String> carToAdd = new ArrayList<String>(temp_car_list.subList(0, 16));
                carToAdd.add(estimatedValue);
                carToAdd.add(priceDiffValue);

                cars.add(carToAdd);
            }
        }catch (ArrayIndexOutOfBoundsException e){
            e.printStackTrace();
        }

        for(int i = 0; i < cars.size(); i++){
            Log.d("Each Array", String.valueOf(cars.get(i)));
        }
    }

    private void initRecyclerView(){
        Log.d("recycle started", String.valueOf(cars));
        RecyclerViewAdapter adapter  = new RecyclerViewAdapter(cars, this);
        RecyclerView recyclerView = findViewById(R.id.carRecyclerView);
        recyclerView.setAdapter(adapter);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));
    }
}
