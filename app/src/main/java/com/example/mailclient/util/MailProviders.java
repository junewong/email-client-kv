package com.example.mailclient.util;

import java.util.HashMap;
import java.util.Map;

public class MailProviders {
    
    public static class Provider {
        public String name;
        public String imapHost;
        public int imapPort;
        public String smtpHost;
        public int smtpPort;
        
        public Provider(String name, String imapHost, int imapPort, String smtpHost, int smtpPort) {
            this.name = name;
            this.imapHost = imapHost;
            this.imapPort = imapPort;
            this.smtpHost = smtpHost;
            this.smtpPort = smtpPort;
        }
    }
    
    private static final Map<String, Provider> providers = new HashMap<>();
    
    static {
        providers.put("QQ邮箱", new Provider("QQ邮箱", "imap.qq.com", 993, "smtp.qq.com", 465));
        providers.put("163邮箱", new Provider("163邮箱", "imap.163.com", 993, "smtp.163.com", 465));
        providers.put("126邮箱", new Provider("126邮箱", "imap.126.com", 993, "smtp.126.com", 465));
        providers.put("Gmail", new Provider("Gmail", "imap.gmail.com", 993, "smtp.gmail.com", 587));
        providers.put("Outlook", new Provider("Outlook", "outlook.office365.com", 993, "smtp.office365.com", 587));
    }
    
    public static String[] getProviderNames() {
        return providers.keySet().toArray(new String[0]);
    }
    
    public static Provider getProvider(String name) {
        return providers.get(name);
    }
}
