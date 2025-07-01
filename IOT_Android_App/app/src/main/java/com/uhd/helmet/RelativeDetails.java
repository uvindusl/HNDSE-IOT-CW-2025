package com.uhd.helmet;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;

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

            Rider R1 = new Rider();

            Map<String, Object> rider = new HashMap<>();
            rider.put("first_name", R1.getFirstName());
            rider.put("middle_name", R1.getMiddleName());
            rider.put("last_name", R1.getLastName());
            rider.put("address",R1.getAddress());
            rider.put("NIC",R1.getNic());

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