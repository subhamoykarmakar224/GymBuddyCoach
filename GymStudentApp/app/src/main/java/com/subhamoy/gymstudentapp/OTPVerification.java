package com.subhamoy.gymstudentapp;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.android.gms.tasks.TaskExecutors;
import com.google.android.material.button.MaterialButton;
import com.google.android.material.textfield.TextInputLayout;
import com.google.android.material.textview.MaterialTextView;
import com.google.firebase.FirebaseException;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.PhoneAuthCredential;
import com.google.firebase.auth.PhoneAuthProvider;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

import java.util.concurrent.TimeUnit;

public class OTPVerification extends AppCompatActivity {

    private static final int TIME_TILL_VALID_OTP = 120;
    private static final String MY_PREFS_NAME = "gymstudentapp_students";

    TextView textViewMsg;
    TextInputLayout textInputOtp;
    MaterialButton btnRegister, btnResendOTP;
    MaterialTextView textViewTimer;
    ProgressBar progressBar;

    private String verficationID;
    private FirebaseAuth mAuth;
    private DatabaseReference databaseRefUser;

    String id;
    String gymId;
    String name;
    String age;
    String phoneNo;
    String membership;
    String allotedTime;

    boolean secondTry;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_otp_verification);

        Intent intent = getIntent();
        id = intent.getStringExtra(ConstantFBStudent.SID);
        gymId = intent.getStringExtra(ConstantFBStudent.gymId);
        name = intent.getStringExtra(ConstantFBStudent.studentName);
        age = intent.getStringExtra(ConstantFBStudent.studentAge);
        phoneNo = intent.getStringExtra(ConstantFBStudent.phone);
        membership = intent.getStringExtra(ConstantFBStudent.membershipValidity);
        allotedTime = intent.getStringExtra(ConstantFBStudent.allottedTime);

        // Widgets
        textViewMsg = findViewById(R.id.textViewMsg);
        textInputOtp = findViewById(R.id.textInputOtp);
        btnRegister = findViewById(R.id.btnRegister);
        btnResendOTP = findViewById(R.id.btnResendOTP);
        progressBar = findViewById(R.id.progressBar);
        textViewTimer = findViewById(R.id.textViewTimer);

        // Firebase
        mAuth = FirebaseAuth.getInstance();
        databaseRefUser = FirebaseDatabase.getInstance().getReference();

        setButtonDisable(btnResendOTP);

        sendVerification(phoneNo);

        btnRegister.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String code = textInputOtp.getEditText().getText().toString().trim();
                if (code.isEmpty()) {
                    textInputOtp.setError("Enter complete code...");
                    textInputOtp.requestFocus();
                    return;
                }
                verifyCode(code);
            }
        });

        btnResendOTP.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(!secondTry) {
                    secondTry = true;
                    sendVerification(phoneNo);
                } else {
                    Toast.makeText(OTPVerification.this, "Please try again later. I think we might ", Toast.LENGTH_SHORT).show();
                }
            }
        });

        textViewMsg.setText("Hi, " + name + "\nPlease wait while we verify your phone: " + phoneNo);
    }

    private void sendVerification(String number) {
        progressBar.setVisibility(View.VISIBLE);
        showToast(this);
        TimerThread thread = new TimerThread(TIME_TILL_VALID_OTP);
        thread.start();
        PhoneAuthProvider.getInstance().verifyPhoneNumber(
                number,
                TIME_TILL_VALID_OTP,
                TimeUnit.SECONDS,
                TaskExecutors.MAIN_THREAD,
                mCallBack
        );
    }

    private void verifyCode(String code) {
        PhoneAuthCredential credential = PhoneAuthProvider.getCredential(
                verficationID, code
        );
        signInWithCredential(credential);
    }

    private void signInWithCredential(PhoneAuthCredential credential) {
        mAuth.signInWithCredential(credential)
                .addOnCompleteListener(new OnCompleteListener<AuthResult>() {
                    @Override
                    public void onComplete(@NonNull Task<AuthResult> task) {
                        if (task.isSuccessful()) {

                            // Insert to SharedPreference
                            SharedPreferences.Editor editor = getSharedPreferences(MY_PREFS_NAME, MODE_PRIVATE).edit();
                            editor.putString(ConstantFBStudent.SID, id);
                            editor.putString(ConstantFBStudent.gymId, gymId);
                            editor.putString(ConstantFBStudent.studentName, name);
                            editor.putString(ConstantFBStudent.studentAge, age);
                            editor.putString(ConstantFBStudent.phone, phoneNo);
                            editor.putString(ConstantFBStudent.membershipValidity, membership);
                            editor.putString(ConstantFBStudent.allottedTime, allotedTime);
                            editor.apply();

                            // Redirect to MainActivity
                            Intent intent = new Intent(OTPVerification.this, MainActivity.class);
                            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                            startActivity(intent);
                        } else {
                            Toast.makeText(OTPVerification.this, "ERROR :: " + task.getException().getMessage(), Toast.LENGTH_LONG).show();
                        }
                    }
                });
    }

    private PhoneAuthProvider.OnVerificationStateChangedCallbacks
            mCallBack = new PhoneAuthProvider.OnVerificationStateChangedCallbacks() {
        @Override
        public void onVerificationCompleted(@NonNull PhoneAuthCredential phoneAuthCredential) {
            String code = phoneAuthCredential.getSmsCode();
            if (code != null) {
                textInputOtp.getEditText().setText(code);
                verifyCode(code);
            }
        }

        @Override
        public void onVerificationFailed(@NonNull FirebaseException e) {
            Toast.makeText(OTPVerification.this, "ERROR :: " + e.getMessage(), Toast.LENGTH_LONG).show();
        }

        @Override
        public void onCodeSent(@NonNull String s, @NonNull PhoneAuthProvider.ForceResendingToken forceResendingToken) {
            super.onCodeSent(s, forceResendingToken);
            verficationID = s;
        }
    };

    /**
     * Set disabled button UI
     * @param btn
     */
    public void setButtonDisable(MaterialButton btn) {
        btn.setBackgroundColor(getResources().getColor(R.color.colorbgLightGrey));
        btn.setTextColor(getResources().getColor(R.color.colorShadow));
        btn.setEnabled(false);
    }

    /**
     * Set enabled button UI
     * @param btn
     */
    public void setButtonEnable(MaterialButton btn) {
        btn.setBackgroundColor(getResources().getColor(R.color.white));
        btn.setTextColor(getResources().getColor(R.color.colorPrimary));
        btn.setEnabled(true);
    }

    public void showToast(Context c) {
        Toast.makeText(c, "Request for OTP sent!", Toast.LENGTH_SHORT).show();
    }

    /**
     * Thread Timer Class
     */
    class TimerThread extends Thread {

        int seconds;

        TimerThread(int seconds) {
            this.seconds = seconds;
        }

        @Override
        public void run() {
            for(int i = 0 ;i < seconds ; i++) {
                int leftSec = TIME_TILL_VALID_OTP - i;
                int minutes = (leftSec% 3600) / 60;
                int seconds = leftSec % 60;
                if(seconds < 10){
                    textViewTimer.setText("Time Left : " + minutes + ":0" + seconds);
                } else {
                    textViewTimer.setText("Time Left : " + minutes + ":" + seconds);
                }
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }

            textViewTimer.setText("Time Left : 0:00");

            // Update the resend OTP button after timer runs out
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    setButtonEnable(btnResendOTP);
                }
            });

        }
    }
}