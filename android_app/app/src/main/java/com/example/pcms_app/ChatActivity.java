package com.example.pcms_app;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.widget.EditText;
import android.widget.Toast;

import com.example.pcms_app.databinding.ActivityChatBinding;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.messaging.FirebaseMessaging;

public class ChatActivity extends AppCompatActivity {

    // viewBinding was enabled in build.gradle app so the ActivityChatBinding class is automatically generated from our layout file activity_chat
    private ActivityChatBinding binding;
    private static final String userName = "Mandy Yao"; // pretend we got this from bundle
    private static final String userID = "42530"; // pretend we got this from bundle

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityChatBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());
        setBackListeners();
        loadReceiverDetails();
    }

    private void loadReceiverDetails() {
        binding.textName.setText(userName);
    }

    private void setBackListeners() {
        binding.imageBack.setOnClickListener(v->onBackPressed());
    }
}