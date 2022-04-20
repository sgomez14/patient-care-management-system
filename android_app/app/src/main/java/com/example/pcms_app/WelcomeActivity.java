package com.example.pcms_app;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.AppCompatButton;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;

import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class WelcomeActivity extends AppCompatActivity {

    ImageView doc1, doc2, star1, star2;
    AppCompatButton btnNext;
    float v=0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_welcome);

        // Instantiate views
        doc1 = findViewById(R.id.doc1);
        doc2 = findViewById(R.id.doc2);
        star1 = findViewById(R.id.star1);
        star2 = findViewById(R.id.star2);
        btnNext = findViewById(R.id.btnNext);

        // Auto reload animation every seconds
        ScheduledExecutorService scheduledExecutorService =
                Executors.newSingleThreadScheduledExecutor();
        scheduledExecutorService.scheduleAtFixedRate(new Runnable() {
            @Override
            public void run() {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        shake(star1);
                        shake(star2);

                    }
                });
            }
        }, 0, 1, TimeUnit.SECONDS);


        // doc1 and doc2 animations pop up
        doc1.setTranslationY(300);
        doc2.setTranslationY(100);

        doc1.setAlpha(v);
        doc2.setAlpha(v);

        doc1.animate().translationY(0).alpha(1).setDuration(1500).setStartDelay(100).start();
        doc2.animate().translationY(0).alpha(1).setDuration(1000).setStartDelay(100).start();

        // Next button to start LoginActivity
        btnNext.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(WelcomeActivity.this, LoginActivity.class);
                startActivity(intent);
            }
        });
    }

    // Shake animation
    private void shake(ImageView img) {
        Animation shake = AnimationUtils.loadAnimation(getApplicationContext(), R.anim.shake);
        img.startAnimation(shake);
    }
}