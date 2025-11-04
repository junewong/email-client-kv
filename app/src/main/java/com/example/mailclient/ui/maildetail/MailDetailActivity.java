package com.example.mailclient.ui.maildetail;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.example.mailclient.R;
import com.example.mailclient.data.mail.ImapClient;
import com.example.mailclient.data.model.Account;
import com.example.mailclient.data.model.Email;
import com.example.mailclient.data.repository.AccountRepository;
import com.example.mailclient.data.repository.EmailRepository;
import com.example.mailclient.ui.compose.ComposeActivity;
import com.example.mailclient.util.CryptoUtil;
import com.google.android.material.appbar.MaterialToolbar;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;
import java.util.concurrent.Executor;
import java.util.concurrent.Executors;

public class MailDetailActivity extends AppCompatActivity {
    private TextView fromText, toText, dateText, bodyText;
    private Button replyButton, forwardButton, deleteButton;
    private EmailRepository emailRepository;
    private AccountRepository accountRepository;
    private final Executor executor = Executors.newSingleThreadExecutor();
    private Email currentEmail;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_mail_detail);
        
        emailRepository = new EmailRepository(this);
        accountRepository = new AccountRepository(this);
        
        MaterialToolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        toolbar.setNavigationOnClickListener(v -> finish());
        
        fromText = findViewById(R.id.fromText);
        toText = findViewById(R.id.toText);
        dateText = findViewById(R.id.dateText);
        bodyText = findViewById(R.id.bodyText);
        replyButton = findViewById(R.id.replyButton);
        forwardButton = findViewById(R.id.forwardButton);
        deleteButton = findViewById(R.id.deleteButton);
        
        String emailUid = getIntent().getStringExtra("email_uid");
        loadEmail(emailUid);
        
        replyButton.setOnClickListener(v -> reply());
        forwardButton.setOnClickListener(v -> forward());
        deleteButton.setOnClickListener(v -> delete());
    }
    
    private void loadEmail(String uid) {
        emailRepository.getEmailByUid(uid, email -> {
            if (email == null) return;
            
            currentEmail = email;
            runOnUiThread(() -> {
                fromText.setText("发件人: " + email.getFrom());
                toText.setText("收件人: " + email.getTo());
                dateText.setText(formatDate(email.getDate()));
                if (getSupportActionBar() != null) {
                    getSupportActionBar().setTitle(email.getSubject());
                }
            });
            
            accountRepository.getDefaultAccount(account -> {
                if (account == null) return;
                
                executor.execute(() -> {
                    try {
                        String password = CryptoUtil.decrypt(account.getEncryptedPassword());
                        ImapClient client = new ImapClient();
                        client.connect(account.getImapServer(), account.getImapPort(),
                            account.getEmail(), password);
                        
                        String body = client.getEmailBody(email.getFolder(), uid);
                        client.disconnect();
                        
                        runOnUiThread(() -> bodyText.setText(body));
                    } catch (Exception e) {
                        runOnUiThread(() -> bodyText.setText("加载失败: " + e.getMessage()));
                    }
                });
            });
        });
    }
    
    private void reply() {
        if (currentEmail == null) return;
        Intent intent = new Intent(this, ComposeActivity.class);
        intent.putExtra("to", currentEmail.getFrom());
        intent.putExtra("subject", "Re: " + currentEmail.getSubject());
        startActivity(intent);
    }
    
    private void forward() {
        if (currentEmail == null) return;
        Intent intent = new Intent(this, ComposeActivity.class);
        intent.putExtra("subject", "Fwd: " + currentEmail.getSubject());
        startActivity(intent);
    }
    
    private void delete() {
        finish();
    }
    
    private String formatDate(long timestamp) {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.getDefault());
        return sdf.format(new Date(timestamp));
    }
}
