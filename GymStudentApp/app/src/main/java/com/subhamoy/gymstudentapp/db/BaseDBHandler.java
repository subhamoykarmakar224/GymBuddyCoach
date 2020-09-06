package com.subhamoy.gymstudentapp.db;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import androidx.annotation.Nullable;

public class BaseDBHandler extends SQLiteOpenHelper {

    private static final int DB_VER = 1;
    private static final String DB_NAME = "MyGymBuddy";

    static final String TABLE_ATTENDENCE = "attendence";
    static final String KEY_ATTENDENCE_DATE = "date";
    static final String KEY_ATTENDENCE_STATE = "state";

    static String TABLE_MSG_NOTIF = "msgnotif";
    static String KEY_MSG_NOTIF_CNT = "msgcounter";
    static String KEY_MSG_NOTIF_MSG = "message";

    public BaseDBHandler(@Nullable Context context) {
        super(context, DB_NAME, null, DB_VER);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        createAttendenceTable(db);
        createNotificationTable(db);
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        String SQL = "drop table id exists ";
        db.execSQL(SQL + TABLE_ATTENDENCE);
        db.execSQL(SQL + TABLE_MSG_NOTIF);
    }

    private void createAttendenceTable(SQLiteDatabase db) {
        String CREATE_TABLE_ATTENDENCE = "create table " + TABLE_ATTENDENCE + " " +
                "(" + KEY_ATTENDENCE_DATE + " text primary key, " + KEY_ATTENDENCE_STATE + " integer)";
        db.execSQL(CREATE_TABLE_ATTENDENCE);
    }

    private void createNotificationTable(SQLiteDatabase db) {
        String CREATE_TABLE_NOTIF_MSG = "create table " + TABLE_MSG_NOTIF + " (" +
                KEY_MSG_NOTIF_CNT + " INTEGER primary key, " + KEY_MSG_NOTIF_MSG + " text)";
        db.execSQL(CREATE_TABLE_NOTIF_MSG);
    }
}
