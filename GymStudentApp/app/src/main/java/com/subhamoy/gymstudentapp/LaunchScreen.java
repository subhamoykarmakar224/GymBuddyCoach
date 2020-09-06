package com.subhamoy.gymstudentapp;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.Query;
import com.google.firebase.database.ValueEventListener;
import com.subhamoy.gymstudentapp.bean.Profile;

public class LaunchScreen extends AppCompatActivity {

    SharedPreferences sp;
    DatabaseReference databaseRefUsers;
    private static final String MY_PREFS_NAME = "gymstudentapp_students";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_launch_screen);
        setUIFlags();
        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                sp = getApplicationContext().getSharedPreferences(MY_PREFS_NAME, Context.MODE_PRIVATE);
                isUserLoggedIn();
            }
        }, 3000);
    }

    /**
     * Checks if the User is logged in or not
     */
    private void isUserLoggedIn() {
        if (FirebaseAuth.getInstance().getCurrentUser() != null) {
            Log.i("olla", "Logged in User : " + FirebaseAuth.getInstance().getCurrentUser().getPhoneNumber());
            Intent intent = new Intent(LaunchScreen.this, MainActivity.class);
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
            checkUserMetaInfo();
            startActivity(intent);
        } else {
            Intent intent = new Intent(LaunchScreen.this, SignIn.class);
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
            startActivity(intent);
        }
    }

    /**
     * Checks the meta information for changes in server for the current user
     */
    private void checkUserMetaInfo() {
        final String gymId = sp.getString(ConstantFBStudent.gymId, "");
        String sid = sp.getString(ConstantFBStudent.SID, "");
        final String name = sp.getString(ConstantFBStudent.studentName, "");
        final String age = sp.getString(ConstantFBStudent.studentAge, "");
        final String validity = sp.getString(ConstantFBStudent.membershipValidity, "");
        final String allotedTime = sp.getString(ConstantFBStudent.allottedTime, "");
        final String phone = sp.getString(ConstantFBStudent.phone, "");

//        DatabaseReference dbRef = databaseReference.getReference(ConstantFBStudent.FB_TABLE_STUDENTS);
//        Query query = dbRef
//                .child(gymId)
//                .orderByChild(KEY_PHONE)
//                .equalTo(phone);

        Log.i("olla", "Gym ID to check :: " + gymId);
        databaseRefUsers = FirebaseDatabase.getInstance().getReference(ConstantFBStudent.FB_TABLE_STUDENTS);
        Query query = databaseRefUsers
                .child(gymId)
                .orderByChild(ConstantFBStudent.SID)
                .equalTo(sid);

        query.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                if (!dataSnapshot.exists()) {
                    // Delete from local DB
                    SharedPreferences.Editor editor = sp.edit();
                    editor.clear();
                    editor.apply();

                    // Sign out user
                    FirebaseAuth.getInstance().signOut();

                    // Redirect User
                    Intent intent = new Intent(LaunchScreen.this, SignIn.class);
                    intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                    startActivity(intent);
                } else {
                    Profile user = null;
                    String status = "";
                    for (DataSnapshot snap : dataSnapshot.getChildren()) {
                        user = new Profile(
                                (String) snap.child(ConstantFBStudent.SID).getValue(),
                                (String) snap.child(ConstantFBStudent.studentName).getValue(),
                                (String) snap.child(ConstantFBStudent.studentAge).getValue(),
                                (String) snap.child(ConstantFBStudent.phone).getValue(),
                                (String) snap.child(ConstantFBStudent.membershipValidity).getValue(),
                                (String) snap.child(ConstantFBStudent.allottedTime).getValue()
                        );
                        status = String.valueOf(snap.child(ConstantFBStudent.membershipStatus).getValue());
                    }

                    SharedPreferences.Editor editor = sp.edit();

                    String tmpStatusString = sp.getString(ConstantFBStudent.membershipStatus, "");
                    if (!status.equalsIgnoreCase(tmpStatusString)) {
                        editor.remove(ConstantFBStudent.membershipStatus);
                        editor.commit();
                        editor.putString(ConstantFBStudent.membershipStatus, status);
                        editor.apply();
                    }

                    if(!phone.equalsIgnoreCase(user.getPhone())) {
                        editor.remove(ConstantFBStudent.phone);
                        editor.commit();
                        editor.putString(ConstantFBStudent.phone, user.getPhone());
                        editor.apply();
                        FirebaseAuth.getInstance().signOut();
                    }

                    if (!user.getName().equalsIgnoreCase(name)) {
                        editor.remove(ConstantFBStudent.studentName);
                        editor.commit();
                        editor.putString(ConstantFBStudent.studentName, user.getName());
                        editor.apply();
                    }

                    if (!user.getAge().equalsIgnoreCase(age)) {
                        editor.remove(ConstantFBStudent.studentAge);
                        editor.commit();
                        editor.putString(ConstantFBStudent.studentAge, user.getAge());
                        editor.apply();
                    }

                    if (!user.getMembershipValidity().equalsIgnoreCase(validity)) {
                        editor.remove(ConstantFBStudent.membershipValidity);
                        editor.commit();
                        editor.putString(ConstantFBStudent.membershipValidity, user.getMembershipValidity());
                        editor.apply();
                    }

                    if (!user.getAllotedtime().equalsIgnoreCase(allotedTime)) {
                        editor.remove(ConstantFBStudent.allottedTime);
                        editor.commit();
                        editor.putString(ConstantFBStudent.allottedTime, user.getAllotedtime());
                        editor.apply();
                    }
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });

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
                | View.SYSTEM_UI_FLAG_LOW_PROFILE;
        decorView.setSystemUiVisibility(uiOptions);
    }
}