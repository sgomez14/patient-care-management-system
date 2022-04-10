package com.example.pcms_app;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.AppCompatButton;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import org.json.JSONObject;
import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;

public class LoginActivity extends AppCompatActivity {

    private AppCompatButton btnGoogle, btnLogin;
    private EditText userName, password;
    private float v = 0;
    private String role = "";
    private static final String DOCTOR = "doctor";
    private static final String PATIENT = "patient";
    private static final String API_BASE_URL = "http://10.0.2.2:5000/users/authenticate-login/";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        // Instantiate views
        btnGoogle = findViewById(R.id.btnGoogle);
        btnLogin = findViewById(R.id.btnLogin);
        userName = findViewById(R.id.userName);
        password = findViewById(R.id.password);

        // Call animation function for log-in preview UI
        animation();

        // Log in button listener
        btnLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                // Authenticate username and password
                callAuthenticateLoginAndReturnRole();
                if (role.contains(DOCTOR)) {
                    // doctor role, DO SOMETHING
                }
                else if (role.contains(PATIENT)){
                    // patient role, DO SOMETHING
                }
            }
        });
    }

    private void animation() {

        // Login UI views translate upward from bottom of screen
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

    // Function to authenticate username and password through Restful API
    private void callAuthenticateLoginAndReturnRole() {

        // Instantiate request queue using volley to call Restful API
        RequestQueue requestQueue = Volley.newRequestQueue(LoginActivity.this);

        // Append username and password to url as parameters
        String url = appendParameterToUrl();

        // Create json object request for api
        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(
                Request.Method.GET,
                url,
                null,

                // Response listener
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        Log.e("PCMS onResponse", response.toString());
                        try {
                            role = response.getString("user_roles");
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
                            String body = new String(error.networkResponse.data, "UTF-8");
                        } catch (UnsupportedEncodingException e) {
                            Log.e("PCMS Exception", e.getMessage());
                        }
                    }
                }
        );
        requestQueue.add(jsonObjectRequest);
    }

    // convert parameters into Base 64 string and append it to url
    private String appendParameterToUrl() {
        int getUserName = Integer.parseInt(userName.getText().toString());
        String getPassword = password.getText().toString();
        try {
            String param = String.format("{" + "\"user_id\"" + ":" + getUserName + "," + "\"password\"" + ":"  + "\"%s\"" + "}", getPassword);
            String encodedParam = URLEncoder.encode(param, "UTF-8");
            return API_BASE_URL + encodedParam;
        }
        catch (Exception e) {
            Log.d("PCMS Exception", e.getMessage());
            return API_BASE_URL;
        }
    }
}