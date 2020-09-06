package com.subhamoy.gymstudentapp.db;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.util.Log;

import androidx.annotation.Nullable;

import com.subhamoy.gymstudentapp.bean.NotifMsg;

import java.util.ArrayList;

public class MsgNotifDBOps extends BaseDBHandler{

    public MsgNotifDBOps(@Nullable Context context) {
        super(context);
    }

    public void insertMsgNotif(NotifMsg notifMsg) {
        clearMsgNotif();
        SQLiteDatabase db = this.getWritableDatabase();
        String sql = "insert into " + TABLE_MSG_NOTIF + " ("+KEY_MSG_NOTIF_CNT+", "+
                KEY_MSG_NOTIF_MSG+") values ("+notifMsg.getCounter()+", '" + notifMsg.getMessage() + "')";
        try {
            db.execSQL(sql, new String[] {});
        } catch (Exception e) {
            Log.i("olla", getClass().getName() + " :: insertMsgNotif() :: Error :: " + e.getMessage());
        } finally {
            db.close();
        }
    }

    public void clearMsgNotif() {
        int totalNotif = 0;
        SQLiteDatabase db = this.getWritableDatabase();
        String query = "select * from " + TABLE_MSG_NOTIF;
        try {
            Cursor cur = db.rawQuery(query, new String[] {});
            totalNotif = cur.getCount();
        } catch (Exception e) {
            Log.i("olla", getClass().getName() + " :: getAllMsgNotif() :: Error :: " + e.getMessage());
        } finally {
            db.close();
        }

        if (totalNotif < 40) {
            return;
        }

        query = "delete from " + TABLE_MSG_NOTIF + " where " + KEY_MSG_NOTIF_CNT + " in (" +
                "select " + KEY_MSG_NOTIF_CNT + " from " + TABLE_MSG_NOTIF + " order by " +
                KEY_MSG_NOTIF_CNT +" asc limit 10)";
        try {
            db.rawQuery(query, new String[] {});
        } catch (Exception e) {
            Log.i("olla", getClass().getName() + " :: getAllMsgNotif() :: Error :: " + e.getMessage());
        } finally {
            db.close();
        }
    }

    public ArrayList<String> getAllMsgNotif() {
        ArrayList<String> messages = new ArrayList<>();
        SQLiteDatabase db = this.getWritableDatabase();
        String sql = "select " + KEY_MSG_NOTIF_MSG + " from " + TABLE_MSG_NOTIF +
                " order by " + KEY_MSG_NOTIF_CNT + " desc";
        try {
            Cursor cur = db.rawQuery(sql, new String[]{});
            if (cur.moveToFirst()) {
                do {
                    messages.add(cur.getString(0));
                } while (cur.moveToNext());
            }
        } catch (Exception e) {
            Log.i("olla", getClass().getName() + " :: getAllMsgNotif() :: Error :: " + e.getMessage());
        } finally {
            db.close();
        }
        return messages;
    }

    public boolean isCounterPresent(long counter) {
        SQLiteDatabase db = this.getWritableDatabase();
        String sql = "select * from " + TABLE_MSG_NOTIF + " where " + KEY_MSG_NOTIF_CNT + "=" + String.valueOf(counter);
        try {
            Cursor cur = db.rawQuery(sql, new String[]{});
            if(cur.getCount() > 0) {
                return true;
            }
        } catch (Exception e) {
            Log.i("olla", getClass().getName() + " :: getAllMsgNotif() :: Error :: " + e.getMessage());
        } finally {
            db.close();
        }
        return false;
    }
}
