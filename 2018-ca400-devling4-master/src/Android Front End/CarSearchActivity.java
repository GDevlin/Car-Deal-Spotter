package dcu.ca400.devlin.glen.cardealspotter;

import android.content.Intent;
import android.graphics.Color;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.Scanner;

public class CarSearchActivity extends AppCompatActivity {


    private Spinner makeSpinner;
    private Spinner modelSpinner;
    private Spinner minYearSpinner;
    private Spinner maxYearSpinner;
    private Spinner minPriceSpinner;
    private Spinner maxPriceSpinner;
    private Spinner countySpinner;
    private Spinner fuelTypeSpinner;

    private ArrayAdapter<CharSequence> makeAdapter;
    private ArrayAdapter<CharSequence> modelAdapter;
    private ArrayAdapter<CharSequence> yearAdapter;
    private ArrayAdapter<CharSequence> priceAdapter;
    private ArrayAdapter<CharSequence> countyAdapter;
    private ArrayAdapter<CharSequence> fuelTypeAdapter;

    private String flaskResult = "";
    private String string_car_urls = "";
    private Button searchButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_car_search);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        toolbar.setTitle("Search Cars");
        toolbar.setTitleTextColor(Color.WHITE);
        setSupportActionBar(toolbar);

        makeSpinner = (Spinner) findViewById(R.id.makeSpinner);
        modelSpinner = (Spinner) findViewById(R.id.modelSpinner);
        minYearSpinner = (Spinner) findViewById(R.id.minYearSpinner);
        maxYearSpinner = (Spinner) findViewById(R.id.maxYearSpinner);
        minPriceSpinner = (Spinner) findViewById(R.id.minPriceSpinner);
        maxPriceSpinner = (Spinner) findViewById(R.id.maxPriceSpinner);
        countySpinner = (Spinner) findViewById(R.id.countySpinner);
        fuelTypeSpinner = (Spinner) findViewById(R.id.fuelTypeSpinner);

        initialiseMakeSpinner();
        initialiseYearSpinners();
        initialisePriceSpinners();
        initialiseCountySpinner();
        initialiseFuelTypeSpinner();

        searchButton = (Button)findViewById(R.id.searchButton);
        searchButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                ArrayList<String> search_parameters = searchClicked();
                Toast.makeText(getApplicationContext(), "Loading...", Toast.LENGTH_LONG).show();
                new JSONTask().execute(search_parameters);
                searchButton.setEnabled(false);
            }
        });
    }

    @Override
    protected void onResume() {
        flaskResult = "";
        super.onResume();
        //Allow the serach button to be pressed again
        searchButton.setEnabled(true);
    }


    public void initialiseMakeSpinner(){
        makeAdapter = ArrayAdapter.createFromResource(this,
                R.array.car_make, android.R.layout.simple_list_item_1);
        makeAdapter.setDropDownViewResource(android.R.layout.simple_dropdown_item_1line);
        makeSpinner.setAdapter(makeAdapter);
        makeSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                String selected_make = adapterView.getItemAtPosition(i).toString();
                getModelsForMake(selected_make);
            }
            @Override
            public void onNothingSelected(AdapterView<?> adapterView){

            }
        });
    }

    //Get models that correspond to make
    public void getModelsForMake(String selected_make){
        if(selected_make.equalsIgnoreCase("Audi")) {
            modelAdapter = ArrayAdapter.createFromResource(this,
                    R.array.car_model_audi, android.R.layout.simple_list_item_1);
        }
        else if(selected_make.equalsIgnoreCase("BMW")) {
            modelAdapter = ArrayAdapter.createFromResource(this,
                    R.array.car_model_bmw, android.R.layout.simple_list_item_1);
        }
        else if(selected_make.equalsIgnoreCase("Ford")) {
            modelAdapter = ArrayAdapter.createFromResource(this,
                    R.array.car_model_ford, android.R.layout.simple_list_item_1);
        }
        else if(selected_make.equalsIgnoreCase("Nissan")) {
            modelAdapter = ArrayAdapter.createFromResource(this,
                    R.array.car_model_nissan, android.R.layout.simple_list_item_1);
        }
        else if(selected_make.equalsIgnoreCase("Opel")) {
            modelAdapter = ArrayAdapter.createFromResource(this,
                    R.array.car_model_opel, android.R.layout.simple_list_item_1);
        }
        else if(selected_make.equalsIgnoreCase("Skoda")) {
            modelAdapter = ArrayAdapter.createFromResource(this,
                    R.array.car_model_skoda, android.R.layout.simple_list_item_1);
        }
        else if(selected_make.equalsIgnoreCase("Volkswagen")) {
            modelAdapter = ArrayAdapter.createFromResource(this,
                    R.array.car_model_volkswagen, android.R.layout.simple_list_item_1);
        }
        modelAdapter.setDropDownViewResource(android.R.layout.simple_dropdown_item_1line);
        modelAdapter.notifyDataSetChanged();
        modelSpinner.setAdapter(modelAdapter);
    }

    public void initialiseYearSpinners(){
        yearAdapter = ArrayAdapter.createFromResource(this,
                R.array.years, android.R.layout.simple_list_item_1);
        yearAdapter.setDropDownViewResource(android.R.layout.simple_dropdown_item_1line);
        minYearSpinner.setAdapter(yearAdapter);
        maxYearSpinner.setAdapter(yearAdapter);
    }

    public void initialisePriceSpinners(){
        priceAdapter = ArrayAdapter.createFromResource(this,
                R.array.car_prices, android.R.layout.simple_list_item_1);
        priceAdapter.setDropDownViewResource(android.R.layout.simple_dropdown_item_1line);
        minPriceSpinner.setAdapter(priceAdapter);
        maxPriceSpinner.setAdapter(priceAdapter);
    }

    public void initialiseCountySpinner(){
        countyAdapter = ArrayAdapter.createFromResource(this,
                R.array.counties_list, android.R.layout.simple_list_item_1);
        countyAdapter.setDropDownViewResource(android.R.layout.simple_dropdown_item_1line);
        countySpinner.setAdapter(countyAdapter);
    }

    public void initialiseFuelTypeSpinner(){
        fuelTypeAdapter = ArrayAdapter.createFromResource(this,
                R.array.fuel_types, android.R.layout.simple_list_item_1);
        fuelTypeAdapter.setDropDownViewResource(android.R.layout.simple_dropdown_item_1line);
        fuelTypeSpinner.setAdapter(fuelTypeAdapter);
    }

    public class JSONTask extends AsyncTask<ArrayList<String>, String, String> {
        @Override
        protected String doInBackground(ArrayList<String>... params) {
            try {
                String model = params[0].get(1);
                model = model.replace(" ", ".");
                String minYear = params[0].get(2);
                String maxYear = params[0].get(3);
                String minPrice = params[0].get(4);
                String maxPrice = params[0].get(5);

                //Remove unwanted characters
                minPrice = minPrice.replace("€", "");
                minPrice = minPrice.replace(",", "");

                maxPrice = maxPrice.replace("€", "");
                maxPrice = maxPrice.replace(",", "");

                String County = params[0].get(6);
                if(County.equalsIgnoreCase("All Ireland"))
                    County = "County";

                String fuelType = params[0].get(7);
                if(fuelType.equalsIgnoreCase("All"))
                    fuelType = "Fuel";

                int minYearInt = Integer.parseInt(minYear);
                int maxYearInt = Integer.parseInt(maxYear);

                if (minYearInt > maxYearInt){
                    int tempYear = maxYearInt;
                    maxYearInt = minYearInt;
                    minYearInt = tempYear;
                }
                Scanner flaskScanner;// = new Scanner();
                while (maxYearInt >= minYearInt) {
                    //Get results by year
                    //URL connectToFlask = new URL(params[0]);
                    String start_of_url = "http://gdevlin.pythonanywhere.com/search_cars/";
                    String end_of_url = params[0].get(0) + "/" +
                                        model + "/" +
                                        String.valueOf(maxYearInt) + "/" +
                                        String.valueOf(maxYearInt) + "/" +
                                        minPrice + "/" +
                                        maxPrice + "/" +
                                        County + "/" +
                                        params[0].get(7);

                    String whole_url = start_of_url + end_of_url;
                    Log.d("pa_url", whole_url);

                    URL connectToFlask = new URL(whole_url);
                    HttpURLConnection connection;
                    connection = (HttpURLConnection) connectToFlask.openConnection();
                    connection.connect();

                    //Use buffer as it's slightly faster than scanner
                    BufferedReader flaskReader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                    StringBuffer buffer = new StringBuffer();
                    String line = "";
                    while ((line = flaskReader.readLine()) !=null)
                        flaskResult += line;

                    Log.d("flask result", flaskResult);
                    //connection.disconnect();
                    //flaskScanner.close();
                    maxYearInt--;
                }

                return flaskResult;
            } catch (java.io.IOException e) {
                e.printStackTrace();
            }
            return null;
        }

        @Override
        protected void onPostExecute(String flaskResult) {
            super.onPostExecute(flaskResult);
            string_car_urls = flaskResult;
            Intent browseCarsIntent = new Intent(getApplicationContext(), Browse_Cars_Activity.class);
            browseCarsIntent.putExtra("LIST_CARS_URL", string_car_urls);
            startActivity(browseCarsIntent);
        }
    }

    public ArrayList<String> searchClicked(){
        ArrayList<String> search_parameters = new ArrayList<String>();
        search_parameters.add(makeSpinner.getSelectedItem().toString());
        search_parameters.add(modelSpinner.getSelectedItem().toString());
        search_parameters.add(minYearSpinner.getSelectedItem().toString());
        search_parameters.add(maxYearSpinner.getSelectedItem().toString());
        search_parameters.add(minPriceSpinner.getSelectedItem().toString());
        search_parameters.add(maxPriceSpinner.getSelectedItem().toString());
        search_parameters.add(countySpinner.getSelectedItem().toString());
        search_parameters.add(fuelTypeSpinner.getSelectedItem().toString());

        return search_parameters;
    }
}
