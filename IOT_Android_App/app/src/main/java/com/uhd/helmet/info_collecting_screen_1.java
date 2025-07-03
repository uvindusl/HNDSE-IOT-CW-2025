package com.uhd.helmet;

import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.TextView;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

public class info_collecting_screen_1 extends AppCompatActivity {

    String age;
    String gender;

    String occupation;
    String workingPlace;

    String workingPlaceTel;

    EditText agetxt;

    RadioGroup gendergroup;
    EditText occupationtxt;
    EditText workingPlacetxt;

    EditText workingPlaceTeltxt;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_info_collecting_screen1);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        //assigning radio group by id
        gendergroup = findViewById(R.id.idRadioGroup);
        //Set listener on RadioGroup
        gendergroup.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(RadioGroup group, int checkedId) {
                //Find the selected RadioButton  by ID

                RadioButton radioButton = group.findViewById(checkedId);
                //RadioButton radioButton = findViewById(checkedId);

                //Set selected text to textView
                if(radioButton != null){
                    gender = radioButton.getText().toString();
                }
            }
        });
    }

    public void onPressActivate(View v){
        try {
            //assigning inputs by id
            agetxt = findViewById(R.id.editText5);
            occupationtxt = findViewById(R.id.editText7);
            workingPlacetxt = findViewById(R.id.editText8);
            workingPlaceTeltxt = findViewById(R.id.editText9);

            //get values from input
            age = agetxt.getText().toString();
            occupation = occupationtxt.getText().toString();
            workingPlace = workingPlacetxt.getText().toString();
            workingPlaceTel = workingPlaceTeltxt.getText().toString();

            //receiving data from previous page
            Intent intent = getIntent();
            String firstName = intent.getStringExtra("firstNameToInfo");
            String middleName = intent.getStringExtra("middleNameToInfo");
            String lastName = intent.getStringExtra("lastNameToInfo");
            String address = intent.getStringExtra("addressToInfo");
            String nic = intent.getStringExtra("nicToInfo");

            //pass values to next page
            Intent myIntent = new Intent(this, BikeDetails.class);
            myIntent.putExtra("firstNameToBike",firstName);
            myIntent.putExtra("middleNameToBike",middleName);
            myIntent.putExtra("lastNameToBike",lastName);
            myIntent.putExtra("addressToBike",address);
            myIntent.putExtra("nicToBike",nic);
            myIntent.putExtra("ageToBike",age);
            myIntent.putExtra("genderToBike",gender);
            myIntent.putExtra("occupationToBike",occupation);
            myIntent.putExtra("workingPlaceToBike",workingPlace);
            myIntent.putExtra("workingPlaceTelToBike",workingPlaceTel);

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
        startActivity(new Intent(info_collecting_screen_1.this, nameCollectingScreen.class));
    }

}