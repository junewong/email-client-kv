import json
import uuid
from pathlib import Path
from kivy.app import App
from src.utils.crypto import encrypt_password, decrypt_password


class AccountManager:
    def __init__(self):
        self.config_file = None
        self.accounts = []
        self.default_account = None
    
    def _get_config_path(self):
        """获取配置文件路径"""
        if self.config_file:
            return self.config_file
        
        app = App.get_running_app()
        if app:
            data_dir = Path(app.user_data_dir)
        else:
            data_dir = Path.home() / '.mailclient'
        
        data_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = data_dir / 'accounts.json'
        return self.config_file
    
    def load_accounts(self):
        """加载账户配置"""
        config_path = self._get_config_path()
        if not config_path.exists():
            return
        
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.accounts = data.get('accounts', [])
            self.default_account = data.get('default_account')
    
    def save_accounts(self):
        """保存账户配置"""
        config_path = self._get_config_path()
        data = {
            'accounts': self.accounts,
            'default_account': self.default_account
        }
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_account(self, email, password, name, imap_server, imap_port, 
                    smtp_server, smtp_port, use_ssl=True):
        """添加账户"""
        account = {
            'id': str(uuid.uuid4()),
            'email': email,
            'name': name,
            'imap_server': imap_server,
            'imap_port': imap_port,
            'smtp_server': smtp_server,
            'smtp_port': smtp_port,
            'password': encrypt_password(password),
            'use_ssl': use_ssl
        }
        self.accounts.append(account)
        
        if not self.default_account:
            self.default_account = account['id']
        
        self.save_accounts()
        return account
    
    def get_account(self, account_id):
        """获取账户"""
        for account in self.accounts:
            if account['id'] == account_id:
                return account
        return None
    
    def get_default_account(self):
        """获取默认账户"""
        if self.default_account:
            return self.get_account(self.default_account)
        return None
    
    def get_decrypted_password(self, account_id):
        """获取解密后的密码"""
        account = self.get_account(account_id)
        if account:
            return decrypt_password(account['password'])
        return None
