package com.example.pcms_app;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
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

public class AssignmentsActivity extends AppCompatActivity {

    private static final String API_BASE_URL = "http://10.0.2.2:5000/users/get-assignments/";
//    private static final String API_BASE_URL = "http://192.168.99.61:5000/users/get-assignments/"; // Santiago home server
//    private static final String API_BASE_URL = "http://10.192.3.123:5000/users/get-assignments/";

    private static final String DOCTOR = "doctor";
    private static final String PATIENT = "patient";
    private String userRole;
    private int userID;

    // list to store the assignments for user
    private ArrayList<String> assignmentList;
    private ArrayList<JSONObject> assignmentsListJSON;

    // array adapter needed for list view
    private ArrayAdapter<String> adapter;

    private TextView tvAssignmentLabel;
    private ListView lvAssignments;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_assignments);

        // get access to the assignments label textview
        tvAssignmentLabel = (TextView) findViewById(R.id.tvAssignmentLabel);

        // get access to the listview element
        lvAssignments = (ListView) findViewById(R.id.lvAssignments);

        // section for setting up the listview
        assignmentList = new ArrayList<>();
        adapter = new ArrayAdapter<>(getApplicationContext(), android.R.layout.simple_spinner_item, assignmentList);
        lvAssignments.setAdapter(adapter);

        // get bundle passed from login activity
        Bundle loginBundle = getIntent().getExtras();

        // extract info from the bundle
        userRole = loginBundle.getString("userRole");
        userID = loginBundle.getInt("userID");

        // log the user role receive
        Log.e("PCMS", "The user role received from login screen: " + userRole);

        if (userRole.contains(DOCTOR)) {
            // doctor role, DO SOMETHING
            tvAssignmentLabel.setText("Assigned Patients");
        }
        else if (userRole.contains(PATIENT)){
            // patient role, DO SOMETHING
            tvAssignmentLabel.setText("Assigned Doctors");
        }

        // make call to Users REST API
        getAssignments(userID);

        // create the listener that takes user to the Patient Record Activity
        lvAssignments.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                sendRowDataToRecordActivity(position);
            }
        });
    } /* end of onCreate() */

    // Function to get the user's assignments through Restful API
    private void getAssignments(int userID) {

        // Instantiate request queue using volley to call Restful API
        RequestQueue requestQueue = Volley.newRequestQueue(AssignmentsActivity.this);

        // Append username and password to url as parameters
        String url = API_BASE_URL + userID;

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

                            // set the assignmentsListJSON
                            assignmentsListJSON =
                                    new ArrayList<JSONObject>(parseAssignmentsJSON(
                                            response.getJSONArray("assignments")));

                            addRowData();
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
    } /* end of getAssignments() */

    // this function parses the assignments records within the response JSON
    private ArrayList<JSONObject> parseAssignmentsJSON(JSONArray assignments){
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
    } /* end of parseAssignmentsJSON() */

    private void addRowData(){
        // add row elements to the listview
        for (JSONObject record : assignmentsListJSON){
            String name = "";
            String recordUserID = "";
            try {
                name = record.getString("name");
                recordUserID = record.getString("user_id");
            } catch (JSONException e) {
                Log.e("PCMS", "Error Parsing JSON when adding row data: " +
                        e.getMessage());
            }
            String rowData = name + ", ID: " + recordUserID;
            assignmentList.add(rowData);
        }
        adapter.notifyDataSetChanged();
    } /* end of addRowData() */

    private void sendRowDataToRecordActivity(int index){
        String name = "";
        String recordUserID = "";
        JSONObject record = assignmentsListJSON.get(index); // grab the row in the list
        try {
            // every JSON record --> {"name": full_name, "user_id": user_id}
            name = record.getString("name");
            recordUserID = record.getString("user_id");

            // create intent to go to the Patient Record Activity
            goToPatientRecord(name, Integer.parseInt(recordUserID));

        } catch (JSONException e) {
            Log.e("PCMS", "Error Parsing JSON when getting row data: " +
                    e.getMessage());
        }
    } /* end of sendRowDataToRecordActivity() */

    private void goToPatientRecord(String rowName, int rowID){
        // create intent to go to the Patient Record activity
        Intent patientRecordIntent = new Intent(this, PatientRecordActivity.class);

        // create Bundle to pass user role and user id to the next activity
        Bundle patientRecordBundle = new Bundle();

        // add sender and receiver info for Chat
        patientRecordBundle.putInt("senderUserID", userID);  // individual using the app is always the sender in chat
        patientRecordBundle.putInt("receiverUserID", rowID); // individual selected from list is always the receiver in chat

        // split the rowName into separate first and last
        String[] fullNameSplit = rowName.split(" ");
        patientRecordBundle.putString("receiverFirstName", fullNameSplit[0]);
        patientRecordBundle.putString("receiverLastName", fullNameSplit[1]);

        if (userRole.equals(DOCTOR)){
            // the user is a doctor and they tapped on patient, so pass along name and ID in the row data to bundle
            patientRecordBundle.putInt("patientID", rowID);
        }
        else{
            // the user in this case is the patient, so just pass their userID along
            patientRecordBundle.putInt("patientID", userID);

        }

        // pair the bundle with the intent
        patientRecordIntent.putExtras(patientRecordBundle);

        // start the intent
        startActivity(patientRecordIntent);
    } /* end of goToPatientRecord() */
};