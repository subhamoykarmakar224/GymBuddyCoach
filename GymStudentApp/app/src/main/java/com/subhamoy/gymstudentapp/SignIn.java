package com.subhamoy.gymstudentapp;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Spinner;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import com.google.android.material.button.MaterialButton;
import com.google.android.material.textfield.TextInputLayout;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.Query;
import com.google.firebase.database.ValueEventListener;
import com.subhamoy.gymstudentapp.bean.Profile;

import java.util.ArrayList;

public class SignIn extends AppCompatActivity {

    TextInputLayout textInputPhone;
    MaterialButton btnLogin;
    Spinner spinnerGymIDs;

    private static final String KEY_PHONE = "phone";

    FirebaseDatabase databaseReference;
    AlertDialog.Builder alertBuilder;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sign_in);
//        setUIFlags();

        databaseReference = FirebaseDatabase.getInstance();

        // Widgets
        textInputPhone = findViewById(R.id.textInputPhone);
        btnLogin = findViewById(R.id.btnLogin);
        spinnerGymIDs = findViewById(R.id.spinnerGymIDs);
        alertBuilder = new AlertDialog.Builder(this);

        btnLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(!validatePhone()) {
                    return;
                }
                String phoneNo = textInputPhone.getEditText().getText().toString().trim();
                phoneNo = "+91" + phoneNo;
                String gymId = spinnerGymIDs.getSelectedItem().toString();
                if(gymId.equalsIgnoreCase("")) {
                    alertBuilder.setMessage("Please select your gym id to continue.")
                            .setPositiveButton("Ok",  null)
                            .setCancelable(false);
                    AlertDialog alertDialog = alertBuilder.create();;
                    alertDialog.show();
                } else {
                    checkIfNewUser(phoneNo, gymId);
                }

            }
        });

        initGYmIdsSpinner();
        btnLogin.setEnabled(false);
    }

    /**
     * Fill the Spinner with Gym IDs
     */
    private void initGYmIdsSpinner() {
        DatabaseReference dbRef = databaseReference.getReference(ConstantFBStudent.FB_TABLE_GYM_ADMIN);
        dbRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                ArrayList<String> arraySpinner = new ArrayList<>();
                arraySpinner.add("");
                for(DataSnapshot snap: dataSnapshot.getChildren()) {
                    arraySpinner.add(snap.getKey());
                }

                ArrayAdapter<String> adapter = new ArrayAdapter<String>(SignIn.this, android.R.layout.simple_spinner_item, arraySpinner);
                adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
                spinnerGymIDs.setAdapter(adapter);

                int paddingTB = 30;
                int paddingLR = 30;
                spinnerGymIDs.setPadding(paddingLR, paddingTB, paddingLR, paddingTB);

                btnLogin.setEnabled(true);
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });
    }

    /**
     * Checks if user exists
     * @param phone
     */
    private void checkIfNewUser(final String phone, final String gymId) {
        DatabaseReference dbRef = databaseReference.getReference(ConstantFBStudent.FB_TABLE_STUDENTS);
        Query query = dbRef
                .child(gymId)
                .orderByChild(KEY_PHONE)
                .equalTo(phone);
        query.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                if(!dataSnapshot.exists()) {
                    alertBuilder.setMessage("This User does not appear to be in our database. Please get in touch with your gym admin to continue using this app.")
                            .setPositiveButton("Ok",  null)
                            .setCancelable(false);
                    AlertDialog alertDialog = alertBuilder.create();;
                    alertDialog.show();
                } else {
                    Profile user = null;
                    String status = "";
                    for(DataSnapshot snap : dataSnapshot.getChildren()){
                        user = new Profile(
                                (String) snap.child(ConstantFBStudent.SID).getValue(),
                                (String) snap.child(ConstantFBStudent.studentName).getValue(),
                                (String) snap.child(ConstantFBStudent.studentAge).getValue(),
                                (String) snap.child(ConstantFBStudent.phone).getValue(),
                                (String) snap.child(ConstantFBStudent.membershipValidity).getValue(),
                                (String) snap.child(ConstantFBStudent.allottedTime).getValue()
                        );

                        status = (String) snap.child(ConstantFBStudent.membershipStatus).getValue();
                    }
                    Intent intent = new Intent(SignIn.this, OTPVerification.class);
                    intent.putExtra(ConstantFBStudent.SID, user.getId());
                    intent.putExtra(ConstantFBStudent.gymId, gymId);
                    intent.putExtra(ConstantFBStudent.studentName, user.getName());
                    intent.putExtra(ConstantFBStudent.studentAge, user.getAge());
                    intent.putExtra(ConstantFBStudent.phone, user.getPhone());
                    intent.putExtra(ConstantFBStudent.membershipValidity, user.getMembershipValidity());
                    intent.putExtra(ConstantFBStudent.allottedTime, user.getAllotedtime());
                    intent.putExtra(ConstantFBStudent.membershipStatus, status);
                    startActivity(intent);
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });
    }

    /**
     * Validate phone number
     * @return
     */
    private boolean validatePhone() {
        String phoneNo = textInputPhone.getEditText().getText().toString().trim();
        if(phoneNo.isEmpty() || phoneNo.length() != 10) {
            textInputPhone.setError("Please enter a valid phone number.");
            textInputPhone.requestFocus();
            return false;
        } else {
            textInputPhone.setError(null);
            textInputPhone.setErrorEnabled(false);
            return true;
        }
    }

    /**
     * UI Visibility flags
     */
    private void setUIFlags() {
        View decorView = getWindow().getDecorView();
        int uiOptions = View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                | View.SYSTEM_UI_FLAG_FULLSCREEN
                | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                | View.SYSTEM_UI_FLAG_LOW_PROFILE
                ;
        decorView.setSystemUiVisibility(uiOptions);
    }
}