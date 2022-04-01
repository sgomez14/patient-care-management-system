package com.example.pcms_app;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.AppCompatButton;
import androidx.viewpager.widget.ViewPager;

import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;

import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.tabs.TabLayout;

public class LoginActivity extends AppCompatActivity {

    TabLayout tabLayout;
    ViewPager viewPager;
    AppCompatButton btnGoogle, btnLogin;
    EditText userName, password;
    float v = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        tabLayout = findViewById(R.id.tabLayout);
        viewPager = findViewById(R.id.viewPager);
        btnGoogle = findViewById(R.id.btnGoogle);
        btnLogin = findViewById(R.id.btnLogin);
        userName = findViewById(R.id.userName);
        password = findViewById(R.id.password);

        userName.setTranslationY(300);
        password.setTranslationY(300);
        btnLogin.setTranslationY(300);
        btnGoogle.setTranslationY(300);

        userName.setAlpha(v);
        password.setAlpha(v);
        btnLogin.setAlpha(v);
        btnGoogle.setAlpha(v);

        btnLogin.animate().translationY(0).alpha(1).setDuration(1500).setStartDelay(100).start();
        password.animate().translationY(0).alpha(1).setDuration(1500).setStartDelay(100).start();
        userName.animate().translationY(0).alpha(1).setDuration(1500).setStartDelay(100).start();
        btnGoogle.animate().translationY(0).alpha(1).setDuration(1500).setStartDelay(100).start();
    }
}