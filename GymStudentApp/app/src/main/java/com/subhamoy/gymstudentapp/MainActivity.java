package com.subhamoy.gymstudentapp;

import android.Manifest;
import android.app.Activity;
import android.app.ActivityManager;
import android.app.AlertDialog;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.os.Bundle;
import android.util.Log;
import android.view.Gravity;
import android.view.MenuItem;
import android.view.View;
import android.widget.ImageButton;
import android.widget.PopupMenu;
import android.widget.TableRow;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.app.NotificationCompat;
import androidx.core.content.ContextCompat;

import com.google.android.gms.ads.AdRequest;
import com.google.android.gms.ads.AdView;
import com.google.android.gms.ads.MobileAds;
import com.google.android.gms.ads.initialization.InitializationStatus;
import com.google.android.gms.ads.initialization.OnInitializationCompleteListener;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import com.subhamoy.gymstudentapp.alarm.TimerService;
import com.subhamoy.gymstudentapp.bean.Attendence;
import com.subhamoy.gymstudentapp.bean.NotifMsg;
import com.subhamoy.gymstudentapp.bean.Notification;
import com.subhamoy.gymstudentapp.db.AttendenceDBOps;
import com.subhamoy.gymstudentapp.db.MsgNotifDBOps;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.Set;
import java.util.concurrent.TimeUnit;


public class MainActivity extends AppCompatActivity {

    // Time Remaining Widget
    TextView textViewTimeRemaining;

    ImageButton imgButtonUserOptions;

    // Calender Widgets
    ImageButton btnPrevMonth, btnNextMonth;
    FloatingActionButton floatingBtnCheckIn;
    TextView textViewMonthName;
    TableRow tableRowLine1, tableRowLine2, tableRowLine3, tableRowLine4, tableRowLine5, tableRowLine6;

    // Summary Widgets
    // 8:00 AM to 10:00 AM  ,   10 days
    TextView textViewAllottedTimeValue, textViewNoOfDaysPresentValue;
    ImageButton btnResetCalenderView;

    // Profile Widgets
    // ID-12345 ,   Subhamoy Karmakar   ,   28yrs   ,   August 2020
    TextView textViewStudentIDValue, textViewStudentNameValue, textViewStudentAgeValue, textViewStudentMembershipValue;

    // Calender control variables
    String [] dayOfWeek = { "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat" };
    String [] months = { "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" };
    int padding_day_of_week;
    int incrementer;

    // Permissions
    String [] PERMISSIONS = {
            Manifest.permission.CAMERA,
            Manifest.permission.FOREGROUND_SERVICE,
            Manifest.permission.INTERNET,
            Manifest.permission.ACCESS_NETWORK_STATE
    };
    private static final int requestCode = 1234;
    private static final int LAUNCH_SECOND_ACTIVITY = 1;

    // Admob
    private AdView mAdView;

    // SharedPreferences
    SharedPreferences sp;
    private static final String MY_PREFS_NAME = "gymstudentapp_students";

    AttendenceDBOps attendenceDBOps;
    AlertDialog.Builder alertBuilder;
    DatabaseReference dbRefNotification;
    public int counter = 0;
    String hms;
    int cnt;

    NotificationManager notificationManager;
    BroadcastReceiver broadcastReceiver;
    Intent serviceIntent;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        cnt = 0;
        sp = getApplicationContext().getSharedPreferences(MY_PREFS_NAME, Context.MODE_PRIVATE);

        initializeAdMob();
        getPermissions();
        getNewNotificationMsgs();

        // Other: Widgets
        alertBuilder = new AlertDialog.Builder(this);
        notificationManager = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);

        // Time Remaining : Widgets
        textViewTimeRemaining = findViewById(R.id.textViewTimeRemaining);
        imgButtonUserOptions = findViewById(R.id.imgButtonUserOptions);

        // Calender : widgets
        floatingBtnCheckIn = findViewById(R.id.floatingBtnCheckIn);
        btnPrevMonth = findViewById(R.id.btnPreviousMonth);
        btnNextMonth = findViewById(R.id.btnNextMonth);
        textViewMonthName = findViewById(R.id.textViewMonthName);
        tableRowLine1 = findViewById(R.id.tableRowLine1);
        tableRowLine2 = findViewById(R.id.tableRowLine2);
        tableRowLine3 = findViewById(R.id.tableRowLine3);
        tableRowLine4 = findViewById(R.id.tableRowLine4);
        tableRowLine5 = findViewById(R.id.tableRowLine5);
        tableRowLine6 = findViewById(R.id.tableRowLine6);

        // Summary : widgets
        btnResetCalenderView = findViewById(R.id.btnResetCalenderView);
        textViewAllottedTimeValue = findViewById(R.id.textViewAllottedTimeValue);
        textViewNoOfDaysPresentValue = findViewById(R.id.textViewNoOfDaysPresentValue);

        // Profile : widgets
        textViewStudentIDValue = findViewById(R.id.textViewStudentIDValue);
        textViewStudentNameValue = findViewById(R.id.textViewStudentNameValue);
        textViewStudentAgeValue = findViewById(R.id.textViewStudentAgeValue);
        textViewStudentMembershipValue = findViewById(R.id.textViewStudentMembershipValue);

        // Widget Properties

        // Listeners
        widgetListeners();

        padding_day_of_week = 10; // 5dp padding for each cell
        incrementer = 0; // controls the view month

        textViewAllottedTimeValue.setText(sp.getString(ConstantFBStudent.allottedTime, ""));
        textViewStudentIDValue.setText(sp.getString(ConstantFBStudent.SID, ""));
        textViewStudentNameValue.setText(sp.getString(ConstantFBStudent.studentName, ""));
        String tmpDOBToAge = sp.getString(ConstantFBStudent.studentAge, "");
        if(!tmpDOBToAge.equalsIgnoreCase("")) {
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
            Date d = null;
            try {
                String pattern = "yyyy-MM-dd";
                String newPattern = "MMMM dd";
                SimpleDateFormat simpleDateFormat = new SimpleDateFormat(pattern);
                Date tmpDateDOB = simpleDateFormat.parse(tmpDOBToAge);
                Calendar now = Calendar.getInstance();
                Calendar dob = Calendar.getInstance();
                dob.setTime(tmpDateDOB);
                int year1 = now.get(Calendar.YEAR);
                int year2 = dob.get(Calendar.YEAR);
                int age = year1 - year2;
                int month1 = now.get(Calendar.MONTH);
                int month2 = dob.get(Calendar.MONTH);
                if (month2 > month1) {
                    age--;
                } else if (month1 == month2) {
                    int day1 = now.get(Calendar.DAY_OF_MONTH);
                    int day2 = dob.get(Calendar.DAY_OF_MONTH);
                    if (day2 > day1) {
                        age--;
                    }
                }
                tmpDOBToAge = String.valueOf(age);
            } catch (Exception e) {
                Log.i("olla", "Error in calc age : " + e);
            }
            textViewStudentAgeValue.setText(tmpDOBToAge + " yrs");
        }
        String tmpValidityString = sp.getString(ConstantFBStudent.membershipValidity, "");
        if(!tmpValidityString.equalsIgnoreCase("")) {
            boolean error = false;
            String pattern = "yyyy-MM-dd";
            String newPattern = "MMMM dd";
            SimpleDateFormat simpleDateFormat = new SimpleDateFormat(pattern);
            SimpleDateFormat newDateFormat = new SimpleDateFormat(newPattern);
            try {
                Date tmpDateValidity = simpleDateFormat.parse(tmpValidityString);
                tmpValidityString = newDateFormat.format(tmpDateValidity);
            } catch (ParseException e) {
                Log.i("olla", "Parse Date error :: " + e);
                textViewStudentMembershipValue.setText(tmpValidityString);
                error = true;
            }
            if (!error) {
                textViewStudentMembershipValue.setText(tmpValidityString);
            }
        }
        imgButtonUserOptions.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                PopupMenu popupMenu = new PopupMenu(MainActivity.this, imgButtonUserOptions);
                popupMenu.getMenuInflater().inflate(R.menu.user_options, popupMenu.getMenu());
                popupMenu.setOnMenuItemClickListener(new PopupMenu.OnMenuItemClickListener() {
                    @Override
                    public boolean onMenuItemClick(MenuItem item) {
                        switch (item.getTitle().toString()) {
                            case "Notifications":
                                Intent intentNotificationMsg = new Intent(MainActivity.this, NotificationMsg.class);
                                startActivity(intentNotificationMsg);
                                break;

                            case "About":
                                Intent intentAbout = new Intent(MainActivity.this, About.class);
                                startActivity(intentAbout);
                                break;

                            case "Logout":
                                logout();
                                break;
                        }
                        return true;
                    }
                });
                popupMenu.show();
            }
        });

        attendenceDBOps = new AttendenceDBOps(this);
        dbRefNotification = FirebaseDatabase.getInstance().getReference().child(ConstantFBStudent.FB_TABLE_NOTIFICATION);
        hms = "--:--:--";

        IntentFilter intentFilter = new IntentFilter();
        intentFilter.addAction(ConstantFBStudent.INTENT_ACTION_TIME_COUNTER);
        broadcastReceiver = new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                String tmptimeVal = intent.getStringExtra(ConstantFBStudent.INTENT_STR_TIME_BACK);
                Long timeVal = Long.parseLong(tmptimeVal);
                hms = String.format("%02d:%02d:%02d", TimeUnit.MILLISECONDS.toHours(timeVal),
                                    TimeUnit.MILLISECONDS.toMinutes(timeVal) - TimeUnit.HOURS.toMinutes(TimeUnit.MILLISECONDS.toHours(timeVal)),
                                    TimeUnit.MILLISECONDS.toSeconds(timeVal) - TimeUnit.MINUTES.toSeconds(TimeUnit.MILLISECONDS.toMinutes(timeVal)));
                textViewTimeRemaining.setText(hms);
                if(timeVal == 0) {
                    stopService();
                }
            }
        };
        registerReceiver(broadcastReceiver, intentFilter);

        checkMembershipValidity();

        serviceIntent = new Intent(this, TimerService.class);
    }

    @Override
    protected void onResume() {
        super.onResume();
        cleanCalenderView();
        initCalenderElements();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        unregisterReceiver(broadcastReceiver);
    }

    /**
     * Resets the calender view by removing all the child elements in the TableRows
     */
    public void cleanCalenderView() {
        tableRowLine1.removeAllViews();
        tableRowLine2.removeAllViews();
        tableRowLine3.removeAllViews();
        tableRowLine4.removeAllViews();
        tableRowLine5.removeAllViews();
        tableRowLine6.removeAllViews();
        textViewMonthName.setText("");
    }

    /**
     * Initialize the calender to current month
     */
    public void initCalenderElements() {
        Date date = new Date();
        date = getNextMonthIncrementer(date);
        textViewMonthName.setText(getDateInMonthAndYear(date));
        setCalenderElements(date);
    }

    /**
     * Returns date "January 2020" format.
     * @param date
     * @return string
     */
    private String getDateInMonthAndYear(Date date) {
        DateFormat dateFormat = new SimpleDateFormat("MMMM YYYY");
        return dateFormat.format(date);
    }

    /**
     * Get day of the week - SUN, MON, ...
     * @param date
     * @return
     */
    public String getDayOfTheWeek(Date date) {
        DateFormat dateFormat = new SimpleDateFormat("E");
        return dateFormat.format(date);
    }

    /**
     * Get day
     * @param date
     * @return
     */
    public String getDayFromDate(Date date) {
        DateFormat dateFormat = new SimpleDateFormat("dd");
        return dateFormat.format(date);
    }

    /**
     * Get Next month
     * @return date
     */
    public Date getNextMonthIncrementer(Date date) {
        Calendar cal = Calendar.getInstance();
        cal.setTime(date);
        cal.add(Calendar.MONTH, incrementer);
        return cal.getTime();
    }

    /**
     * Set TableRow elements
     * @param date
     */
    public void setCalenderElements(Date date) {
        String [] tmpMonthYear = textViewMonthName.getText().toString().split(" ");
        String [] months = { "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" };
        int tmp = 0;
        for(tmp = 0 ; tmp < months.length ; tmp ++) {
            if(months[tmp].equalsIgnoreCase(tmpMonthYear[0])) {
                break;
            }
        }
        ArrayList<Integer> datesList = attendenceDBOps.getStatusList(String.valueOf(tmp + 1), tmpMonthYear[1]);
        textViewNoOfDaysPresentValue.setText(datesList.size() + " days");

        String [] monthNYear = getDateInMonthAndYear(date).split(" ");
        Calendar cal = Calendar.getInstance();
        int i = 0;
        for(i = 0 ; i < months.length ; i ++) {
            if(months[i].equalsIgnoreCase(monthNYear[0])) {
                break;
            }
        }
        cal.set(Integer.parseInt(monthNYear[1]), i, 1);
        Date firstDayOfMonth = cal.getTime(); // Wed Jul 01 22:58:49 GMT+05:30 2020
        int noOfDaysInMonth = cal.getActualMaximum(Calendar.DAY_OF_MONTH); // gets not of days in the month

        int cnt = 1;
        String todayDate = getDayFromDate(date);
        String startDayOfWeek = getDayOfTheWeek(firstDayOfMonth);
        int dayOfWeekCnt = 0;
        for(dayOfWeekCnt = 0 ; dayOfWeekCnt < dayOfWeek.length ; dayOfWeekCnt ++) {
            if (startDayOfWeek.equalsIgnoreCase(dayOfWeek[dayOfWeekCnt])) {
                break;
            }
        }

        // Row 1
        for(int j=0;j<7;j++) {
            TextView tmpTxtView = new TextView(this);
            if(j < dayOfWeekCnt) {
                tmpTxtView.setText("0");
                setHiddenTextViewDecoration(tmpTxtView);
            } else {
                tmpTxtView.setText(String.valueOf(cnt));
                setTextViewDecoration(tmpTxtView, todayDate, cnt, datesList);
                cnt ++;
            }
            tableRowLine1.addView(tmpTxtView);
        }

        // Row 2
        for(int j=0;j<7;j++) {
            TextView tmpTxtView = new TextView(this);
            tmpTxtView.setText(String.valueOf(cnt));
            setTextViewDecoration(tmpTxtView, todayDate, cnt, datesList);
            tableRowLine2.addView(tmpTxtView);
            cnt ++;
        }

        // Row 3
        for(int j=0;j<7;j++) {
            TextView tmpTxtView = new TextView(this);
            tmpTxtView.setText(String.valueOf(cnt));
            setTextViewDecoration(tmpTxtView, todayDate, cnt, datesList);
            tableRowLine3.addView(tmpTxtView);
            cnt ++;
        }

        // Row 4
        for(int j=0;j<7;j++) {
            TextView tmpTxtView = new TextView(this);
            tmpTxtView.setText(String.valueOf(cnt));
            setTextViewDecoration(tmpTxtView, todayDate, cnt, datesList);
            tableRowLine4.addView(tmpTxtView);
            cnt ++;
        }

        // Row 5
        for(int j=0;j<7;j++) {
            TextView tmpTxtView = new TextView(this);
            if(cnt == noOfDaysInMonth + 1)
                break;
            tmpTxtView.setText(String.valueOf(cnt));
            setTextViewDecoration(tmpTxtView, todayDate, cnt, datesList);
            tableRowLine5.addView(tmpTxtView);
            cnt ++;
        }

        // Row 6
        for(int j=0;j<7;j++) {
            TextView tmpTxtView = new TextView(this);
            if(cnt > noOfDaysInMonth) {
                tmpTxtView.setText("0");
                setHiddenTextViewDecoration(tmpTxtView);
            } else {
                tmpTxtView.setText(String.valueOf(cnt));
                setTextViewDecoration(tmpTxtView, todayDate, cnt, datesList);
            }
            tableRowLine6.addView(tmpTxtView);
            cnt++;
        }
    }

    /**
     * Sets the textview style
     * @param textView
     */
    private void setTextViewDecoration(TextView textView, String currDate, int cnt, ArrayList<Integer> datesList) {
        String [] monthNYear = getDateInMonthAndYear(new Date()).split(" ");
        if(datesList.contains(cnt) && textViewMonthName.getText().toString().indexOf(monthNYear[0]) != -1 && currDate.equalsIgnoreCase(String.valueOf(cnt))) {
            setTextViewDecorationPresentDateForToday(textView);
        } else if(datesList.contains(cnt)) {
            setTextViewDecorationPresentDate(textView);
        } else {
            if (textViewMonthName.getText().toString().indexOf(monthNYear[0]) != -1 && currDate.equalsIgnoreCase(String.valueOf(cnt))) {
                setTextViewDecorationToday(textView);
            } else {
                TableRow.LayoutParams params1 = new TableRow.LayoutParams(TableRow.LayoutParams.WRAP_CONTENT, TableRow.LayoutParams.WRAP_CONTENT);
                params1.gravity = Gravity.CENTER;
                textView.setLayoutParams(params1);
                textView.setTextColor(Color.BLACK);
                textView.setPadding(padding_day_of_week, padding_day_of_week, padding_day_of_week, padding_day_of_week);
            }
        }
    }

    /**
     * Sets the hidden textview style
     * @param textView
     */
    private void setHiddenTextViewDecoration(TextView textView) {
        TableRow.LayoutParams params1 = new TableRow.LayoutParams(TableRow.LayoutParams.WRAP_CONTENT, TableRow.LayoutParams.WRAP_CONTENT);
        params1.gravity = Gravity.CENTER;
        textView.setLayoutParams(params1);
        textView.setTextColor(Color.WHITE);
        textView.setPadding(padding_day_of_week, padding_day_of_week, padding_day_of_week, padding_day_of_week);
    }

    /**
     * Sets the textview style for today's date
     * @param textView
     */
    private void setTextViewDecorationToday(TextView textView) {
        TableRow.LayoutParams params1 = new TableRow.LayoutParams(TableRow.LayoutParams.WRAP_CONTENT, TableRow.LayoutParams.WRAP_CONTENT);
        params1.gravity = Gravity.CENTER;
        textView.setLayoutParams(params1);
        textView.setTextColor(Color.WHITE);
        textView.setBackground(ContextCompat.getDrawable(this, R.drawable.bg_date_today));
        textView.setPadding(padding_day_of_week, padding_day_of_week, padding_day_of_week, padding_day_of_week);
    }

    /**
     * Sets the textView style for  dates the user was present
     * @param textView
     */
    private void setTextViewDecorationPresentDate(TextView textView) {
        TableRow.LayoutParams params1 = new TableRow.LayoutParams(TableRow.LayoutParams.WRAP_CONTENT, TableRow.LayoutParams.WRAP_CONTENT);
        params1.gravity = Gravity.CENTER;
        textView.setLayoutParams(params1);
        textView.setTextColor(ContextCompat.getColor(this, R.color.darkGreen));
        textView.setPadding(padding_day_of_week, padding_day_of_week, padding_day_of_week, padding_day_of_week);
    }

    /**
     * Sets the textView style for dates the user was present and also its todays' date
     * @param textView
     */
    private void setTextViewDecorationPresentDateForToday(TextView textView) {
        TableRow.LayoutParams params1 = new TableRow.LayoutParams(TableRow.LayoutParams.WRAP_CONTENT, TableRow.LayoutParams.WRAP_CONTENT);
        params1.gravity = Gravity.CENTER;
        textView.setLayoutParams(params1);
        textView.setTextColor(ContextCompat.getColor(this, R.color.darkGreen));
        textView.setBackground(ContextCompat.getDrawable(this, R.drawable.bg_date_today));
        textView.setPadding(padding_day_of_week, padding_day_of_week, padding_day_of_week, padding_day_of_week);
    }

    /**
     * Init Listeners for widgets
     */
    public void widgetListeners() {
        floatingBtnCheckIn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String tmpStatusString = sp.getString(ConstantFBStudent.membershipStatus, "");
                if(tmpStatusString.equalsIgnoreCase("-1") || tmpStatusString.equalsIgnoreCase("")) {
                    alertBuilder.setMessage("Your membership status has been put on hold. Please speak to the gym admin to resume services.")
                            .setPositiveButton("Ok", null)
                            .setCancelable(false);
                    AlertDialog alertDialog = alertBuilder.create();
                    alertDialog.show();
                    return;
                }


                if(attendenceDBOps.checkedInStatus()) {
                    alertBuilder.setMessage("Unable to process your request. You have already punched in today.")
                            .setPositiveButton("Ok",  null)
                            .setTitle("Error")
                            .setCancelable(false);
                    AlertDialog alertDialog = alertBuilder.create();;
                    alertDialog.show();
                    return;
                }
                Intent intent = new Intent(MainActivity.this, ScanQRCodeActivity.class);
                startActivityForResult(intent, LAUNCH_SECOND_ACTIVITY);
            }
        });

        btnNextMonth.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                incrementer ++;
                cleanCalenderView();
                initCalenderElements();
            }
        });

        btnPrevMonth.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                incrementer --;
                cleanCalenderView();
                initCalenderElements();
            }
        });

        btnResetCalenderView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                incrementer = 0;
                cleanCalenderView();
                initCalenderElements();
            }
        });

    }

    /**
     * Logout User
     */
    private void logout() {
        final AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setMessage("Are you sure you want to Logout? You will have to re-authenticate to use the app again?")
                .setCancelable(false)
                .setTitle("Logout?")
                .setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        // Delete from local DB
                        SharedPreferences.Editor editor = sp.edit();
                        editor.clear();
                        editor.apply();

                        // Sign out user
                        FirebaseAuth.getInstance().signOut();

                        // Redirect User
                        Intent intent = new Intent(MainActivity.this, SignIn.class);
                        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                        startActivity(intent);
                    }
                })
                .setNegativeButton("No", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        dialog.dismiss();
                    }
                });

        // Create & Show the AlertDialog object and return it
        final AlertDialog dialog = builder.create();
        dialog.setOnShowListener( new DialogInterface.OnShowListener() {
            @Override
            public void onShow(DialogInterface arg0) {
                int colBG = getResources().getColor(android.R.color.transparent);
                int colText = getResources().getColor(R.color.colorPrimaryDark);

                dialog.getButton(AlertDialog.BUTTON_NEGATIVE).setBackgroundColor(colBG);
                dialog.getButton(AlertDialog.BUTTON_NEGATIVE).setTextColor(colText);
                dialog.getButton(AlertDialog.BUTTON_POSITIVE).setBackgroundColor(colBG);
                dialog.getButton(AlertDialog.BUTTON_POSITIVE).setTextColor(colText);
            }
        });

        // Show the dialog
        dialog.show();
    }

    /**
     * Get Permissions from User
     */
    public void getPermissions() {
        for(String permission : PERMISSIONS) {
            if(ActivityCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(
                        this,
                        new String[] { permission },
                        requestCode
                );
            }
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == LAUNCH_SECOND_ACTIVITY) {
            if (resultCode == Activity.RESULT_OK) {
                // Data returned :: BodyShapersGym-2932 for Date :: 30-07-2020
                String qrdata = data.getStringExtra("QRCODE_SCAN_DATA");
                String date = data.getStringExtra("QRCODE_SCAN_DATE");
                if (!checkIfBelongToThisGym(qrdata)) {
                    alertBuilder.setMessage("You are not allowed in this gym presently, as you are not a member here right now. Please get in touch with the Gym Admin to gain access to this gym.")
                            .setPositiveButton("Ok", null)
                            .setCancelable(false);
                    AlertDialog alertDialog = alertBuilder.create();
                    ;
                    alertDialog.show();
                } else {
                    // Check time validity
                    if (checkTimeValidity(qrdata)) {
                        attendenceDBOps.insertAttendence(new Attendence(date, "1"));
                        if(!isMyServiceRunning(TimerService.class)) {
                            startService();
                        }
                    }
                }
            }
            if (resultCode == Activity.RESULT_CANCELED) {
            }
        }
    }

    /**
     * Starts the timer foreground service
     */
    public void startService() {
        Date d = new Date();

        DateFormat dateFormat = new SimpleDateFormat("hh:mm a");
        String time = dateFormat.format(d);

        String allotedTime = sp.getString(ConstantFBStudent.allottedTime, null);
        if(allotedTime != null) {
            String endTime = allotedTime.split("to")[1].trim();
            Date allottedEndTime, currTime;
            try {
                allottedEndTime = new SimpleDateFormat("hh:mm a").parse(endTime);
                currTime = new SimpleDateFormat("hh:mm a").parse(time);
            } catch (ParseException e) {
                Log.i("olla", getLocalClassName() + " :: Error :: " + e.getMessage());
                return;
            }
            Long timeDifference = allottedEndTime.getTime() - currTime.getTime();
            serviceIntent.putExtra(ConstantFBStudent.INTENT_STR_TIME_LEFT, timeDifference.toString());
            startService(serviceIntent);
        }
    }

    /**
     * Check if foreground service is running
     * @param serviceClass
     * @return
     */
    private boolean isMyServiceRunning(Class<?> serviceClass) {
        ActivityManager manager = (ActivityManager) getSystemService(Context.ACTIVITY_SERVICE);
        for (ActivityManager.RunningServiceInfo service : manager.getRunningServices(Integer.MAX_VALUE)) {
            if (serviceClass.getName().equals(service.service.getClassName())) {
                return true;
            }
        }
        return false;
    }

    /**
     * Stops the timer foreground service
     */
    public void stopService() {
        stopService(serviceIntent);
    }



    /**
     * Checks if the user is a member of that gym
     * @param qrDate
     * @return
     */
    private boolean checkIfBelongToThisGym(String qrDate) { // BodyShapersGym-2932, ID-2932-1
        String gymID = qrDate.split("-")[1].trim();
        String studentId_gymid = sp.getString(ConstantFBStudent.SID, null).split("-")[1];
        if(gymID.equalsIgnoreCase(studentId_gymid)) {
            return true;
        }
        return false;
    }

    /**
     * Checks time of entry if valid
     * @return
     */
    private boolean checkTimeValidity(String qrdata) {
        String timeRegEx = "hh:mm a";
        boolean status = false;
        Date date = new Date();
        DateFormat dateFormat = new SimpleDateFormat(timeRegEx);
        String time = dateFormat.format(date);

        String allotedTime = sp.getString(ConstantFBStudent.allottedTime, null);
        if(allotedTime == null)
            return false;
        String startTime = allotedTime.split("to")[0].trim();
        String endTime = allotedTime.split("to")[1].trim();
        Date allottedStartTime, allottedEndTime, currTime;
        try {
            allottedStartTime = new SimpleDateFormat(timeRegEx).parse(startTime);
            allottedEndTime = new SimpleDateFormat(timeRegEx).parse(endTime);
            currTime = new SimpleDateFormat(timeRegEx).parse(time);
        } catch(ParseException e) {
            Log.i("olla", getLocalClassName() + " :: Error :: " + e.getMessage());
            return false;
        }

        // add buffer time to start and end time
        Calendar cal = Calendar.getInstance();
        cal.setTime(allottedStartTime);
        cal.add(Calendar.MINUTE, -10);
        allottedStartTime = cal.getTime();

        cal.setTime(allottedEndTime);
        cal.add(Calendar.MINUTE, -15);
        allottedEndTime = cal.getTime();


        // TODO :: THIS IS FOR TESTING DELETE LATER
//        cal.setTime(currTime);
//        cal.add(Calendar.HOUR, 1);
//        cal.add(Calendar.MINUTE, 10);
//        currTime = cal.getTime();
//        Log.i("olla", "Allotted Time :: " + allottedStartTime + " to " + allottedEndTime);
//        Log.i("olla", "Curr Time :: " + currTime);

        if(currTime.after(allottedStartTime) && currTime.before(allottedEndTime)) {
            status = true;
            // Upload data to Firebase
            FBSendNotification fbSendNotifThread = new FBSendNotification(
                    sp.getString(ConstantFBStudent.SID, null), // SID
                    qrdata, // GymID
                    (new Date()).toString(), // Timestamp
                    ConstantFBStudent.MSG_LEVEL_GREEN, // Level
                    "Student entered the gym."
            );
            fbSendNotifThread.start();

//            final long timeDifference = allottedEndTime.getTime() - currTime.getTime();

            // Start Timer Thread
//            new CountDownTimer(timeDifference, 1000){
//                public void onTick(long millisUntilFinished){
//                    long tmpTimeRemain = timeDifference - (counter * 1000);
//                    counter ++;
//                    hms = String.format("%02d:%02d:%02d", TimeUnit.MILLISECONDS.toHours(tmpTimeRemain),
//                            TimeUnit.MILLISECONDS.toMinutes(tmpTimeRemain) - TimeUnit.HOURS.toMinutes(TimeUnit.MILLISECONDS.toHours(tmpTimeRemain)),
//                            TimeUnit.MILLISECONDS.toSeconds(tmpTimeRemain) - TimeUnit.MINUTES.toSeconds(TimeUnit.MILLISECONDS.toMinutes(tmpTimeRemain)));
//                    textViewTimeRemaining.setText(hms);
//
//                }
//                public  void onFinish(){
//                    textViewTimeRemaining.setText("--:--:--");
//                }
//            }.start();

//            startScheduler(MainActivity.this, timeDifference);

        } else {
            // Upload data to Firebase
            FBSendNotification fbSendNotifThread = new FBSendNotification(
                    sp.getString(ConstantFBStudent.SID, null), // SID
                    qrdata, // GymID
                    (new Date()).toString(), // Timestamp
                    ConstantFBStudent.MSG_LEVEL_RED, // Level
                    "Student tried to access when not alloted."
            );
            fbSendNotifThread.start();


            alertBuilder.setMessage("You are not allowed in the gym right now. Please get in touch with the gym admin for further information.")
                    .setPositiveButton("Ok",  null)
                    .setCancelable(false);
            AlertDialog alertDialog = alertBuilder.create();;
            alertDialog.show();
        }
        return status;
    }

//    /**
//     * Background schedular for end time
//     * @param c
//     * @param timeDifference
//     */
//    private void startScheduler(Context c, long timeDifference) {
//        Intent intent = new Intent(MainActivity.this, ExecutableService.class);
//        PendingIntent pendingIntent = PendingIntent.getBroadcast(
//                MainActivity.this, 0, intent, 0
//        );
//        AlarmManager alarmManager = (AlarmManager) getSystemService(ALARM_SERVICE);
//
//        long tmpSeconds = 1000 * timeDifference;
//        alarmManager.set(
//                AlarmManager.RTC_WAKEUP,
//                System.currentTimeMillis() + tmpSeconds,
//                pendingIntent
//        );
//    }

    /**
     * Thread to send notification to FB
     */
    class FBSendNotification extends Thread {

        String studentId;
        String gymId;
        String dateTime;
        String level;
        String msg;


        FBSendNotification(String studentId, String gymId, String dateTime, String level, String msg) {
            this.studentId = studentId;
            this.gymId = gymId;
            this.dateTime = dateTime;
            this.level = level;
            this.msg = msg;
        }

        @Override
        public void run() {
            // studentId, gymId, dateTime, level, msg
            Notification n = new Notification(studentId, gymId, dateTime, level, msg);
            dbRefNotification
                    .child(n.getGymId())
                    .push()
                    .setValue(n);
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
        mAdView = findViewById(R.id.adView);
        AdRequest adRequest = new AdRequest.Builder().build();
        mAdView.loadAd(adRequest);
    }

    /**
     * Gets the notification messages from firebase
     */
    public void getNewNotificationMsgs() {
        Thread thread = new Thread() {
            @Override
            public void run() {
                super.run();
                controlNotifMsg();
            }

            public void controlNotifMsg() {
                final MsgNotifDBOps msgNotifDBOps = new MsgNotifDBOps(MainActivity.this);
                DatabaseReference notifRef;
                String GYM_ID = sp.getString(ConstantFBStudent.gymId, "");
                String SID = sp.getString(ConstantFBStudent.SID, "");
                notifRef = FirebaseDatabase.getInstance().getReference()
                        .child(ConstantFBStudent.FB_TABLE_MSG_NOTIF)
                        .child(GYM_ID).child(SID);
                notifRef.addValueEventListener(new ValueEventListener() {
                    @Override
                    public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                        if (dataSnapshot.exists()) {
                            ArrayList<NotifMsg> messages = new ArrayList<>();
                            AttendenceDBOps attendenceDBOps = new AttendenceDBOps(MainActivity.this);
                            NotifMsg notifMsg = null;
                            Hashtable<String, String> dateAttendence = new Hashtable<String, String>();
                            for (DataSnapshot snap : dataSnapshot.getChildren()) {
                                notifMsg = new NotifMsg(
                                        (long) snap.child(ConstantFBStudent.MSG_NOTIF_CNT).getValue(),
                                        (String) snap.child(ConstantFBStudent.MSG_NOTIF_MSG).getValue()
                                );

                                // Add or delete remote attendance
                                if(notifMsg.getMessage().contains("Attend :: ")) {
                                    String [] data = notifMsg.getMessage().split(" :: ");
                                    Attendence attendence = new Attendence(data[1].trim(), data[2].trim());
                                    dateAttendence.put(attendence.getDate(), attendence.getState());
                                    continue;
                                }

                                boolean status = msgNotifDBOps.isCounterPresent(notifMsg.getCounter());
                                if (!status) {
                                    msgNotifDBOps.insertMsgNotif(notifMsg);
                                    messages.add(notifMsg);
                                }
                            }

                            // Remote check in feature check
                            Set<String> keys = dateAttendence.keySet();
                            Iterator<String> itr = keys.iterator();
                            String keyDate = "";
                            String valueStatus = "";
                            while (itr.hasNext()) {
                                keyDate = itr.next();
                                valueStatus = dateAttendence.get(keyDate);
                                if(valueStatus.equalsIgnoreCase("1")) {
                                    attendenceDBOps.insertAttendence(new Attendence(keyDate, valueStatus));
                                } else {
                                    attendenceDBOps.deleteAttendence(new Attendence(keyDate, valueStatus));
                                }
                            }

                            // New Notification
                            newNotificationControl(messages);

                        }
                    }

                    @Override
                    public void onCancelled(@NonNull DatabaseError databaseError) {
                    }
                });
            }

            /**
             * Show notification of messages from admin
             * @param notifMsgs
             */
            public void newNotificationControl(ArrayList<NotifMsg> notifMsgs) {
                if(notifMsgs.size() <= 0)
                    return;
                Intent intentNotif = new Intent(MainActivity.this, NotificationMsg.class);
                PendingIntent pendingIntent = PendingIntent.getActivity(
                        MainActivity.this, 0, intentNotif, 0
                );
                for(NotifMsg n : notifMsgs) {
                    android.app.Notification notification = new NotificationCompat.Builder(MainActivity.this, ConstantFBStudent.NOTIFICATION_CHANNEL)
                            .setSmallIcon(R.drawable.ic_alert)
                            .setContentTitle("GYMMS")
                            .setContentText(n.getMessage())
                            .setPriority(NotificationCompat.PRIORITY_LOW)
                            .setContentIntent(pendingIntent)
                            .setStyle(new NotificationCompat.BigTextStyle()
                                    .bigText(n.getMessage())
                            )
                            .build();
                    notificationManager.notify(cnt, notification);
                    cnt ++;
                }
            }
        };
        thread.start();
    }

    /**
     * Checks if the membership has been put on hold from the admin side
     */
    public void checkMembershipValidity() {
        String tmpValidityString = sp.getString(ConstantFBStudent.membershipValidity, "");
        SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd");
        Date tmpDateValidity;
        try {
            tmpDateValidity = simpleDateFormat.parse(tmpValidityString);
        } catch (ParseException e) {
            Log.i("olla", "Parse Date error :: " + e);
            return;
        }
        long difference_In_Time = tmpDateValidity.getTime() - (new Date()).getTime();
        int diffDays = (int) (difference_In_Time / (24 * 60 * 60 * 1000));
        String message = "";
        if(diffDays > 1 && diffDays <= 4) {
            message = "Your membership is going to expire.\n" +
                    "Please renew your membership to continue using gym services.";
        } else if (diffDays <= 0) {
            message = "Your membership has expired!\n" +
                    "Please renew your membership to continue using gym services.";
        }

        if(message != "") {
            alertBuilder.setMessage(message)
                    .setPositiveButton("Ok", null)
                    .setCancelable(false);
            AlertDialog alertDialog = alertBuilder.create();
            alertDialog.show();
        }
    }
}
