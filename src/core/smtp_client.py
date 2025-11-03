import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path


class SMTPClient:
    def __init__(self):
        self.connection = None
    
    def connect(self, server, port, email_addr, password, use_ssl=True):
        """连接SMTP服务器"""
        if port == 465:
            self.connection = smtplib.SMTP_SSL(server, port)
        else:
            self.connection = smtplib.SMTP(server, port)
            if use_ssl:
                self.connection.starttls()
        
        self.connection.login(email_addr, password)
        return True
    
    def disconnect(self):
        """断开连接"""
        if self.connection:
            self.connection.quit()
            self.connection = None
    
    def send_email(self, from_addr, to_addrs, subject, body, attachments=None):
        """发送邮件"""
        if not self.connection:
            raise Exception("未连接到服务器")
        
        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = ', '.join(to_addrs) if isinstance(to_addrs, list) else to_addrs
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        if attachments:
            for filepath in attachments:
                self._attach_file(msg, filepath)
        
        self.connection.send_message(msg)
        return True
    
    def _attach_file(self, msg, filepath):
        """添加附件"""
        path = Path(filepath)
        if not path.exists():
            return
        
        with open(filepath, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
        
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={path.name}')
        msg.attach(part)
