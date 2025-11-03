"""邮箱服务商配置"""

MAIL_PROVIDERS = {
    "QQ邮箱": {
        "domain": "qq.com",
        "imap": ("imap.qq.com", 993),
        "smtp": ("smtp.qq.com", 465),
        "note": "需要开启IMAP/SMTP服务并使用授权码"
    },
    "163邮箱": {
        "domain": "163.com",
        "imap": ("imap.163.com", 993),
        "smtp": ("smtp.163.com", 465),
        "note": "需要开启IMAP/SMTP服务并使用授权码"
    },
    "126邮箱": {
        "domain": "126.com",
        "imap": ("imap.126.com", 993),
        "smtp": ("smtp.126.com", 465),
        "note": "需要开启IMAP/SMTP服务并使用授权码"
    },
    "Gmail": {
        "domain": "gmail.com",
        "imap": ("imap.gmail.com", 993),
        "smtp": ("smtp.gmail.com", 587),
        "note": "需要开启应用专用密码"
    },
    "Outlook": {
        "domain": "outlook.com",
        "imap": ("outlook.office365.com", 993),
        "smtp": ("smtp.office365.com", 587),
        "note": "支持直接登录"
    }
}
