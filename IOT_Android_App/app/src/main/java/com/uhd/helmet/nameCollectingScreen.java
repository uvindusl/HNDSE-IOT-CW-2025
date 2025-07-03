package com.uhd.helmet;

import static android.content.ContentValues.TAG;

import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;


import androidx.activity.EdgeToEdge;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.firestore.FirebaseFirestore;

import java.util.HashMap;
import java.util.Map;

public class nameCollectingScreen extends AppCompatActivity {

    String firstName;
    String middleName;
    String lastName;
    String address;
    String nic;
    EditText firstNametxt;
    EditText middleNametxt;
    EditText lastNametxt;

    EditText addresstxt;
    EditText nictxt;



    // Access a Cloud Firestore instance from your Activity
//    FirebaseFirestore db = FirebaseFirestore.getInstance();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_name_collecting_screen);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });
    }

    public void onPressActivate(View v){

        try {
            //assigning edit texts by id
            firstNametxt = findViewById(R.id.editText5);
            middleNametxt = findViewById(R.id.editText6);
            lastNametxt = findViewById(R.id.editText7);
            addresstxt = findViewById(R.id.editText8);
            nictxt = findViewById(R.id.editText9);

            //get values from input
            firstName = firstNametxt.getText().toString();
            middleName = middleNametxt.getText().toString();
            lastName = lastNametxt.getText().toString();
            address = lastNametxt.getText().toString();
            nic = lastNametxt.getText().toString();

            //pass values to next page
            Intent myIntent = new Intent(this, info_collecting_screen_1.class);
            myIntent.putExtra("firstNameToInfo",firstName);
            myIntent.putExtra("middleNameToInfo",middleName);
            myIntent.putExtra("lastNameToInfo",lastName);
            myIntent.putExtra("addressToInfo",address);
            myIntent.putExtra("nicToInfo",nic);

            try{
                startActivity(myIntent);
            }catch (ActivityNotFoundException e){
                Log.d("passName","data passing failed",e);
            }
        } catch (Exception e) {
            Log.d("catch", "Error writing document", e);
        }
    }

    public void back(View v){
        startActivity(new Intent(nameCollectingScreen.this, MainActivity.class));

    }
}