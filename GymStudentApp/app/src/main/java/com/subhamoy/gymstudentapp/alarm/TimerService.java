package com.subhamoy.gymstudentapp.alarm;

import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.media.Ringtone;
import android.media.RingtoneManager;
import android.net.Uri;
import android.os.IBinder;
import android.util.Log;

import androidx.annotation.Nullable;
import androidx.core.app.NotificationCompat;

import com.subhamoy.gymstudentapp.ConstantFBStudent;
import com.subhamoy.gymstudentapp.LaunchScreen;
import com.subhamoy.gymstudentapp.MainActivity;
import com.subhamoy.gymstudentapp.R;

import java.util.Timer;
import java.util.TimerTask;

public class TimerService extends Service {

    @Override
    public void onCreate() {
        super.onCreate();
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        notificationUpdate(1, "Welcome...Your time has started. You will be notified as " +
                "soon as your time expires");
        final int[] timeRemaining = {Integer.parseInt(intent.getStringExtra(ConstantFBStudent.INTENT_STR_TIME_LEFT))};
        final Timer timer = new Timer();
        timer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                Intent intentLocal = new Intent();
                intentLocal.setAction(ConstantFBStudent.INTENT_ACTION_TIME_COUNTER);
                timeRemaining[0] = timeRemaining[0] - 1000;
                if (timeRemaining[0] <= 0) {
                    simpleNotification(2, "Your time has expired. Please exit the gym. See you tomorrow. Bye Bye!");
                    timer.cancel();
                }
                intentLocal.putExtra(ConstantFBStudent.INTENT_STR_TIME_BACK, String.valueOf(timeRemaining[0]));
                sendBroadcast(intentLocal);
            }
        }, 0, 1000);
        return START_STICKY;
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    /**
     * Show Notification data
     */
    public void notificationUpdate(int index, String msg) {
        Intent notificationIntent = new Intent(this, LaunchScreen.class);
        final PendingIntent pendingIntent = PendingIntent.getActivity(this, 0, notificationIntent, 0);

        final Notification notifications = new NotificationCompat
                .Builder(this, ConstantFBStudent.NOTIFICATION_CHANNEL)
                .setContentTitle("GYMMS")
                .setContentText(msg.substring(0, 70) + "...")
                .setSmallIcon(R.drawable.ic_alert)
                .setContentIntent(pendingIntent)
                .setPriority(NotificationManager.IMPORTANCE_DEFAULT)
                .setStyle(new NotificationCompat.BigTextStyle()
                        .bigText(msg))
                .build();

        startForeground(index, notifications);
    }

    /**
     * Show Notification data
     */
    public void simpleNotification(int index, String msg) {
        Intent notificationIntent = new Intent(this, LaunchScreen.class);
        final PendingIntent pendingIntent = PendingIntent.getActivity(this, 0, notificationIntent, 0);

        final Notification notification = new NotificationCompat
                .Builder(this, ConstantFBStudent.NOTIFICATION_CHANNEL)
                .setContentTitle("GYMMS")
                .setContentText(msg.substring(0, 70) + "...")
                .setSmallIcon(R.drawable.ic_alert)
                .setContentIntent(pendingIntent)
                .setPriority(NotificationManager.IMPORTANCE_DEFAULT)
                .setStyle(new NotificationCompat.BigTextStyle()
                        .bigText(msg))
                .build();

        NotificationManager notificationManager = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
        notificationManager.notify(index, notification);
        playNotification(this);
    }

    private void playNotification (Context context) {
        Uri notification = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM);
        Ringtone r = RingtoneManager.getRingtone(context, notification);
        r.play();
    }


}
