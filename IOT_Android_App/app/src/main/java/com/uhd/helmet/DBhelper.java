package com.uhd.helmet;


import static android.content.ContentValues.TAG;

import android.util.Log;
import android.widget.Toast;

import androidx.annotation.NonNull;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.QueryDocumentSnapshot;
import com.google.firebase.firestore.QuerySnapshot;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class DBhelper{
    String HID;
    String UID;
    String ACD;
    FirebaseFirestore db = FirebaseFirestore.getInstance();
    Map<String, Object> data = new HashMap<>();

    public void addData(String helmet_id) {
        data.put("h_id", helmet_id);
        data.put("user_id", "u003");
        data.put("activated_day", "25-06-99");
        db.collection("Activation")
                .add(data)
                .addOnSuccessListener(documentReference -> {


                })
                .addOnFailureListener(e -> {

                });
    }



}
