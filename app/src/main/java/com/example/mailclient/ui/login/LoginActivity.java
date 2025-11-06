package com.example.mailclient.ui.login;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.example.mailclient.MainActivity;
import com.example.mailclient.R;
import com.example.mailclient.data.mail.ImapClient;
import com.example.mailclient.data.model.Account;
import com.example.mailclient.data.repository.AccountRepository;
import com.example.mailclient.util.CryptoUtil;
import com.example.mailclient.util.MailProviders;
import com.google.android.material.textfield.TextInputEditText;

import java.util.concurrent.Executor;
import java.util.concurrent.Executors;

public class LoginActivity extends AppCompatActivity {
    private Spinner providerSpinner;
    private TextInputEditText emailInput, passwordInput;
    private Button loginButton;
    private TextView statusText;
    private AccountRepository accountRepository;
    private final Executor executor = Executors.newSingleThreadExecutor();
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        accountRepository = new AccountRepository(this);
        
        // 检查是否已有账户
        accountRepository.getDefaultAccount(account -> {
            if (account != null) {
                startActivity(new Intent(this, MainActivity.class));
                finish();
            }
        });
        
        setContentView(R.layout.activity_login);
        
        providerSpinner = findViewById(R.id.providerSpinner);
        emailInput = findViewById(R.id.emailInput);
        passwordInput = findViewById(R.id.passwordInput);
        loginButton = findViewById(R.id.loginButton);
        statusText = findViewById(R.id.statusText);
        
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this,
            android.R.layout.simple_spinner_item, MailProviders.getProviderNames());
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        providerSpinner.setAdapter(adapter);
        
        loginButton.setOnClickListener(v -> login());
    }
    
    private void login() {
        String email = emailInput.getText().toString().trim();
        String password = passwordInput.getText().toString().trim();
        String providerName = providerSpinner.getSelectedItem().toString();
        
        if (email.isEmpty() || password.isEmpty()) {
            statusText.setText("请填写完整信息");
            return;
        }
        
        loginButton.setEnabled(false);
        statusText.setText("正在连接...");
        
        executor.execute(() -> {
            try {
                MailProviders.Provider provider = MailProviders.getProvider(providerName);
                
                ImapClient client = new ImapClient();
                client.connect(provider.imapHost, provider.imapPort, email, password);
                client.disconnect();
                
                // 先删除所有旧账户
                accountRepository.deleteAllAccounts(() -> {
                    Account account = new Account();
                    account.setEmail(email);
                    account.setName(email.split("@")[0]);
                    account.setImapServer(provider.imapHost);
                    account.setImapPort(provider.imapPort);
                    account.setSmtpServer(provider.smtpHost);
                    account.setSmtpPort(provider.smtpPort);
                    account.setEncryptedPassword(CryptoUtil.encrypt(password));
                    account.setUseSsl(true);
                    account.setDefault(true);
                    
                    accountRepository.addAccount(account, id -> {
                        runOnUiThread(() -> {
                            startActivity(new Intent(this, MainActivity.class));
                            finish();
                        });
                    });
                });
                
            } catch (Exception e) {
                runOnUiThread(() -> {
                    statusText.setText("登录失败: " + e.getMessage());
                    loginButton.setEnabled(true);
                });
            }
        });
    }
}
