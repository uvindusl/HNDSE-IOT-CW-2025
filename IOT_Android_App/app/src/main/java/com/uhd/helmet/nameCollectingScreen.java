package com.uhd.helmet;

import static android.content.ContentValues.TAG;

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

            firstNametxt = findViewById(R.id.editText5);
            middleNametxt = findViewById(R.id.editText6);
            lastNametxt = findViewById(R.id.editText7);
            addresstxt = findViewById(R.id.editText8);
            nictxt = findViewById(R.id.editText9);

            firstName = firstNametxt.getText().toString();
            middleName = middleNametxt.getText().toString();
            lastName = lastNametxt.getText().toString();
            address = lastNametxt.getText().toString();
            nic = lastNametxt.getText().toString();

            Rider R1 = new Rider();

            R1.setFirstName(firstName);
            R1.setMiddleName(middleName);
            R1.setLastName(lastName);
            R1.setAddress(address);
            R1.setNic(nic);

//            Map<String, Object> rider = new HashMap<>();
//            rider.put("first_name", R1.getFirstName());
//            rider.put("middle_name", R1.getMiddleName());
//            rider.put("last_name", R1.getLastName());
//            rider.put("address",R1.getAddress());
//            rider.put("NIC",R1.getNic());

//            db.collection("Riders")
//                    .add(rider)
//                    .addOnSuccessListener(documentReference -> {
//                        // Success callback
//                        System.out.println("Document added with ID: " + documentReference.getId());
//                    })
//                    .addOnFailureListener(new OnFailureListener() {
//                        @Override
//                        public void onFailure(@NonNull Exception e) {
//                            Log.d("failure", "Error writing document", e);
//                        }
//                    });

        } catch (Exception e) {
            Log.d("catch", "Error writing document", e);
        }

        //directing to next page
        startActivity(new Intent(nameCollectingScreen.this, info_collecting_screen_1.class));
    }

    public void back(View v){
        startActivity(new Intent(nameCollectingScreen.this, MainActivity.class));
    }
}