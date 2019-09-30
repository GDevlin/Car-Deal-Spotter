package dcu.ca400.devlin.glen.cardealspotter;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button browseCarButton = (Button)findViewById(R.id.browse_cars_button);
        Button valueCarButtin = (Button)findViewById(R.id.value_car_button);

        //Buttons to launch those activities
        browseCarButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent carSearchIntent = new Intent(getApplicationContext(), CarSearchActivity.class);
                startActivity(carSearchIntent);
            }
        });

        valueCarButtin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent valueCarIntent = new Intent(getApplicationContext(), ValueCarActivity.class);
                startActivity(valueCarIntent);
            }
        });
    }
}
