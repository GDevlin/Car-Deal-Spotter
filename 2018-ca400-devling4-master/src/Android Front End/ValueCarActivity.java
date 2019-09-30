package dcu.ca400.devlin.glen.cardealspotter;

import android.content.DialogInterface;
import android.graphics.Color;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;

import java.net.HttpURLConnection;
import java.net.URL;
import java.text.DecimalFormat;
import java.util.Scanner;

public class ValueCarActivity extends AppCompatActivity {

    //Spinners
    private Spinner makeSpinner;
    private Spinner modelSpinner;
    private Spinner yearSpinner;
    private Spinner fuelTypeSpinner;
    private Spinner engineSizeSpinner;
    private Spinner colourSpinner;
    private Spinner bodySpinner;
    private Spinner ownersSpinner;
    private Spinner transmissionSpinner;

    private EditText odometerTextInput;

    //Adapters
    private ArrayAdapter<CharSequence> makeAdapter;
    private ArrayAdapter<CharSequence> modelAdapter;
    private ArrayAdapter<CharSequence> yearAdapter;
    private ArrayAdapter<CharSequence> fuelTypeAdapter;
    private ArrayAdapter<CharSequence> engineSizeAdapter;
    private ArrayAdapter<CharSequence> colourAdapter;
    private ArrayAdapter<CharSequence> bodyAdapter;
    private ArrayAdapter<CharSequence> ownersAdapter;
    private ArrayAdapter<CharSequence> transmissionAdapter;

    private String selected_make = "";
    private String userInput = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_value_car);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        toolbar.setTitle("Value Car");
        toolbar.setTitleTextColor(Color.WHITE);
        setSupportActionBar(toolbar);

        //Find views on screen
        makeSpinner = (Spinner) findViewById(R.id.makeSpinner);
        modelSpinner = (Spinner) findViewById(R.id.modelSpinner);
        yearSpinner = (Spinner) findViewById(R.id.yearSpinner);
        fuelTypeSpinner = (Spinner) findViewById(R.id.fuelTypeSpinner);
        engineSizeSpinner = (Spinner) findViewById(R.id.engineSizeSpinner);
        colourSpinner = (Spinner) findViewById(R.id.colourSpinner);
        bodySpinner = (Spinner) findViewById(R.id.bodySpinner);
        ownersSpinner = (Spinner) findViewById(R.id.ownersSpinner);
        transmissionSpinner = (Spinner) findViewById(R.id.transmissionSpinner);

        odometerTextInput = (EditText) findViewById(R.id.odometerTextInput);

        //Initialize spinners
        makeAdapter = ArrayAdapter.createFromResource(this,
                R.array.car_make_value, android.R.layout.simple_list_item_1);
        makeAdapter.setDropDownViewResource(android.R.layout.simple_dropdown_item_1line);
        makeSpinner.setAdapter(makeAdapter);
        makeSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                //getModelsForMake(i);
                selected_make = adapterView.getItemAtPosition(i).toString();
                getModelsForMake(selected_make);
            }
            @Override
            public void onNothingSelected(AdapterView<?> adapterView){

            }
        });

        //Spinners
        initialiseYearSpinner();
        initialiseFuelTypeSpinner();
        initialiseEngnineSizeSpinner();
        initialiseColourSpinner();
        initialiseBodySpinner();
        initialiseOwnersSpinner();
        initialiseTransmissionSpinner();


        //Connect to python anywhere button
        final Button valueCarButton = (Button) findViewById(R.id.valueCarButton);
        valueCarButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(makeSpinner.getSelectedItem().toString().equalsIgnoreCase("Make")) {
                    Toast.makeText(getApplicationContext(), "Choose Make", Toast.LENGTH_LONG).show();
                }
                else if(modelSpinner.getSelectedItem().toString().equalsIgnoreCase("Model")){
                    Toast.makeText(getApplicationContext(), "Choose Model", Toast.LENGTH_LONG).show();
                }
                else if(yearSpinner.getSelectedItem().toString().equalsIgnoreCase("Year")){
                    Toast.makeText(getApplicationContext(), "Choose Year", Toast.LENGTH_LONG).show();
                }
                else if(fuelTypeSpinner.getSelectedItem().toString().equalsIgnoreCase("Fuel Type")){
                    Toast.makeText(getApplicationContext(), "Choose Fuel Type", Toast.LENGTH_LONG).show();
                }
                else if(engineSizeSpinner.getSelectedItem().toString().equalsIgnoreCase("Engine Size")){
                    Toast.makeText(getApplicationContext(), "Choose Engine Size", Toast.LENGTH_LONG).show();
                }
                else if(colourSpinner.getSelectedItem().toString().equalsIgnoreCase("Colour")){
                    Toast.makeText(getApplicationContext(), "Choose Car Colour", Toast.LENGTH_LONG).show();
                }
                else if(bodySpinner.getSelectedItem().toString().equalsIgnoreCase("Body")){
                    Toast.makeText(getApplicationContext(), "Choose Car Body", Toast.LENGTH_LONG).show();
                }
                else if(ownersSpinner.getSelectedItem().toString().equalsIgnoreCase("Owners")){
                    Toast.makeText(getApplicationContext(), "Choose number of Owners", Toast.LENGTH_LONG).show();
                }
                else if(transmissionSpinner.getSelectedItem().toString().equalsIgnoreCase("Transmission")){
                    Toast.makeText(getApplicationContext(), "Choose Transmission", Toast.LENGTH_LONG).show();
                }
                else {
                    String end_of_url = valueCarClicked();
                    String start_of_url = "http://gdevlin.pythonanywhere.com/accept_car/";
                    String whole_url = start_of_url + end_of_url;
                    Log.d("url_output", whole_url);
                    new JSONTask().execute(whole_url);
                }
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
        else if(selected_make.equalsIgnoreCase("Make")) {
            modelAdapter = ArrayAdapter.createFromResource(this,
                    R.array.car_model_blank, android.R.layout.simple_list_item_1);
        }
        modelAdapter.setDropDownViewResource(android.R.layout.simple_dropdown_item_1line);
        modelAdapter.notifyDataSetChanged();
        modelSpinner.setAdapter(modelAdapter);
    }

    public void initialiseYearSpinner(){
        yearAdapter = ArrayAdapter.createFromResource(this,
                R.array.years_value, android.R.layout.simple_list_item_1);
        yearAdapter.setDropDownViewResource(android.R.layout.simple_dropdown_item_1line);
        yearSpinner.setAdapter(yearAdapter);
    }

    public void initialiseFuelTypeSpinner(){
        fuelTypeAdapter = ArrayAdapter.createFromResource(this,
                R.array.fuel_types_value, android.R.layout.simple_list_item_1);
        fuelTypeAdapter.setDropDownViewResource(android.R.layout.simple_dropdown_item_1line);
        fuelTypeSpinner.setAdapter(fuelTypeAdapter);
    }

    public void initialiseEngnineSizeSpinner(){
        engineSizeAdapter = ArrayAdapter.createFromResource(this,
                R.array.engine_sizes, android.R.layout.simple_list_item_1);
        engineSizeAdapter.setDropDownViewResource(android.R.layout.simple_dropdown_item_1line);
        engineSizeSpinner.setAdapter(engineSizeAdapter);
    }

    public void initialiseColourSpinner(){
        colourAdapter = ArrayAdapter.createFromResource(this,
                R.array.colours, android.R.layout.simple_list_item_1);
        colourAdapter.setDropDownViewResource(android.R.layout.simple_dropdown_item_1line);
        colourSpinner.setAdapter(colourAdapter);
    }

    public void initialiseBodySpinner(){
        bodyAdapter = ArrayAdapter.createFromResource(this,
                R.array.body_types, android.R.layout.simple_list_item_1);
        bodyAdapter.setDropDownViewResource(android.R.layout.simple_dropdown_item_1line);
        bodySpinner.setAdapter(bodyAdapter);
    }

    public void initialiseOwnersSpinner(){
        ownersAdapter = ArrayAdapter.createFromResource(this,
                R.array.owners, android.R.layout.simple_list_item_1);
        ownersAdapter.setDropDownViewResource(android.R.layout.simple_dropdown_item_1line);
        ownersSpinner.setAdapter(ownersAdapter);
    }

    public void initialiseTransmissionSpinner(){
        transmissionAdapter = ArrayAdapter.createFromResource(this,
                R.array.tranmissions, android.R.layout.simple_list_item_1);
        transmissionAdapter.setDropDownViewResource(android.R.layout.simple_dropdown_item_1line);
        transmissionSpinner.setAdapter(transmissionAdapter);
    }

    public String valueCarClicked(){
        String model_without_spaces = modelSpinner.getSelectedItem().toString();
        model_without_spaces = model_without_spaces.replace(' ', '.');
        String odometer = odometerTextInput.getText().toString();
        if(odometer.isEmpty())
            odometer = "0";
        odometer = convertToMiles(odometer);
        String owners = ownersSpinner.getSelectedItem().toString();
        if(owners.equalsIgnoreCase("5 or more"))
            owners = "5";

        userInput = makeSpinner.getSelectedItem().toString() + "/" +
                           model_without_spaces + "/" +
                           yearSpinner.getSelectedItem().toString() + "/" +
                           odometer + "/" +
                           fuelTypeSpinner.getSelectedItem().toString() + "/" +
                           engineSizeSpinner.getSelectedItem().toString() + "/" +
                           colourSpinner.getSelectedItem().toString() + "/" +
                           bodySpinner.getSelectedItem().toString() + "/" +
                           owners + "/" +
                           transmissionSpinner.getSelectedItem().toString();

        return userInput;
    }

    //Connect to pythonanywhere function to retrieve results
    public class JSONTask extends AsyncTask<String, String, String> {
        @Override
        protected String doInBackground(String... params) {
            String flaskResult = " ";
            try {
                URL connectToFlask = new URL(params[0]);
                HttpURLConnection connection;
                connection = (HttpURLConnection) connectToFlask.openConnection();
                connection.connect();

                Scanner flaskScanner = new Scanner(connectToFlask.openStream());
                while(flaskScanner.hasNext())
                    flaskResult += flaskScanner.next();
                connection.disconnect();
                flaskScanner.close();

                return flaskResult;
            } catch (java.io.IOException e) {
                e.printStackTrace();
            }
            return null;
        }

        //After you recieved the result, pop a dialog box to show it
        @Override
        protected void onPostExecute(String flaskResult) {
            super.onPostExecute(flaskResult);
            AlertDialog.Builder priceBuilder = new AlertDialog.Builder(ValueCarActivity.this);
            priceBuilder.setMessage("Estimated value of car is  " + convertToEuro(checkNegative(flaskResult)));
            priceBuilder.setPositiveButton("Okay", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialogInterface, int i) {
                    dialogInterface.dismiss();
                }
            });
            AlertDialog alertDialog = priceBuilder.create();
            alertDialog.show();
        }
    }

    //Convert the returned string to a euro format
    public String convertToEuro(String number){
        number = number.replace(" ", "");
        int numInt = Integer.parseInt(number);
        DecimalFormat properfomat = new DecimalFormat("#");
        properfomat.setGroupingUsed(true);
        properfomat.setGroupingSize(3);
        return String.valueOf("€" + properfomat.format(numInt));
    }

    //Check if number is negative and if so convert to zero
    public String checkNegative(String number){
        number = number.replace(" ", "");
        if(number.substring(0,1).equalsIgnoreCase("-"))
            return "0";
        else
            return number;
    }

    public String convertToMiles(String kilo){
        Double kiloDb = Double.parseDouble(kilo);
        kiloDb = kiloDb * .62;
        int miles = (int) Math.round(kiloDb);
        return String.valueOf(miles);
    }
}

