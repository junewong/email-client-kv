package com.example.mailclient;

import android.content.Intent;
import android.os.Bundle;
import android.view.MenuItem;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.drawerlayout.widget.DrawerLayout;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout;

import com.example.mailclient.data.mail.ImapClient;
import com.example.mailclient.data.model.Account;
import com.example.mailclient.data.model.Email;
import com.example.mailclient.data.repository.AccountRepository;
import com.example.mailclient.data.repository.EmailRepository;
import com.example.mailclient.ui.compose.ComposeActivity;
import com.example.mailclient.ui.maildetail.MailDetailActivity;
import com.example.mailclient.ui.maillist.MailListAdapter;
import com.example.mailclient.util.CryptoUtil;
import com.google.android.material.appbar.MaterialToolbar;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.navigation.NavigationView;

import java.util.List;
import java.util.concurrent.Executor;
import java.util.concurrent.Executors;

public class MainActivity extends AppCompatActivity {
    private DrawerLayout drawerLayout;
    private RecyclerView mailList;
    private SwipeRefreshLayout swipeRefresh;
    private MailListAdapter adapter;
    private AccountRepository accountRepository;
    private EmailRepository emailRepository;
    private final Executor executor = Executors.newSingleThreadExecutor();
    private String currentFolder = "INBOX";
    private boolean isLoading = false;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        accountRepository = new AccountRepository(this);
        emailRepository = new EmailRepository(this);
        
        MaterialToolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        toolbar.setNavigationOnClickListener(v -> drawerLayout.open());
        
        drawerLayout = findViewById(R.id.drawerLayout);
        mailList = findViewById(R.id.mailList);
        swipeRefresh = findViewById(R.id.swipeRefresh);
        FloatingActionButton composeFab = findViewById(R.id.composeFab);
        NavigationView navigationView = findViewById(R.id.navigationView);
        
        adapter = new MailListAdapter();
        mailList.setLayoutManager(new LinearLayoutManager(this));
        mailList.setAdapter(adapter);
        
        adapter.setOnItemClickListener(email -> {
            Intent intent = new Intent(this, MailDetailActivity.class);
            intent.putExtra("email_uid", email.getUid());
            startActivity(intent);
        });
        
        swipeRefresh.setOnRefreshListener(this::loadEmails);
        composeFab.setOnClickListener(v -> startActivity(new Intent(this, ComposeActivity.class)));
        
        navigationView.setNavigationItemSelectedListener(item -> {
            int id = item.getItemId();
            if (id == R.id.nav_inbox) currentFolder = "INBOX";
            else if (id == R.id.nav_sent) currentFolder = "Sent";
            else if (id == R.id.nav_drafts) currentFolder = "Drafts";
            else if (id == R.id.nav_trash) currentFolder = "Trash";
            
            if (getSupportActionBar() != null) {
                getSupportActionBar().setTitle(item.getTitle());
            }
            drawerLayout.close();
            loadEmailsFromDatabase();
            loadEmails();
            return true;
        });
        
        loadEmailsFromDatabase();
        loadEmails();
    }
    
    private void loadEmailsFromDatabase() {
        accountRepository.getDefaultAccount(account -> {
            if (account != null) {
                emailRepository.getEmails(account.getId(), currentFolder, 50, emails -> {
                    runOnUiThread(() -> {
                        if (emails != null && !emails.isEmpty()) {
                            adapter.setEmails(emails);
                        }
                    });
                });
            }
        });
    }
    
    private void loadEmails() {
        if (isLoading) {
            return;
        }
        
        isLoading = true;
        swipeRefresh.setRefreshing(true);
        
        accountRepository.getDefaultAccount(account -> {
            if (account == null) {
                runOnUiThread(() -> {
                    swipeRefresh.setRefreshing(false);
                    isLoading = false;
                    Toast.makeText(this, "未找到账户", Toast.LENGTH_SHORT).show();
                });
                return;
            }
            
            executor.execute(() -> {
                try {
                    String password = CryptoUtil.decrypt(account.getEncryptedPassword());
                    ImapClient client = new ImapClient();
                    client.connect(account.getImapServer(), account.getImapPort(),
                        account.getEmail(), password);
                    
                    List<Email> emails = client.fetchEmails(currentFolder, 50);
                    for (Email email : emails) {
                        email.setAccountId(account.getId());
                    }
                    
                    client.disconnect();
                    
                    emailRepository.saveEmails(emails, () -> {
                        runOnUiThread(() -> {
                            adapter.setEmails(emails);
                            swipeRefresh.setRefreshing(false);
                            isLoading = false;
                            Toast.makeText(this, "加载了 " + emails.size() + " 封邮件", Toast.LENGTH_SHORT).show();
                        });
                    });
                    
                } catch (Exception e) {
                    e.printStackTrace();
                    runOnUiThread(() -> {
                        swipeRefresh.setRefreshing(false);
                        isLoading = false;
                        Toast.makeText(this, "加载失败: " + e.getMessage(), Toast.LENGTH_LONG).show();
                    });
                }
            });
        });
    }
}
