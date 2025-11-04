package com.example.mailclient.util;

import android.util.Base64;

public class CryptoUtil {
    
    public static String encrypt(String plaintext) {
        // 简单的Base64编码（生产环境应使用Android Keystore + AES）
        return Base64.encodeToString(plaintext.getBytes(), Base64.DEFAULT);
    }
    
    public static String decrypt(String encrypted) {
        return new String(Base64.decode(encrypted, Base64.DEFAULT));
    }
}
