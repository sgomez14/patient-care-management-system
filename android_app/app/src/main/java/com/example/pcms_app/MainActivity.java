package com.example.pcms_app;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Start WelcomeActivity
        Intent intent = new Intent(this, WelcomeActivity.class);
        startActivity(intent);
    }



}