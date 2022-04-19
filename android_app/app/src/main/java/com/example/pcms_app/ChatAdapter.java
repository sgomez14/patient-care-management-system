package com.example.pcms_app;

import android.graphics.Bitmap;
import android.view.LayoutInflater;
import android.view.ViewGroup;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import com.example.pcms_app.databinding.ItemContainerReceivedMessageBinding;
import com.example.pcms_app.databinding.ItemContainerSentMessageBinding;
import java.util.List;

/*
The purpose of the ChatAdapter is to inflate RecyclerViews.
Please refer to for more information: https://www.youtube.com/watch?v=EnyJsp5bMzs
 */
public class ChatAdapter extends RecyclerView.Adapter<RecyclerView.ViewHolder>{

    private final List<ChatMessage> chatMessages;
    private final Bitmap receiverProfileImage;
    private final String senderId;

    public static final int VIEW_TYPE_SENT = 1;
    public static final int VIEW_TYPE_RECEIVED = 2;

    public ChatAdapter(List<ChatMessage> chatMessages, Bitmap receiverProfileImage, String senderId) {
        this.chatMessages = chatMessages;
        this.receiverProfileImage = receiverProfileImage;
        this.senderId = senderId;
    }

    /*
    The ViewHolder references to the views inside
    the inflated item-layout file.
    onCreate checks type and calls either sender or receiver ViewHolder functions
     */
    @NonNull
    @Override
    public RecyclerView.ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        if (viewType == VIEW_TYPE_SENT) {
            return new SentMessageViewHolder(
                    ItemContainerSentMessageBinding.inflate(
                            LayoutInflater.from(parent.getContext()),
                            parent,
                            false
                    )
            );
        }
        else {
            return new ReceivedMessageViewHolder(
                    ItemContainerReceivedMessageBinding.inflate(
                            LayoutInflater.from(parent.getContext()),
                            parent,
                            false
                    )
            );
        }
    }

    /*
    if it's sender position, inflate sender messages
    if it's receiver position, inflate receiver messages and profile picture
     */
    @Override
    public void onBindViewHolder(@NonNull RecyclerView.ViewHolder holder, int position) {
        if (getItemViewType(position) == VIEW_TYPE_SENT) {
            ((SentMessageViewHolder) holder).setData(chatMessages.get(position));
        }
        else {
            ((ReceivedMessageViewHolder) holder).setData(chatMessages.get(position), receiverProfileImage);
        }
    }

    /*
    Return total message counts
     */
    @Override
    public int getItemCount() {
        return chatMessages.size();
    }

    /*
    Check to see if it's sender or receiver view
     */
    @Override
    public int getItemViewType(int position) {
        if (chatMessages.get(position).senderId.equals(senderId)) {
            return VIEW_TYPE_SENT;
        }
        else {
            return VIEW_TYPE_RECEIVED;
        }
    }


    /*
    The ViewHolder references to the views inside
    the inflated item-layout file.
    These references are used to load new data into the
    views every time the layout is recycled to show the new data.
    */
    static class SentMessageViewHolder extends RecyclerView.ViewHolder {

        // ItemContainerSentMessageBinding class is automatically generated from layout file item_container_sent_message
        private final ItemContainerSentMessageBinding binding;

        SentMessageViewHolder(ItemContainerSentMessageBinding itemContainerSentMessageBinding) {
            super(itemContainerSentMessageBinding.getRoot());
            binding = itemContainerSentMessageBinding;
        }

        void setData(ChatMessage chatMessage) {
            binding.textMessage.setText(chatMessage.message);
            binding.textDateTime.setText(chatMessage.dateTime);
        }
    }

    /*
    The ViewHolder references to the views inside
    the inflated item-layout file.
    These references are used to load new data into the
    views every time the layout is recycled to show the new data.
     */
    static class ReceivedMessageViewHolder extends RecyclerView.ViewHolder {

        // ItemContainerReceivedMessageBinding class is automatically generated from layout file item_container_received_message
        private final ItemContainerReceivedMessageBinding binding;

        ReceivedMessageViewHolder(ItemContainerReceivedMessageBinding itemContainerReceivedMessageBinding) {
            super(itemContainerReceivedMessageBinding.getRoot());
            binding = itemContainerReceivedMessageBinding;
        }

        void setData(ChatMessage chatMessage, Bitmap receiverProfileImage) {
            binding.textMessage.setText(chatMessage.message);
            binding.textDateTime.setText(chatMessage.dateTime);
            binding.imageProfile.setImageBitmap(receiverProfileImage);
        }
    }
}
