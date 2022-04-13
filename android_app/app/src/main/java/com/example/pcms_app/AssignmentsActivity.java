package com.example.pcms_app;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;

import org.w3c.dom.Text;

import java.util.ArrayList;

public class AssignmentsActivity extends AppCompatActivity {

    private static final String DOCTOR = "doctor";
    private static final String PATIENT = "patient";
    private String userRole;
    private int userID;

    // list to store the assignments for user
    private ArrayList<String> assignmentList;

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
            assignmentList.add("Santiago Gomez");
        }
        else if (userRole.contains(PATIENT)){
            // patient role, DO SOMETHING
            tvAssignmentLabel.setText("Assigned Doctors");
            assignmentList.add("Mandy Yao");
        }




    }
}