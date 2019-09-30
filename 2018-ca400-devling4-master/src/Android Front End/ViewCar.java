package dcu.ca400.devlin.glen.cardealspotter;

import android.content.Intent;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.text.DecimalFormat;
import java.util.ArrayList;

public class ViewCar extends AppCompatActivity {

    ArrayList<String> car_features = new ArrayList<>();

    private TextView makeTextView;
    private TextView modelTextView;
    private TextView yearTextView;
    private TextView priceTextView;
    private TextView valueTextView;
    private TextView priceDiffTextView;
    private TextView countyTextView;
    private TextView engineSizeTextView;
    private TextView fuelTypeTextView;
    private TextView odometerTextView;
    private TextView colourTextView;
    private TextView transmissionTextView;
    private TextView ownersTextView;
    private TextView bodyTextView;
    private TextView roadTaxTextView;
    private TextView fuelEconomyTextView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_car);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        toolbar.setTitle("View Car");
        toolbar.setTitleTextColor(Color.WHITE);
        setSupportActionBar(toolbar);

        car_features = getIntent().getStringArrayListExtra("Car Features");
        Log.d("car feat", String.valueOf(car_features));

        //Find text views
        makeTextView = (TextView) findViewById(R.id.makeTextView);
        modelTextView = (TextView) findViewById(R.id.modelTextview);
        yearTextView = (TextView) findViewById(R.id.yearTextView);
        priceTextView = (TextView) findViewById(R.id.priceTextView);
        valueTextView = (TextView) findViewById(R.id.valueTextView);
        priceDiffTextView = (TextView) findViewById(R.id.priceDiffTextView);
        countyTextView = (TextView) findViewById(R.id.countyTextView);
        engineSizeTextView = (TextView) findViewById(R.id.engineSizeTextView);
        fuelTypeTextView = (TextView) findViewById(R.id.fuelTypeTextView);
        odometerTextView = (TextView) findViewById(R.id.odometerTextView);
        colourTextView = (TextView) findViewById(R.id.colourTextView);
        transmissionTextView = (TextView) findViewById(R.id.transmissionTextView);
        ownersTextView = (TextView) findViewById(R.id.ownersTextView);
        bodyTextView = (TextView) findViewById(R.id.bodyTextView);
        roadTaxTextView = (TextView) findViewById(R.id.roadTaxTextView);
        fuelEconomyTextView = (TextView) findViewById(R.id.fuelEconomyTextView);


        //Set TextViews
        makeTextView.setText(car_features.get(2));
        modelTextView.setText(car_features.get(3));
        String carYear = car_features.get(4).substring(0,4);
        yearTextView.setText(carYear);
        priceTextView.setText(convertNumberToCurrency(car_features.get(5)));
        odometerTextView.setText(getKilometresForMiles(car_features.get(6)));
        fuelTypeTextView.setText(car_features.get(7));
        engineSizeTextView.setText(car_features.get(8));
        colourTextView.setText(capitaliseWord(car_features.get(9)));
        bodyTextView.setText(car_features.get(10));
        ownersTextView.setText(car_features.get(11));
        transmissionTextView.setText(car_features.get(12));
        countyTextView.setText(car_features.get(13));
        roadTaxTextView.setText(convertNumberToCurrency(car_features.get(14)));
        fuelEconomyTextView.setText(car_features.get(15) + " MPG");
        valueTextView.setText(convertNumberToCurrency(car_features.get(16)));
        priceDiffTextView.setText(convertNumberToCurrency(car_features.get(17)));
        //countyTextView.setText("Dublin");

        //Open carsIreland to view the ad
        Button launchURLButton = (Button) findViewById(R.id.launchURLButton);
        launchURLButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent launchBrowser = new Intent(Intent.ACTION_VIEW, Uri.parse(car_features.get(0)));
                startActivity(launchBrowser);
            }
        });
    }

    public String convertNumberToCurrency(String number){
        float numFloat = Float.parseFloat(number);
        int numInt = (int) numFloat;
        numInt = Math.abs(numInt);
        DecimalFormat properfomat = new DecimalFormat("#");
        properfomat.setGroupingUsed(true);
        properfomat.setGroupingSize(3);
        return String.valueOf("€" + properfomat.format(numInt));
    }

    public String getKilometresForMiles(String miles){
        int milesInt = Integer.parseInt(miles);
        double km = milesInt * 1.60934;
        int kmInt =(int) Math.round(km);
        return miles + " miles/ " + String.valueOf(kmInt) + " kilometres";
    }

    public String capitaliseWord(String word){
        return word.substring(0,1).toUpperCase() + word.substring(1).toLowerCase();
    }
}
