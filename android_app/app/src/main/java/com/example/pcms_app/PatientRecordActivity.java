package com.example.pcms_app;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

public class PatientRecordActivity extends AppCompatActivity {

    private Button btnRecord;
    private Button btnChat;

    private Bundle chatActivityBundle;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_patient_record);

        chatActivityBundle = getIntent().getExtras();


        btnRecord = (Button) findViewById(R.id.btnRecord);
        btnChat = (Button) findViewById(R.id.btnChat);

        btnChat.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                goToChatActivity(chatActivityBundle);
            }
        });


    } /* end of onCreate() */




    // this function parses the summary JSON within the response JSON
    private ArrayList<JSONObject> parseSummaryJSON(JSONArray assignments){
        ArrayList<JSONObject> assignmentList = new ArrayList<JSONObject>();

        if (assignments != null){
            for (int i = 0; i < assignments.length(); i++){
                try {
                    assignmentList.add((JSONObject) assignments.get(i));
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        }

        return assignmentList;
    }

    private void goToChatActivity(Bundle chatActivityBundle) {
        Intent chatIntent = new Intent(this, ChatActivity.class);

        chatIntent.putExtras(chatActivityBundle);

        startActivity(chatIntent);
    }
}