package com.uhd.helmet;

import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
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
    String insuranceTel;

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

        try{
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
            insuranceTel = insuranceTeltxt.getText().toString();

            //receiving gata from previous page
            Intent intent = getIntent();
            String firstName = intent.getStringExtra("firstNameToBike");
            String middleName = intent.getStringExtra("middleNameToBike");
            String lastName = intent.getStringExtra("lastNameToBike");
            String address = intent.getStringExtra("addressToBike");
            String nic = intent.getStringExtra("nicToBike");
            String age = intent.getStringExtra("ageToBike");
            String gender = intent.getStringExtra("genderToBike");
            String occupation = intent.getStringExtra("occupationToBike");
            String workingPlace = intent.getStringExtra("workingPlaceToBike");
            String workingPlaceTel = intent.getStringExtra("workingPlaceTelToBike");

            //pass values to next page
            Intent myIntent = new Intent(this, RelativeDetails.class);
            myIntent.putExtra("firstNameToRelative",firstName);
            myIntent.putExtra("middleNameToRelative",middleName);
            myIntent.putExtra("lastNameToRelative",lastName);
            myIntent.putExtra("addressToRelative",address);
            myIntent.putExtra("nicToRelative",nic);
            myIntent.putExtra("ageToRelative",age);
            myIntent.putExtra("genderToRelative",gender);
            myIntent.putExtra("occupationToRelative",occupation);
            myIntent.putExtra("workingPlaceToRelative",workingPlace);
            myIntent.putExtra("workingPlaceTelToRelative",workingPlaceTel);
            myIntent.putExtra("colorToRelative",color);
            myIntent.putExtra("modelToRelative",model);
            myIntent.putExtra("numberPlateToRelative",numberPlate);
            myIntent.putExtra("insuranceCompanyToRelative",insuranceCompany);
            myIntent.putExtra("insuranceTelToRelative",insuranceTel);

            try{
                startActivity(myIntent);
            }catch (ActivityNotFoundException e){
                Log.d("passName","data passing failed",e);
            }

        }catch (Exception e) {
            Log.d("catch", "Error writing document", e);
        }

    }

    public void back(View v){
        startActivity(new Intent(BikeDetails.this, info_collecting_screen_1.class));
    }
}