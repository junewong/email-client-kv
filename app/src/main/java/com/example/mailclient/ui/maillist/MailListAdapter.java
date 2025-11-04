package com.example.mailclient.ui.maillist;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.mailclient.R;
import com.example.mailclient.data.model.Email;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class MailListAdapter extends RecyclerView.Adapter<MailListAdapter.ViewHolder> {
    private List<Email> emails = new ArrayList<>();
    private OnItemClickListener listener;
    
    public interface OnItemClickListener {
        void onItemClick(Email email);
    }
    
    public void setOnItemClickListener(OnItemClickListener listener) {
        this.listener = listener;
    }
    
    public void setEmails(List<Email> emails) {
        this.emails = emails;
        notifyDataSetChanged();
    }
    
    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
            .inflate(R.layout.item_mail, parent, false);
        return new ViewHolder(view);
    }
    
    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        Email email = emails.get(position);
        holder.senderText.setText(email.getFrom());
        holder.subjectText.setText(email.getSubject());
        holder.previewText.setText(email.getBody() != null ? email.getBody() : "");
        holder.dateText.setText(formatDate(email.getDate()));
        
        holder.itemView.setOnClickListener(v -> {
            if (listener != null) listener.onItemClick(email);
        });
    }
    
    @Override
    public int getItemCount() {
        return emails.size();
    }
    
    private String formatDate(long timestamp) {
        SimpleDateFormat sdf = new SimpleDateFormat("MM-dd HH:mm", Locale.getDefault());
        return sdf.format(new Date(timestamp));
    }
    
    static class ViewHolder extends RecyclerView.ViewHolder {
        TextView senderText, subjectText, previewText, dateText;
        
        ViewHolder(View view) {
            super(view);
            senderText = view.findViewById(R.id.senderText);
            subjectText = view.findViewById(R.id.subjectText);
            previewText = view.findViewById(R.id.previewText);
            dateText = view.findViewById(R.id.dateText);
        }
    }
}
