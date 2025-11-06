package com.example.mailclient.data.mail;

import android.util.Log;

import com.example.mailclient.data.model.Email;

import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

import javax.mail.Folder;
import javax.mail.Message;
import javax.mail.Session;
import javax.mail.Store;
import javax.mail.internet.InternetAddress;

public class ImapClient {
    private static final String TAG = "ImapClient";
    private Store store;
    
    public void connect(String host, int port, String email, String password) throws Exception {
        Log.d(TAG, "连接到: " + host + ":" + port + " 用户: " + email);
        Properties props = new Properties();
        props.put("mail.store.protocol", "imaps");
        props.put("mail.imaps.host", host);
        props.put("mail.imaps.port", String.valueOf(port));
        props.put("mail.imaps.ssl.enable", "true");
        props.put("mail.imaps.ssl.trust", "*");
        props.put("mail.imaps.timeout", "10000");
        props.put("mail.imaps.connectiontimeout", "10000");
        props.put("mail.imaps.auth.login.disable", "false");
        props.put("mail.imaps.auth.plain.disable", "false");
        props.put("mail.debug", "false");
        
        Session session = Session.getInstance(props);
        store = session.getStore("imaps");
        store.connect(host, email, password);
        Log.d(TAG, "连接成功");
    }
    
    public List<Email> fetchEmails(String folderName, int limit) throws Exception {
        Folder folder = store.getFolder(folderName);
        folder.open(Folder.READ_WRITE);
        
        Message[] messages = folder.getMessages();
        List<Email> emails = new ArrayList<>();
        
        int start = Math.max(1, messages.length - limit + 1);
        for (int i = messages.length; i >= start; i--) {
            Message msg = messages[i - 1];
            Email email = new Email();
            email.setUid(String.valueOf(msg.getMessageNumber()));
            email.setFrom(getAddress(msg.getFrom()));
            email.setTo(getAddress(msg.getAllRecipients()));
            email.setSubject(msg.getSubject() != null ? msg.getSubject() : "(无主题)");
            email.setDate(msg.getSentDate() != null ? msg.getSentDate().getTime() : System.currentTimeMillis());
            email.setFolder(folderName);
            emails.add(email);
        }
        
        folder.close(false);
        return emails;
    }
    
    public String getEmailBody(String folderName, String uid) throws Exception {
        Folder folder = store.getFolder(folderName);
        folder.open(Folder.READ_WRITE);
        
        Message msg = folder.getMessage(Integer.parseInt(uid));
        String body = "";
        
        if (msg.isMimeType("text/plain")) {
            body = msg.getContent().toString();
        } else if (msg.isMimeType("multipart/*")) {
            body = "(暂不支持复杂格式)";
        }
        
        folder.close(false);
        return body;
    }
    
    public void disconnect() throws Exception {
        if (store != null && store.isConnected()) {
            store.close();
        }
    }
    
    private String getAddress(javax.mail.Address[] addresses) {
        if (addresses == null || addresses.length == 0) return "";
        return ((InternetAddress) addresses[0]).getAddress();
    }
}
