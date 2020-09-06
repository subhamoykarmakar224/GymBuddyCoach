package com.subhamoy.gymstudentapp.alarm;

import android.app.AlertDialog;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.media.Ringtone;
import android.media.RingtoneManager;
import android.net.Uri;
import android.widget.Toast;

import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;

import com.subhamoy.gymstudentapp.ConstantFBStudent;
import com.subhamoy.gymstudentapp.R;

public class ExecutableService extends BroadcastReceiver {

    AlertDialog.Builder alertBuilder;

    @Override
    public void onReceive(Context context, Intent intent) {
        Toast.makeText(context, "Your Time is Up! Please exit the premises to make way for next slot. Thank you for working out today. See you tomorrow!", Toast.LENGTH_LONG).show();
        showNotification(context);
        playNotification(context);

    }

    private void playNotification (Context context) {
        Uri notification = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM);
        Ringtone r = RingtoneManager.getRingtone(context, notification);
        r.play();
        r.play();
    }

    private void showNotification(Context context) {
        NotificationCompat.Builder builder = new NotificationCompat.Builder(context, ConstantFBStudent.NOTIFICATION_CHANNEL)
                .setSmallIcon(R.drawable.ic_alert)
                .setContentTitle("Time's Up!")
                .setContentText("Thank you for working out today...")
                .setStyle(new NotificationCompat.BigTextStyle()
                        .bigText("Thank you for working out today. Please make way for the nest slot. See you tomorrow! Bye Bye!")
                )
                .setPriority(NotificationCompat.PRIORITY_DEFAULT);
        NotificationManagerCompat notificationManagerCompat = NotificationManagerCompat.from(context);
        notificationManagerCompat.notify(200, builder.build());
    }
}
