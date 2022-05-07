package com.example.pcms_app;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.android.volley.NetworkResponse;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

public class PatientRecordActivity extends AppCompatActivity {

    private static final String API_SUMMARY_URL = "http://10.0.2.2:5000/users/get-patient-summary/";
//    private static final String API_SUMMARY_URL = "http://192.168.99.61:5000/users/get-patient-summary/";
    private static final String API_MEASUREMENTS_URL = "http://10.0.2.2:5000/users/get-all-recent-measurements/";
//    private static final String API_BASE_URL = "http://192.168.99.61:5000/users/get-patient-summary/";
//    private static final String API_BASE_URL = "http://168.122.223.67:5000/users/get-patient-summary/";


//    private Button btnRecord;
    private Button btnChat;

    private TextView tvPatientName;
    private TextView tvPatientNameLabel;
    private TextView tvPatientID;
    private TextView tvPatientIDLabel;
    private TextView tvPatientHeight;
    private TextView tvPatientHeightLabel;
    private TextView tvPatientWeight;
    private TextView tvPatientWeightLabel;
    private TextView tvPatientAllergies;
    private TextView tvPatientAllergiesLabel;
    private TextView tvPatientMedication;
    private TextView tvPatientMedicationLabel;
    private TextView tvPatientMedicalConditions;
    private TextView tvPatientMedicalConditionsLabel;


    private TextView tvTemp;
    private TextView tvBloodPressure;
    private TextView tvPulse;
    private TextView tvOximeter;
    private TextView tvWeight;
    private TextView tvGlucometer;


    // variables to store patient summary information
    private String patientName;
    private String patientID;
    private String patientHeight;
    private String patientWeight;
    private String patientAllergies;
    private String patientMedication;
    private String patientMedicalConditions;

    // variables to store patient recent measurements
    private String patientTemp;
    private String patientBloodPressure;
    private String patientPulse;
    private String patientOximeter;
    private String patientWeightRecent;
    private String patientGlucometer;



    // variable to store bundle passed from Assignments Activity
    private Bundle chatActivityBundle;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_patient_record);

        // get the bundle passed from Assignments Activity
        // this bundle is forwarded to the Chat Activity
        chatActivityBundle = getIntent().getExtras();



        // get reference to summary GUI elements
        // summary elements
        tvPatientName                   = (TextView) findViewById(R.id.tvPatientName);
        tvPatientNameLabel              = (TextView) findViewById(R.id.tvPatientNameLabel);
        tvPatientID                     = (TextView) findViewById(R.id.tvPatientID);
        tvPatientIDLabel                = (TextView) findViewById(R.id.tvPatientIDLabel);
        tvPatientHeight                 = (TextView) findViewById(R.id.tvPatientHeight);
        tvPatientHeightLabel            = (TextView) findViewById(R.id.tvPatientHeightLabel);
        tvPatientWeight                 = (TextView) findViewById(R.id.tvPatientWeight);
        tvPatientWeightLabel            = (TextView) findViewById(R.id.tvPatientWeightLabel);
        tvPatientAllergies              = (TextView) findViewById(R.id.tvPatientAllergies);
        tvPatientAllergiesLabel         = (TextView) findViewById(R.id.tvPatientAllergiesLabel);
        tvPatientMedication             = (TextView) findViewById(R.id.tvPatientMedication);
        tvPatientMedicationLabel        = (TextView) findViewById(R.id.tvPatientMedicationLabel);
        tvPatientMedicalConditions      = (TextView) findViewById(R.id.tvPatientMedicalConditions);
        tvPatientMedicalConditionsLabel = (TextView) findViewById(R.id.tvPatientMedicalConditionsLabel);
        // recent measurements elements
        tvTemp           = (TextView) findViewById(R.id.tvTemp);
        tvBloodPressure  = (TextView) findViewById(R.id.tvBloodPressure);
        tvPulse          = (TextView) findViewById(R.id.tvPulse);
        tvOximeter       = (TextView) findViewById(R.id.tvOximeter);
        tvWeight         = (TextView) findViewById(R.id.tvWeight);
        tvGlucometer     = (TextView) findViewById(R.id.tvGlucometer);







        // get button GUI reference and setup onclicklistener
        btnChat = (Button) findViewById(R.id.btnChat);
        btnChat.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                goToChatActivity(chatActivityBundle);
            }
        });

        // make call to API to get the patient's summary
        getSummary(chatActivityBundle.getInt("patientID"));

        // make call to API to get the patient's recent measurements
        getRecentMeasurements(chatActivityBundle.getInt("patientID")); 



    } /* end of onCreate() */


    // Function to get a patient's summary through Restful API
    private void getSummary(int userID) {

        // Instantiate request queue using volley to call Restful API
        RequestQueue requestQueue = Volley.newRequestQueue(PatientRecordActivity.this);

        // Append username and password to url as parameters
        String url = API_SUMMARY_URL + userID;

        // Create json object request for api
        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(
                Request.Method.GET,
                url,
                null,

                // Response listener
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        Log.i("PCMS onResponse", response.toString());
                        try {

                            // process the response
                            parseSummaryJSON(response.getJSONObject("summary"));
                        }
                        catch (Exception e) {
                            Log.e("PCMS Exception", e.getMessage());
                        }
                    }
                },

                // Error listener
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Log.e("PCMS onErrorResponse", error.toString());
                        try {
//                            String body = new String(error.networkResponse.data, "UTF-8");
                            NetworkResponse response = error.networkResponse;
                            String errorMsg = "";
                            if(response != null && response.data != null){
                                String errorString = new String(response.data);
                                Log.i("log error", errorString);
                            }
                        } catch (/*UnsupportedEncodingException*/ Exception e) {
                            Log.e("PCMS Exception", e.getMessage());
                        }
                    }
                }
        );
        requestQueue.add(jsonObjectRequest);
    } /* end of getSummary() */


    // Function to get a patient's recent measurements through Restful API
    private void getRecentMeasurements(int userID) {

        // Instantiate request queue using volley to call Restful API
        RequestQueue requestQueue = Volley.newRequestQueue(PatientRecordActivity.this);

        // Append username and password to url as parameters
        String url = API_MEASUREMENTS_URL + userID;

        // Create json object request for api
        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(
                Request.Method.GET,
                url,
                null,

                // Response listener
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        Log.i("PCMS onResponse", response.toString());
                        try {

                            // process the response
                            parseMeasurementsJSON(response.getJSONObject("measurements"));
                        }
                        catch (Exception e) {
                            Log.e("PCMS Exception", e.getMessage());
                        }
                    }
                },

                // Error listener
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Log.e("PCMS onErrorResponse", error.toString());
                        try {
//                            String body = new String(error.networkResponse.data, "UTF-8");
                            NetworkResponse response = error.networkResponse;
                            String errorMsg = "";
                            if(response != null && response.data != null){
                                String errorString = new String(response.data);
                                Log.i("log error", errorString);
                            }
                        } catch (/*UnsupportedEncodingException*/ Exception e) {
                            Log.e("PCMS Exception", e.getMessage());
                        }
                    }
                }
        );
        requestQueue.add(jsonObjectRequest);
    } /* end of getRecentMeasurements() */


    // this function parses the summary JSON within the response JSON
    private void parseSummaryJSON(JSONObject summary) throws JSONException {

        // expecting a JSON in this format:
        /*
            {
                "user_id": 321,
                "name": "test_patient_first test_patient_last",
                "height": "5 ft. 1 in.",
                "weight": "150 lbs.",
                "allergies": ["rain"],
                "medication": ["happiness"],
                "medical_conditions": ["high blood pressure"]
            }
       */
        if (summary != null){
            patientID   = Integer.toString(summary.getInt("user_id"));
            patientName = summary.getString("name");
            patientHeight = summary.getString("height");
            patientWeight = summary.getString("weight");

            // parse the allergies array
            patientAllergies = parseSummaryJSONArray(summary.getJSONArray("allergies"));

            // parse the medication array
            patientMedication = parseSummaryJSONArray(summary.getJSONArray("medication"));

            // parse the medical conditions array
            patientMedicalConditions =
                    parseSummaryJSONArray(summary.getJSONArray("medical_conditions"));


            // set the UI
            tvPatientID.setText(patientID);
            tvPatientName.setText(patientName);
            tvPatientHeight.setText(patientHeight);
            tvPatientWeight.setText(patientWeight);
            tvPatientAllergies.setText(patientAllergies);
            tvPatientMedication.setText(patientMedication);
            tvPatientMedicalConditions.setText(patientMedicalConditions);

        }
        else {
            Log.e("PCMS Exception", "JSON object passed to parseSummaryJSON is null.");
        }
    }

    private String parseSummaryJSONArray(JSONArray jsonArray) throws JSONException {
        int len = jsonArray.length();
        StringBuilder stringBuilder = new StringBuilder(); // initialize allergies string
        for (int i = 0; i < len; i++){
            if (i > 0 && i < len-1){ // no commas at beginning or end
                stringBuilder.append(", ");
            }
            stringBuilder.append(jsonArray.get(i));
        }

        return stringBuilder.toString();
    }

    // this function parses the Measurements JSON within the response JSON
    private void parseMeasurementsJSON(JSONObject measurements) throws JSONException {

        // expecting a JSON in this format:
        /*
            {
                "temperature": "100.1 F Date: 2022-04-27 00:35:28",
                "blood_pressure": "115/70 mmHg Date: 2022-04-27 00:45:28",
                "pulse": "Measurement not in record.",
                "oximeter": "Measurement not in record.",
                "weight": "Measurement not in record.",
                "glucometer": "Measurement not in record."
            }
       */
        if (measurements != null){
            patientTemp          = measurements.getString("temperature");
            patientBloodPressure = measurements.getString("blood_pressure");
            patientPulse         = measurements.getString("pulse");
            patientOximeter      = measurements.getString("oximeter");
            patientWeightRecent  = measurements.getString("weight");
            patientGlucometer    = measurements.getString("glucometer");

            String temp =  getResources().getString(R.string.temperature) + patientTemp;
            String bp =  getResources().getString(R.string.blood_pressure) + patientBloodPressure;
            String pulse =  getResources().getString(R.string.pulse) + patientPulse;
            String oximeter =  getResources().getString(R.string.oximeter) + patientOximeter;
            String weightRecent =  getResources().getString(R.string.weight) + patientWeightRecent;
            String glucometer =  getResources().getString(R.string.glucometer) + patientGlucometer;

            // set the UI
            tvTemp.setText(temp);
            tvBloodPressure.setText(bp);
            tvPulse.setText(pulse);
            tvOximeter.setText(oximeter);
            tvWeight.setText(weightRecent);
            tvGlucometer.setText(glucometer);


        }
        else {
            Log.e("PCMS Exception", "JSON object passed to parseSummaryJSON is null.");
        }
    }

    private void goToChatActivity(Bundle chatActivityBundle) {
        Intent chatIntent = new Intent(this, ChatActivity.class);

        chatIntent.putExtras(chatActivityBundle);

        startActivity(chatIntent);
    }
};