package com.uhd.helmet;

import static android.content.ContentValues.TAG;

import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.annotation.NonNull;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.FirebaseFirestore;

import java.time.LocalDate;
import java.util.HashMap;
import java.util.Map;

public class RelativeDetails extends AppCompatActivity {

    // Access a Cloud Firestore instance from your Activity
    FirebaseFirestore db = FirebaseFirestore.getInstance();

    String relativeName;
    String relativeTel;
    String relative2Name;
    String relative2el;

    EditText relativeNametxt;
    EditText relativeTeltxt;
    EditText relative2Nametxt;
    EditText relative2eltxt;
    LocalDate currentDate;

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

    @RequiresApi(api = Build.VERSION_CODES.O)
    public void onPressActivate(View v){
        try{
            //assigning input by id
            relativeNametxt = findViewById(R.id.editText5);
            relativeTeltxt = findViewById(R.id.editText6);
            relative2Nametxt = findViewById(R.id.editText7);
            relative2eltxt = findViewById(R.id.editText8);

            //get values from input
            relativeName = relativeNametxt.getText().toString();
            relativeTel = relativeTeltxt.getText().toString();
            relative2Name = relative2Nametxt.getText().toString();
            relative2el = relative2eltxt.getText().toString();
            currentDate = LocalDate.now();

            //receiving data from previous page
            Intent intent = getIntent();
            String helmetID = intent.getStringExtra("helmetIDToRelative");
            String firstName = intent.getStringExtra("firstNameToRelative");
            String middleName = intent.getStringExtra("middleNameToRelative");
            String lastName = intent.getStringExtra("lastNameToRelative");
            String address = intent.getStringExtra("addressToRelative");
            String nic = intent.getStringExtra("nicToRelative");
            String age = intent.getStringExtra("ageToRelative");
            String gender = intent.getStringExtra("genderToRelative");
            String occupation = intent.getStringExtra("occupationToRelative");
            String workingPlace = intent.getStringExtra("workingPlaceToRelative");
            String workingPlaceTel = intent.getStringExtra("workingPlaceTelToRelative");
            String color = intent.getStringExtra("colorToRelative");
            String model = intent.getStringExtra("modelToRelative");
            String numberPlate = intent.getStringExtra("numberPlateToRelative");
            String insuranceCompany = intent.getStringExtra("insuranceCompanyToRelative");
            String insuranceTel = intent.getStringExtra("insuranceTelToRelative");

            //put data to a hashmap
            Map<String, Object> rider = new HashMap<>();
            rider.put("h_id", helmetID);
            rider.put("first_name", firstName);
            rider.put("middle_name", middleName);
            rider.put("last_name", lastName);
            rider.put("address",address);
            rider.put("NIC",nic);
            rider.put("age", age);
            rider.put("Gender", gender);
            rider.put("occupation", occupation);
            rider.put("working_place",workingPlace);
            rider.put("working_place_tel",workingPlaceTel);
            rider.put("bike_color", color);
            rider.put("bike_model", model);
            rider.put("number_plate",numberPlate);
            rider.put("insuarance_company",insuranceCompany);
            rider.put("insuarance_tel",insuranceTel);

            //pass rider data to firebase
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

            //update the activated date
            assert helmetID != null;
            DocumentReference activationRef = db.collection("Activation").document(helmetID);
            activationRef
                    .update("activated_day",currentDate)
                    .addOnSuccessListener(new OnSuccessListener<Void>(){
                        @Override
                        public void onSuccess(Void aVoid) {
                            Log.d(TAG, "DocumentSnapshot successfully updated!");
                            Toast.makeText(RelativeDetails.this, "Activation Success", Toast.LENGTH_SHORT).show();
                        }
                    })
                    .addOnFailureListener(new OnFailureListener() {
                        @Override
                        public void onFailure(@NonNull Exception e) {
                            Log.w(TAG,"Error updating document", e);
                        }
                    });

            //Redirecting to first page
            startActivity(new Intent(RelativeDetails.this, MainActivity.class));

        } catch (Exception e) {
            Log.d("catch", "Error writing document", e);
        }
    }
}