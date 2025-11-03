import sqlite3
from pathlib import Path
from kivy.app import App
from datetime import datetime


class EmailStorage:
    def __init__(self):
        self.db_path = None
        self.conn = None
    
    def _get_db_path(self):
        """获取数据库路径"""
        if self.db_path:
            return self.db_path
        
        app = App.get_running_app()
        if app:
            data_dir = Path(app.user_data_dir)
        else:
            data_dir = Path.home() / '.mailclient'
        
        data_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = data_dir / 'emails.db'
        return self.db_path
    
    def connect(self):
        """连接数据库"""
        db_path = self._get_db_path()
        self.conn = sqlite3.connect(str(db_path))
        self._create_tables()
    
    def _create_tables(self):
        """创建表"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emails (
                id TEXT PRIMARY KEY,
                account_id TEXT,
                folder TEXT,
                sender TEXT,
                recipients TEXT,
                subject TEXT,
                date DATETIME,
                body_preview TEXT,
                has_attachment INTEGER,
                is_read INTEGER,
                size INTEGER,
                cached_at DATETIME
            )
        ''')
        
        self.conn.commit()
    
    def save_email(self, email_data, account_id, folder='INBOX'):
        """保存邮件"""
        if not self.conn:
            self.connect()
        
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO emails 
            (id, account_id, folder, sender, subject, date, body_preview, is_read, cached_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            email_data['id'],
            account_id,
            folder,
            email_data.get('from', ''),
            email_data.get('subject', ''),
            email_data.get('date', ''),
            email_data.get('preview', ''),
            0,
            datetime.now().isoformat()
        ))
        
        self.conn.commit()
    
    def get_emails(self, account_id, folder='INBOX', limit=50):
        """获取邮件列表"""
        if not self.conn:
            self.connect()
        
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, sender, subject, date, body_preview, is_read
            FROM emails
            WHERE account_id = ? AND folder = ?
            ORDER BY date DESC
            LIMIT ?
        ''', (account_id, folder, limit))
        
        emails = []
        for row in cursor.fetchall():
            emails.append({
                'id': row[0],
                'from': row[1],
                'subject': row[2],
                'date': row[3],
                'preview': row[4],
                'is_read': bool(row[5])
            })
        
        return emails
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()
            self.conn = None
