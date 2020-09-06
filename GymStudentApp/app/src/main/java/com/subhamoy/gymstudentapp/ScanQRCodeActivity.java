package com.subhamoy.gymstudentapp;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.app.Activity;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.util.Log;
import android.util.SparseArray;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.widget.TextView;

import com.google.android.gms.vision.CameraSource;
import com.google.android.gms.vision.Detector;
import com.google.android.gms.vision.barcode.Barcode;
import com.google.android.gms.vision.barcode.BarcodeDetector;

import java.io.IOException;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;

public class ScanQRCodeActivity extends AppCompatActivity {

    SurfaceView surfaceView;
    TextView textView;

    CameraSource cameraSource;
    BarcodeDetector barcodeDetector;

    // Permissions
    String [] PERMISSIONS = {
            Manifest.permission.CAMERA
    };
    private static final int requestCode = 1234;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_scan_qr_code);

        // Widgets
        surfaceView = findViewById(R.id.cameraPreview);
        textView = findViewById(R.id.textView);

        // Other object initialization
        barcodeDetector = new BarcodeDetector.Builder(this)
                .setBarcodeFormats(Barcode.QR_CODE)
                .build();
        cameraSource = new CameraSource.Builder(this, barcodeDetector)
                .setAutoFocusEnabled(true)
                .setRequestedPreviewSize(640, 480)
                .build();

        surfaceView.getHolder().addCallback(new SurfaceHolder.Callback() {
            @Override
            public void surfaceCreated(SurfaceHolder holder) {
                try {
                    if (ActivityCompat.checkSelfPermission(ScanQRCodeActivity.this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
                        getPermissions();
                        return;
                    }
                    cameraSource.start(holder);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }

            @Override
            public void surfaceChanged(SurfaceHolder holder, int format, int width, int height) {
            }

            @Override
            public void surfaceDestroyed(SurfaceHolder holder) {
                cameraSource.stop();
            }
        });

        barcodeDetector.setProcessor(new Detector.Processor<Barcode>() {
            @Override
            public void release() { }

            @Override
            public void receiveDetections(Detector.Detections<Barcode> detections) {
                final SparseArray<Barcode> qrCodes = detections.getDetectedItems();
                if(qrCodes.size() != 0) {
                    String qrCodeValue = qrCodes.valueAt(0).displayValue;
                    String today = getNormalizedDateFormat(new Date());
                    Intent intent = new Intent(ScanQRCodeActivity.this, MainActivity.class);
                    intent.putExtra("QRCODE_SCAN_DATA", qrCodeValue);
                    intent.putExtra("QRCODE_SCAN_DATE", today);
                    setResult(Activity.RESULT_OK, intent);
                    finish();
                }
            }
        });
    }

    /**
     * Get date in format dd-mm-yyyy
     * @param date
     * @return
     */
    public String getNormalizedDateFormat(Date date) {
        DateFormat dateFormat = new SimpleDateFormat("dd-MM-yyyy");
        return dateFormat.format(date);
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
}