package com.uhd.helmet;

import static android.content.ContentValues.TAG;

import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.Firebase;
import com.google.firebase.firestore.CollectionReference;
import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.Query;
import com.google.firebase.firestore.QuerySnapshot;

import java.util.HashMap;
import java.util.Map;


public class MainActivity extends AppCompatActivity {
    TextView t2;
    String helmetID;
    EditText helmetIdText;
    Button activate;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });
        helmetIdText = findViewById(R.id.helmetIDtxt);
        activate = findViewById(R.id.activatebtn);
        t2 = findViewById(R.id.textView2);

        //database data retriever should be implemented on the main actvity since the onComplete method cant pass data outside its context.

    }
    public void onPressActivate(View v){
        helmetID = helmetIdText.getText().toString();
        FirebaseFirestore db = FirebaseFirestore.getInstance();
        CollectionReference collRef = db.collection("Activation");
        Query query = collRef.whereEqualTo("h_id", helmetID);
        query.get().addOnCompleteListener(task -> {
            if (task.isSuccessful()) {

                QuerySnapshot querySnapshot = task.getResult();
                if(querySnapshot != null && !querySnapshot.isEmpty()){
                    t2.setText("data found");
                    //pass values to next page
                    Intent myIntent = new Intent(this, nameCollectingScreen.class);
                    myIntent.putExtra("helmetIDToNameCollecting",helmetID);
                    try{
                        startActivity(myIntent);
                    }catch (ActivityNotFoundException e){
                        Log.d("passName","data passing failed",e);
                    }
                }else{
                    t2.setText("no data found");
                }
            }else{
                t2.setText("error");
            }
        });

    }
}