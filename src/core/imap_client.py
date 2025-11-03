import imaplib
import email
from email.header import decode_header
from datetime import datetime


class IMAPClient:
    def __init__(self):
        self.connection = None
    
    def connect(self, server, port, email_addr, password, use_ssl=True):
        """连接IMAP服务器"""
        if use_ssl:
            self.connection = imaplib.IMAP4_SSL(server, port)
        else:
            self.connection = imaplib.IMAP4(server, port)
        
        self.connection.login(email_addr, password)
        return True
    
    def disconnect(self):
        """断开连接"""
        if self.connection:
            self.connection.logout()
            self.connection = None
    
    def fetch_folders(self):
        """获取文件夹列表"""
        if not self.connection:
            raise Exception("未连接到服务器")
        
        status, folders = self.connection.list()
        folder_list = []
        for folder in folders:
            folder_name = folder.decode().split('"')[-2]
            folder_list.append(folder_name)
        return folder_list
    
    def fetch_emails(self, folder='INBOX', limit=50):
        """获取邮件列表"""
        if not self.connection:
            raise Exception("未连接到服务器")
        
        self.connection.select(folder)
        status, messages = self.connection.search(None, 'ALL')
        
        email_ids = messages[0].split()
        email_ids = email_ids[-limit:]  # 获取最新的limit封
        email_ids.reverse()  # 最新的在前
        
        emails = []
        for email_id in email_ids:
            try:
                email_data = self._fetch_email_header(email_id)
                if email_data:
                    emails.append(email_data)
            except Exception as e:
                print(f"获取邮件 {email_id} 失败: {e}")
        
        return emails
    
    def _fetch_email_header(self, email_id):
        """获取邮件头信息"""
        status, msg_data = self.connection.fetch(email_id, '(RFC822.HEADER)')
        if status != 'OK':
            return None
        
        msg = email.message_from_bytes(msg_data[0][1])
        
        subject = self._decode_header(msg.get('Subject', ''))
        from_addr = self._decode_header(msg.get('From', ''))
        date_str = msg.get('Date', '')
        
        return {
            'id': email_id.decode(),
            'from': from_addr,
            'subject': subject,
            'date': date_str,
            'preview': subject[:100] if subject else '',
            'is_read': False
        }
    
    def _decode_header(self, header):
        """解码邮件头"""
        if not header:
            return ''
        
        decoded_parts = decode_header(header)
        result = []
        for content, encoding in decoded_parts:
            if isinstance(content, bytes):
                result.append(content.decode(encoding or 'utf-8', errors='ignore'))
            else:
                result.append(content)
        return ''.join(result)
    
    def get_email_content(self, email_id):
        """获取邮件完整内容"""
        if not self.connection:
            raise Exception("未连接到服务器")
        
        status, msg_data = self.connection.fetch(email_id.encode(), '(RFC822)')
        if status != 'OK':
            return None
        
        msg = email.message_from_bytes(msg_data[0][1])
        
        body = ''
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True).decode(errors='ignore')
                    break
        else:
            body = msg.get_payload(decode=True).decode(errors='ignore')
        
        return {
            'id': email_id,
            'from': self._decode_header(msg.get('From', '')),
            'to': self._decode_header(msg.get('To', '')),
            'subject': self._decode_header(msg.get('Subject', '')),
            'date': msg.get('Date', ''),
            'body': body
        }
