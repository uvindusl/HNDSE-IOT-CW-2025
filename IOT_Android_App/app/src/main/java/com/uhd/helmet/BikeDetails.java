package com.uhd.helmet;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

public class BikeDetails extends AppCompatActivity {

    String color;
    String model;
    String numberPlate;
    String insuranceCompany;
    int insuranceTel;

    EditText colortxt;
    EditText modeltxt;

    EditText numberPlatetxt;
    EditText insuranceCompanytxt;

    EditText insuranceTeltxt;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_bike_details);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });
    }

    public void onPressActivate(View v){

        //assigning input by id
        colortxt = findViewById(R.id.editText5);
        modeltxt = findViewById(R.id.editText6);
        numberPlatetxt = findViewById(R.id.editText7);
        insuranceCompanytxt = findViewById(R.id.editText8);
        insuranceTeltxt = findViewById(R.id.editText9);

        //get values from input
        color = colortxt.getText().toString();
        model = modeltxt.getText().toString();
        numberPlate = numberPlatetxt.getText().toString();
        insuranceCompany = insuranceCompanytxt.getText().toString();
        insuranceTel = Integer.parseInt(insuranceTeltxt.getText().toString());

        startActivity(new Intent(BikeDetails.this, RelativeDetails.class));
    }

    public void back(View v){
        startActivity(new Intent(BikeDetails.this, info_collecting_screen_1.class));
    }
}