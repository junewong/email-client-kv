package com.example.mailclient.data.database;

import android.content.Context;

import androidx.room.Database;
import androidx.room.Room;
import androidx.room.RoomDatabase;

import com.example.mailclient.data.model.Account;
import com.example.mailclient.data.model.Email;

@Database(entities = {Account.class, Email.class}, version = 1)
public abstract class AppDatabase extends RoomDatabase {
    private static AppDatabase instance;
    
    public abstract AccountDao accountDao();
    public abstract EmailDao emailDao();
    
    public static synchronized AppDatabase getInstance(Context context) {
        if (instance == null) {
            instance = Room.databaseBuilder(
                context.getApplicationContext(),
                AppDatabase.class,
                "mail_database"
            ).build();
        }
        return instance;
    }
}
