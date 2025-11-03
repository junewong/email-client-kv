from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from src.core.account import AccountManager
from src.core.imap_client import IMAPClient
import threading


class MailListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.account_manager = AccountManager()
        self.imap_client = None
        
        layout = BoxLayout(orientation='vertical')
        
        # 顶部工具栏
        toolbar = BoxLayout(size_hint_y=0.08, spacing=10, padding=10)
        refresh_btn = Button(text='刷新')
        refresh_btn.bind(on_press=self.refresh_emails)
        toolbar.add_widget(refresh_btn)
        
        compose_btn = Button(text='写邮件')
        compose_btn.bind(on_press=self.compose_email)
        toolbar.add_widget(compose_btn)
        
        logout_btn = Button(text='退出')
        logout_btn.bind(on_press=self.logout)
        toolbar.add_widget(logout_btn)
        
        layout.add_widget(toolbar)
        
        # 状态标签
        self.status_label = Label(text='', size_hint_y=0.05)
        layout.add_widget(self.status_label)
        
        # 邮件列表
        scroll = ScrollView()
        self.mail_list = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.mail_list.bind(minimum_height=self.mail_list.setter('height'))
        scroll.add_widget(self.mail_list)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
        self.emails_data = []
    
    def on_enter(self):
        """进入界面时加载邮件"""
        self.account_manager.load_accounts()
        self.refresh_emails()
    
    def refresh_emails(self, instance=None):
        """刷新邮件列表"""
        self.status_label.text = '正在加载邮件...'
        self.mail_list.clear_widgets()
        self.emails_data = []
        
        account = self.account_manager.get_default_account()
        if not account:
            self.status_label.text = '未找到账户'
            return
        
        threading.Thread(target=self._load_emails, args=(account,)).start()
    
    def _load_emails(self, account):
        """后台加载邮件"""
        try:
            password = self.account_manager.get_decrypted_password(account['id'])
            
            self.imap_client = IMAPClient()
            self.imap_client.connect(
                account['imap_server'],
                account['imap_port'],
                account['email'],
                password
            )
            
            emails = self.imap_client.fetch_emails(limit=20)
            self.emails_data = emails
            
            self.status_label.text = f'加载了 {len(emails)} 封邮件'
            
            for idx, email_data in enumerate(emails):
                self._add_mail_item(email_data, idx)
            
        except Exception as e:
            self.status_label.text = f'加载失败: {str(e)}'
    
    def _add_mail_item(self, email_data, index):
        """添加邮件项到列表"""
        item = BoxLayout(orientation='vertical', size_hint_y=None, height=100, padding=10)
        item.add_widget(Label(text=f"发件人: {email_data['from']}", size_hint_y=0.3, halign='left'))
        item.add_widget(Label(text=f"主题: {email_data['subject']}", size_hint_y=0.4, bold=True, halign='left'))
        item.add_widget(Label(text=f"时间: {email_data['date']}", size_hint_y=0.3, color=(0.5, 0.5, 0.5, 1), halign='left'))
        
        btn = Button(size_hint_y=None, height=100, background_color=(0, 0, 0, 0))
        btn.bind(on_press=lambda x, i=index: self.view_email(i))
        
        container = BoxLayout(size_hint_y=None, height=100)
        container.add_widget(item)
        container.add_widget(btn)
        
        self.mail_list.add_widget(container)
    
    def view_email(self, index):
        """查看邮件详情"""
        if index >= len(self.emails_data):
            return
        
        email_data = self.emails_data[index]
        
        self.status_label.text = '正在加载邮件内容...'
        threading.Thread(target=self._load_email_content, args=(email_data['id'],)).start()
    
    def _load_email_content(self, email_id):
        """加载邮件完整内容"""
        try:
            full_email = self.imap_client.get_email_content(email_id)
            
            detail_screen = self.manager.get_screen('maildetail')
            detail_screen.set_email(full_email, self.imap_client)
            self.manager.current = 'maildetail'
        except Exception as e:
            self.status_label.text = f'加载失败: {str(e)}'
    
    def compose_email(self, instance):
        """撰写新邮件"""
        self.manager.current = 'compose'
    
    def logout(self, instance):
        """退出登录"""
        if self.imap_client:
            self.imap_client.disconnect()
        self.manager.current = 'login'
