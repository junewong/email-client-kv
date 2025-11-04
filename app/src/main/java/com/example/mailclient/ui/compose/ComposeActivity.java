package com.example.mailclient.ui.compose;

import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.mailclient.R;
import com.example.mailclient.data.mail.SmtpClient;
import com.example.mailclient.data.repository.AccountRepository;
import com.example.mailclient.util.CryptoUtil;
import com.google.android.material.appbar.MaterialToolbar;
import com.google.android.material.textfield.TextInputEditText;

import java.util.concurrent.Executor;
import java.util.concurrent.Executors;

public class ComposeActivity extends AppCompatActivity {
    private TextInputEditText toInput, subjectInput, bodyInput;
    private AccountRepository accountRepository;
    private final Executor executor = Executors.newSingleThreadExecutor();
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_compose);
        
        accountRepository = new AccountRepository(this);
        
        MaterialToolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        toolbar.setNavigationOnClickListener(v -> finish());
        
        toInput = findViewById(R.id.toInput);
        subjectInput = findViewById(R.id.subjectInput);
        bodyInput = findViewById(R.id.bodyInput);
        
        String to = getIntent().getStringExtra("to");
        String subject = getIntent().getStringExtra("subject");
        if (to != null) toInput.setText(to);
        if (subject != null) subjectInput.setText(subject);
    }
    
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.compose_menu, menu);
        return true;
    }
    
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        if (item.getItemId() == R.id.action_send) {
            sendEmail();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
    
    private void sendEmail() {
        String to = toInput.getText().toString().trim();
        String subject = subjectInput.getText().toString().trim();
        String body = bodyInput.getText().toString().trim();
        
        if (to.isEmpty() || subject.isEmpty()) {
            Toast.makeText(this, "请填写收件人和主题", Toast.LENGTH_SHORT).show();
            return;
        }
        
        Toast.makeText(this, "正在发送...", Toast.LENGTH_SHORT).show();
        
        accountRepository.getDefaultAccount(account -> {
            if (account == null) {
                runOnUiThread(() -> Toast.makeText(this, "未找到账户", Toast.LENGTH_SHORT).show());
                return;
            }
            
            executor.execute(() -> {
                try {
                    String password = CryptoUtil.decrypt(account.getEncryptedPassword());
                    SmtpClient client = new SmtpClient();
                    client.sendEmail(account.getSmtpServer(), account.getSmtpPort(),
                        account.getEmail(), password, to, subject, body);
                    
                    runOnUiThread(() -> {
                        Toast.makeText(this, "发送成功", Toast.LENGTH_SHORT).show();
                        finish();
                    });
                    
                } catch (Exception e) {
                    runOnUiThread(() -> 
                        Toast.makeText(this, "发送失败: " + e.getMessage(), Toast.LENGTH_SHORT).show()
                    );
                }
            });
        });
    }
}
