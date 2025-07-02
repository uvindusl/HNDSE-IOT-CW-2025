package com.uhd.helmet;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
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

            Intent intent = getIntent();
            String firstName = intent.getStringExtra("firstName");
            String middleName = intent.getStringExtra("middleName");
            String lastName = intent.getStringExtra("lastName");
            String address = intent.getStringExtra("address");
            String nic = intent.getStringExtra("nic");

//            TextView reciveTextView = findViewById(R.id.textView19);
//            // reciveTextView.setText(passMsg + String.valueOf(thisYear));
//
//            reciveTextView.setText(passMsg);

            Map<String, Object> rider = new HashMap<>();
            rider.put("first_name", firstName);
            rider.put("middle_name", middleName);
            rider.put("last_name", lastName);
            rider.put("address",address);
            rider.put("NIC",nic);

//            Map<String, Object> rider = new HashMap<>();
//            rider.put("first_name", R1.getFirstName());
//            rider.put("middle_name", R1.getMiddleName());
//            rider.put("last_name", R1.getLastName());
//            rider.put("address",R1.getAddress());
//            rider.put("NIC",R1.getNic());

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