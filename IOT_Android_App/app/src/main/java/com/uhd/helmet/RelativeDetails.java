package com.uhd.helmet;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

import androidx.activity.EdgeToEdge;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.google.android.gms.tasks.OnFailureListener;
import com.google.firebase.firestore.FirebaseFirestore;

import java.util.HashMap;
import java.util.Map;

public class RelativeDetails extends AppCompatActivity {

    // Access a Cloud Firestore instance from your Activity
    FirebaseFirestore db = FirebaseFirestore.getInstance();

    String relativeName;
    int relativeTel;
    String relative2Name;
    int relative2el;

    EditText relativeNametxt;
    EditText relativeTeltxt;
    EditText relative2Nametxt;
    EditText relative2eltxt;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_relative_details);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });
    }

    public void back(View v){
        startActivity(new Intent(RelativeDetails.this, BikeDetails.class));
    }

    public void onPressActivate(View v){
        try{
            //assigning input by id
            relativeNametxt = findViewById(R.id.editText5);
            relativeTeltxt = findViewById(R.id.editText6);
            relative2Nametxt = findViewById(R.id.editText7);
            relative2eltxt = findViewById(R.id.editText8);

            //get values from input
            relativeName = relativeNametxt.getText().toString();
            relativeTel = Integer.parseInt(relativeTeltxt.getText().toString());
            relative2Name = relative2Nametxt.getText().toString();
            relative2el = Integer.parseInt(relative2eltxt.getText().toString());

            //recieving geta from previos page
            Intent intent = getIntent();
            String firstName = intent.getStringExtra("firstName");
            String middleName = intent.getStringExtra("middleName");
            String lastName = intent.getStringExtra("lastName");
            String address = intent.getStringExtra("address");
            String nic = intent.getStringExtra("nic");

            //put data to a hashmap
            Map<String, Object> rider = new HashMap<>();
            rider.put("first_name", firstName);
            rider.put("middle_name", middleName);
            rider.put("last_name", lastName);
            rider.put("address",address);
            rider.put("NIC",nic);

            //pass data to firebase
            db.collection("Riders")
            .add(rider)
            .addOnSuccessListener(documentReference -> {
                // Success callback
                System.out.println("Document added with ID: " + documentReference.getId());
            })
            .addOnFailureListener(new OnFailureListener() {
                @Override
                public void onFailure(@NonNull Exception e) {
                    Log.d("failure", "Error writing document", e);
                }
            });

        } catch (Exception e) {
            Log.d("catch", "Error writing document", e);
        }
    }
}