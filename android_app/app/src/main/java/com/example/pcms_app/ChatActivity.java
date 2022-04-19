package com.example.pcms_app;

import androidx.appcompat.app.AppCompatActivity;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import com.example.pcms_app.databinding.ActivityChatBinding;
import com.google.firebase.firestore.DocumentChange;
import com.google.firebase.firestore.EventListener;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.QuerySnapshot;
import java.io.ByteArrayOutputStream;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;

/*
The purpose of ChatActivity is to generate a chat system between two users.
Please refer to for more information: https://www.youtube.com/watch?v=EnyJsp5bMzs
 */

public class ChatActivity extends AppCompatActivity {

    /*
    viewBinding was enabled in build.gradle app so the
    ActivityChatBinding class is automatically generated from our layout file activity_chat
     */
    private ActivityChatBinding binding;
    private List<ChatMessage> chatMessages;
    private ChatAdapter chatAdapter;
    private FirebaseFirestore database;

    // Sender info
    private int senderUserID;

    // Receiver info
    private int receiverUserID;
    private String receiverFirstName;
    private String receiverLastName;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityChatBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        // get bundle passed from login activity
        Bundle loginBundle = getIntent().getExtras();

        // extract sender info from bundle
        senderUserID = loginBundle.getInt("senderUserID");

        // extract receiver info from bundle
        receiverUserID = loginBundle.getInt("receiverUserID");
        receiverFirstName = loginBundle.getString("receiverFirstName");
        receiverLastName = loginBundle.getString("receiverLastName");

        setListeners();
        loadReceiverDetails();
        init();
        listenMessages();
    }

    /*
    Instantiating chat UI and firebase
     */
    private void init() {
        chatMessages = new ArrayList<>();

        // convert hard coded profile pic to base 64 encoded string
        Bitmap profile = BitmapFactory.decodeResource(getApplicationContext().getResources(), R.drawable.profile);
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        profile.compress(Bitmap.CompressFormat.JPEG, 100, byteArrayOutputStream);
        byte[] bytes = byteArrayOutputStream.toByteArray();
        String encoded = Base64.encodeToString(bytes, Base64.DEFAULT);

        // loading past messages with sender profile
        chatAdapter = new ChatAdapter(
                chatMessages,
                // sender profile
                getBitmapFromEncodedString(encoded),
                // sender Id
                //preferenceManager.getString(Constants.KEY_USER_ID)
                String.valueOf(senderUserID)
        );
        binding.chatRecyclerView.setAdapter(chatAdapter);

        // start the instance of firebase and save it globally
        database = FirebaseFirestore.getInstance();
    }

    // send message and update database
    private void sendMessage() {
        Log.d("ChatActivity debug: ", "sendMessage");
        HashMap<String, Object> message = new HashMap<>();

        // set senderId
        message.put(Constants.KEY_SENDER_ID, String.valueOf(senderUserID));
        Log.d("ChatActivity debug senderId: ", String.valueOf(senderUserID));

        // set receiverId
        message.put(Constants.KEY_RECEIVER_ID, String.valueOf(receiverUserID));
        Log.d("ChatActivity debug receiverId: ", String.valueOf(receiverUserID));

        // set message
        message.put(Constants.KEY_MESSAGE, binding.inputMessage.getText().toString());
        Log.d("ChatActivity debug message: ", binding.inputMessage.getText().toString());

        // set timestamp
        message.put(Constants.KEY_TIMESTAMP, new Date());
        Log.d("ChatActivity debug date: ", new Date().toString());

        database.collection(Constants.KEY_COLLECTION_CHAT). add(message);
        binding.inputMessage.setText(null);
    }

    // Listen to message and update database
    private void listenMessages() {
        database.collection(Constants.KEY_COLLECTION_CHAT)
                .whereEqualTo(Constants.KEY_SENDER_ID, String.valueOf(senderUserID))
                .whereEqualTo(Constants.KEY_RECEIVER_ID, String.valueOf(receiverUserID))
                .addSnapshotListener(eventListener);
        database.collection(Constants.KEY_COLLECTION_CHAT)
                .whereEqualTo(Constants.KEY_SENDER_ID, String.valueOf(receiverUserID))
                .whereEqualTo(Constants.KEY_RECEIVER_ID, String.valueOf(senderUserID))
                .addSnapshotListener(eventListener);
    }

    // Event listener for new messages and continue updating ui
    private final EventListener<QuerySnapshot> eventListener = (value, error) -> {

        if (error != null) {
            return;
        }
        if (value != null) {
            int count = chatMessages.size();
            // load each message into list of messages
            for(DocumentChange documentChange : value.getDocumentChanges()) {
                if (documentChange.getType() == DocumentChange.Type.ADDED) {
                    ChatMessage chatMessage = new ChatMessage();
                    chatMessage.senderId = documentChange.getDocument().getString(Constants.KEY_SENDER_ID);
                    chatMessage.receiverId = documentChange.getDocument().getString(Constants.KEY_RECEIVER_ID);
                    chatMessage.message = documentChange.getDocument().getString(Constants.KEY_MESSAGE);
                    chatMessage.dateTime = getReadableDateTime(documentChange.getDocument().getDate(Constants.KEY_TIMESTAMP));
                    chatMessage.dateObject = documentChange.getDocument().getDate(Constants.KEY_TIMESTAMP);
                    chatMessages.add(chatMessage);
                }
            }
            Collections.sort(chatMessages, (obj1, obj2) -> obj1.dateObject.compareTo(obj2.dateObject));
            if (count == 0) {
                chatAdapter.notifyDataSetChanged();
            }
            else {
                /*
                Notify any registered observers that the itemCount items starting at position positionStart have changed.
                Equivalent to calling notifyItemRangeChanged(position, itemCount, null);.
                This is an item change event, not a structural change event.
                It indicates that any reflection of the data in the given position range is out of date and should be updated.
                The items in the given range retain the same identity.
                 */
                chatAdapter.notifyItemRangeChanged(chatMessages.size(), chatMessages.size());
                /*
                Starts a smooth scroll to an adapter position.
                 */
                binding.chatRecyclerView.smoothScrollToPosition(chatMessages.size() - 1);
            }
            binding.chatRecyclerView.setVisibility(View.VISIBLE);
        }
        binding.progressBar.setVisibility(View.GONE);
    };

    // Convert encoded string to bitmap
    private Bitmap getBitmapFromEncodedString (String encodedImage) {
        byte[] bytes = Base64.decode(encodedImage, Base64.DEFAULT);
        return BitmapFactory.decodeByteArray(bytes, 0, bytes.length);
    }

    // Receiver name on the top
    private void loadReceiverDetails() {
        binding.textName.setText(String.format("%s %s", receiverFirstName, receiverLastName));
    }

    // Button listeners
    private void setListeners() {
        // back button listener
        binding.imageBack.setOnClickListener(v->onBackPressed());
        // send button listener
        binding.layoutSend.setOnClickListener(v->sendMessage());
    }

    // Convert date time to simple date format
    private String getReadableDateTime(Date date) {
        return new SimpleDateFormat("MMMM dd, yyyy - hh:mm a", Locale.getDefault()).format(date);
    }
}