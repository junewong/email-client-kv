package com.example.mailclient.data.database;

import androidx.room.Dao;
import androidx.room.Insert;
import androidx.room.Query;
import androidx.room.Update;

import com.example.mailclient.data.model.Account;

import java.util.List;

@Dao
public interface AccountDao {
    @Insert
    long insert(Account account);
    
    @Update
    void update(Account account);
    
    @Query("SELECT * FROM accounts")
    List<Account> getAllAccounts();
    
    @Query("SELECT * FROM accounts WHERE isDefault = 1 LIMIT 1")
    Account getDefaultAccount();
    
    @Query("SELECT * FROM accounts WHERE id = :id")
    Account getAccountById(long id);
    
    @Query("DELETE FROM accounts WHERE id = :id")
    void deleteAccount(long id);
    
    @Query("DELETE FROM accounts")
    void deleteAll();
}
