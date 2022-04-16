package com.example.pcms_app;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

public class PatientRecordActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_patient_record);
    }

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
}