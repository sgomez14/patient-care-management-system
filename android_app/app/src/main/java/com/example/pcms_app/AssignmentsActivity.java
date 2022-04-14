package com.example.pcms_app;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
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
import org.w3c.dom.Text;

import java.util.ArrayList;

public class AssignmentsActivity extends AppCompatActivity {

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

    private static final String API_BASE_URL = "http://10.0.2.2:5000/users/get-assignments/";

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
//            assignmentList.add("Santiago Gomez");
        }
        else if (userRole.contains(PATIENT)){
            // patient role, DO SOMETHING
            tvAssignmentLabel.setText("Assigned Doctors");
//            assignmentList.add("Mandy Yao");
        }

        // make call to Users REST API
        getAssignments(userID);






    }

    // Function to authenticate username and password through Restful API
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
    }

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
    }

    private void addRowData(){
        // add row elements to the listview
        for (JSONObject record : assignmentsListJSON){
            String name = "";
            String recordUserID = "";
            try {
                name = record.getString("name");
                recordUserID = record.getString("user_id");
            } catch (JSONException e) {
                e.printStackTrace();
            }
            String rowData = name + ", ID: " + recordUserID;
            assignmentList.add(rowData);
        }
        adapter.notifyDataSetChanged();
    }
}