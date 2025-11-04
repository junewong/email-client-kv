package com.example.mailclient.data.repository;

import android.content.Context;

import com.example.mailclient.data.database.AppDatabase;
import com.example.mailclient.data.model.Email;

import java.util.List;
import java.util.concurrent.Executor;
import java.util.concurrent.Executors;

public class EmailRepository {
    private final AppDatabase database;
    private final Executor executor = Executors.newSingleThreadExecutor();
    
    public EmailRepository(Context context) {
        this.database = AppDatabase.getInstance(context);
    }
    
    public void saveEmails(List<Email> emails, Runnable onComplete) {
        executor.execute(() -> {
            database.emailDao().insertAll(emails);
            if (onComplete != null) onComplete.run();
        });
    }
    
    public void getEmails(long accountId, String folder, int limit, Callback<List<Email>> callback) {
        executor.execute(() -> {
            List<Email> emails = database.emailDao().getEmails(accountId, folder, limit);
            callback.onResult(emails);
        });
    }
    
    public void getEmailByUid(String uid, Callback<Email> callback) {
        executor.execute(() -> {
            Email email = database.emailDao().getEmailByUid(uid);
            callback.onResult(email);
        });
    }
    
    public interface Callback<T> {
        void onResult(T result);
    }
}
