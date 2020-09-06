package com.subhamoy.gymstudentapp;

import android.app.PendingIntent;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageButton;
import android.widget.ListView;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.google.android.gms.ads.AdRequest;
import com.google.android.gms.ads.AdView;
import com.google.android.gms.ads.MobileAds;
import com.google.android.gms.ads.initialization.InitializationStatus;
import com.google.android.gms.ads.initialization.OnInitializationCompleteListener;
import com.google.firebase.database.DatabaseReference;
import com.subhamoy.gymstudentapp.db.MsgNotifDBOps;

import java.util.ArrayList;

public class NotificationMsg extends AppCompatActivity {

    ImageButton imgButtonBackToHome;
    ListView listViewNotifications;

    // Admob
    private AdView mAdView;

    // Firebase
    DatabaseReference reference;

    // Notification
    Intent notificationIntent;
    PendingIntent pendingIntent;

    // SharedPreferences
    SharedPreferences sp;
    private static final String MY_PREFS_NAME = "gymstudentapp_students";
    String SID, GYM_ID;

    ArrayList<String> messages;
    CustomAdapter customAdapter;
    MsgNotifDBOps msgNotifDBOps;
    Thread threadNotif;
    boolean keepUpdatingList = false;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_notification_msg);

        listViewNotifications = findViewById(R.id.listViewNotifications);
        imgButtonBackToHome = findViewById(R.id.imgButtonBackToHome);
        mAdView = findViewById(R.id.adViewNotif);

        // Init ArrayList
        messages = new ArrayList<>();

        msgNotifDBOps = new MsgNotifDBOps(this);
        messages = msgNotifDBOps.getAllMsgNotif();
        if(messages.size() == 0) {
            messages.add("No Notifications as of yet!");
        }

        // Init CustomAdapter
        customAdapter = new CustomAdapter();
        listViewNotifications.setAdapter(customAdapter);

        imgButtonBackToHome.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                finish();
            }
        });

        keepUpdatingList = true;

        initializeAdMob();
        startAutoUpdateThread();
        initUI();

    }

    /**
     * Auto updates list
     */
    private void startAutoUpdateThread() {
        threadNotif = new Thread() {
            @Override
            public void run() {
                super.run();
                while(keepUpdatingList) {
                    messages.clear();
                    messages = msgNotifDBOps.getAllMsgNotif();
                    if(messages.size() == 0) {
                        messages.add("No Notifications as of yet!");
                    }

                    // update msg list
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            customAdapter.notifyDataSetChanged();
                        }
                    });

                    try {
                        Thread.sleep(1000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        };
        threadNotif.start();
    }

    /**
     * Custom adapter for the list view elements
     */
    class CustomAdapter extends BaseAdapter {

        @Override
        public int getCount() {
            return messages.size();
        }

        @Override
        public Object getItem(int i) {
            return null;
        }

        @Override
        public long getItemId(int i) {
            return 0;
        }

        @Override
        public View getView(int i, View view, ViewGroup viewGroup) {
            view = getLayoutInflater().inflate(R.layout.custom_notification_msg, null);
            TextView textViewNotifMsg = view.findViewById(R.id.textViewNotifMsg);
            textViewNotifMsg.setText(messages.get(i));
            return view;
        }
    }

    /**
     * Initializes the adMob
     */
    private void initializeAdMob() {
        MobileAds.initialize(this, new OnInitializationCompleteListener() {
            @Override
            public void onInitializationComplete(InitializationStatus initializationStatus) {
            }
        });
        AdRequest adRequest = new AdRequest.Builder().build();
        mAdView.loadAd(adRequest);
    }

    /**
     * Set UI flags
     */
    public void initUI() {
        View decorView = getWindow().getDecorView();
        int uiOptions = View.SYSTEM_UI_FLAG_LAYOUT_STABLE |
                View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION |
//                View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN |
                View.SYSTEM_UI_FLAG_HIDE_NAVIGATION |
//                View.SYSTEM_UI_FLAG_FULLSCREEN |
                View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY;
        decorView.setSystemUiVisibility(uiOptions);
    }

    @Override
    protected void onDestroy() {
        keepUpdatingList = false;
        if(threadNotif.isAlive()) {
            threadNotif.interrupt();
        }
        super.onDestroy();
    }
}