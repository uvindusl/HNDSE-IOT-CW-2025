package com.uhd.helmet;

import android.content.Intent;
import android.os.Bundle;
import android.provider.MediaStore;
import android.view.View;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.RadioGroup;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

public class info_collecting_screen_1 extends AppCompatActivity {

    int age;
    String gender;

    String occupation;
    String workingPlace;

    int workingPlaceTel;

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
    }

    public void onPressActivate(View v){
        //assigning inputs by id
        agetxt = findViewById(R.id.editText5);
        gendergroup = findViewById(R.id.idRadioGroup);
        occupationtxt = findViewById(R.id.editText7);
        workingPlacetxt = findViewById(R.id.editText8);
        workingPlaceTeltxt = findViewById(R.id.editText9);

        //get values from input
        age = Integer.parseInt(agetxt.getText().toString());
        //Set listener on RadioGroup
        gendergroup.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(RadioGroup group, int checkedId) {
                //Find the selected RadioButton  by ID
                RadioButton radioButton = group.findViewById(checkedId);

                //Set selected text to textView
                if(radioButton != null){
                    gender = radioButton.getText().toString();
                }
            }
        });
        occupation = occupationtxt.getText().toString();
        workingPlace = workingPlacetxt.getText().toString();
        workingPlaceTel = Integer.parseInt(workingPlaceTeltxt.getText().toString());

        startActivity(new Intent(info_collecting_screen_1.this, BikeDetails.class));
    }

    public void back(View v){
        startActivity(new Intent(info_collecting_screen_1.this, nameCollectingScreen.class));
    }

}