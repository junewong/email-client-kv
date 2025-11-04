package com.example.mailclient.data.repository;

import android.content.Context;

import com.example.mailclient.data.database.AppDatabase;
import com.example.mailclient.data.model.Account;

import java.util.List;
import java.util.concurrent.Executor;
import java.util.concurrent.Executors;

public class AccountRepository {
    private final AppDatabase database;
    private final Executor executor = Executors.newSingleThreadExecutor();
    
    public AccountRepository(Context context) {
        this.database = AppDatabase.getInstance(context);
    }
    
    public void addAccount(Account account, Callback<Long> callback) {
        executor.execute(() -> {
            long id = database.accountDao().insert(account);
            callback.onResult(id);
        });
    }
    
    public void getDefaultAccount(Callback<Account> callback) {
        executor.execute(() -> {
            Account account = database.accountDao().getDefaultAccount();
            callback.onResult(account);
        });
    }
    
    public void getAllAccounts(Callback<List<Account>> callback) {
        executor.execute(() -> {
            List<Account> accounts = database.accountDao().getAllAccounts();
            callback.onResult(accounts);
        });
    }
    
    public interface Callback<T> {
        void onResult(T result);
    }
}
