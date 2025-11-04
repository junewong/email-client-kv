package com.example.mailclient.data.database;

import androidx.room.Dao;
import androidx.room.Insert;
import androidx.room.OnConflictStrategy;
import androidx.room.Query;

import com.example.mailclient.data.model.Email;

import java.util.List;

@Dao
public interface EmailDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    void insert(Email email);
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    void insertAll(List<Email> emails);
    
    @Query("SELECT * FROM emails WHERE accountId = :accountId AND folder = :folder ORDER BY date DESC LIMIT :limit")
    List<Email> getEmails(long accountId, String folder, int limit);
    
    @Query("SELECT * FROM emails WHERE uid = :uid")
    Email getEmailByUid(String uid);
    
    @Query("DELETE FROM emails WHERE uid = :uid")
    void deleteEmail(String uid);
    
    @Query("DELETE FROM emails WHERE accountId = :accountId")
    void deleteAllByAccount(long accountId);
}
