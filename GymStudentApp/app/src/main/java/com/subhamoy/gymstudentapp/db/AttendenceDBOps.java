package com.subhamoy.gymstudentapp.db;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.util.Log;

import androidx.annotation.Nullable;

import com.google.android.gms.common.api.internal.IStatusCallback;
import com.subhamoy.gymstudentapp.bean.Attendence;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class AttendenceDBOps extends BaseDBHandler {

    public AttendenceDBOps(@Nullable Context context) {
        super(context);
    }

    /**
     * Insert new attendance
     * @param attendence
     */
    public void insertAttendence(Attendence attendence) {
        if (isPresent(attendence)) {
            return;
        }
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues content = new ContentValues();
        content.put(KEY_ATTENDENCE_DATE, attendence.getDate());
        content.put(KEY_ATTENDENCE_STATE, attendence.getState());

        try {
            db.insert(TABLE_ATTENDENCE, null, content);
        } catch (Exception e) {
            Log.i("olla", getClass().getName() + " :: insertAttendence() :: Error :: " + e.getMessage());
        }
    }

    /**
     * Delete attendance from database
     * @param attendence
     */
    public void deleteAttendence(Attendence attendence) {
//        if(!isPresent(attendence)) {
//            return;
//        }
        SQLiteDatabase db = this.getWritableDatabase();
        String q = "delete from " + TABLE_ATTENDENCE + " where " + KEY_ATTENDENCE_DATE +
                "='" + attendence.getDate() + "'";
        try {
//            db.rawQuery(q, new String[] {});
            db.delete(TABLE_ATTENDENCE, KEY_ATTENDENCE_DATE + "=?", new String[]{ attendence.getDate() });
        } catch (Exception e) {
            Log.i("olla", getClass().getName() + " :: deleteAttendence() :: Error :: " + e.getMessage());
        } finally {
            db.close();
        }
        return;
    }

    /**
     * Checks if date already present
     * @param attendence
     * @return boolean
     */
    public boolean isPresent(Attendence attendence) {
        SQLiteDatabase db = this.getWritableDatabase();

        try {
            Cursor cur = db.rawQuery(
                    "select * from " + TABLE_ATTENDENCE + " where " +KEY_ATTENDENCE_DATE+"='" + attendence.getDate() + "'",
                    new String[]{}
            );
            if(cur.getCount()!= 0) {
                return true;
            }
        } catch (Exception e) {
            Log.i("olla", getClass().getName() + " :: insertAttendence() :: Error :: " + e.getMessage());
        }

        return false;
    }

    /**
     * Gets the dates of the month and year
     * @param month
     * @param year
     * @return
     */
    public ArrayList<Integer> getStatusList(String month, String year) {
        if (month.length() == 1) {
            month = "0" + month;
        }
        month = "-" + month + "-" + year;
        ArrayList<Integer> dateList = new ArrayList<>();
        SQLiteDatabase db = this.getWritableDatabase();
        String sql = "select " + KEY_ATTENDENCE_DATE + " from " + TABLE_ATTENDENCE + " where " + KEY_ATTENDENCE_DATE + " like '%" + month + "'";
        try {
            String tmp = "";
            Cursor cur = db.rawQuery(sql, new String[]{});
            if (cur.moveToFirst()) {
                do {
                    tmp = cur.getString(0);
                    tmp = tmp.substring(0, tmp.indexOf("-"));
                    dateList.add(Integer.parseInt(tmp));
                } while (cur.moveToNext());
            }
        } catch (Exception e) {
            Log.i("olla", getClass().getName() + " :: deleteAttendence() :: Error :: " + e.getMessage());
        } finally {
            db.close();
        }
        return dateList;
    }

    public boolean checkedInStatus() {
        String tmp = getNormalizedDateFormat(new Date());
        boolean status = false;
        SQLiteDatabase db = this.getWritableDatabase();
        String sql = "select " + KEY_ATTENDENCE_STATE + " from " + TABLE_ATTENDENCE + " where " + KEY_ATTENDENCE_DATE + "=?";
        try {
            Cursor cur = db.rawQuery(sql, new String[]{tmp});
            if (cur.moveToFirst()) {
                tmp = cur.getString(0);
                if(tmp.equalsIgnoreCase("1")) {
                    status = true;
                }
            }
        } catch (Exception e) {
            Log.i("olla", getClass().getName() + " :: deleteAttendence() :: Error :: " + e.getMessage());
        } finally {
            db.close();
        }

        return status;
    }

    public String getNormalizedDateFormat(Date date) {
        DateFormat dateFormat = new SimpleDateFormat("dd-MM-yyyy");
        return dateFormat.format(date);
    }
}

