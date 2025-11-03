from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from src.core.account import AccountManager
from src.core.smtp_client import SMTPClient
import threading


class ComposeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.account_manager = AccountManager()
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 顶部工具栏
        toolbar = BoxLayout(size_hint_y=0.08, spacing=10)
        back_btn = Button(text='返回')
        back_btn.bind(on_press=self.go_back)
        toolbar.add_widget(back_btn)
        
        send_btn = Button(text='发送')
        send_btn.bind(on_press=self.send_email)
        toolbar.add_widget(send_btn)
        
        layout.add_widget(toolbar)
        
        # 收件人
        self.to_input = TextInput(hint_text='收件人（多个用逗号分隔）', multiline=False, size_hint_y=0.08)
        layout.add_widget(self.to_input)
        
        # 主题
        self.subject_input = TextInput(hint_text='主题', multiline=False, size_hint_y=0.08)
        layout.add_widget(self.subject_input)
        
        # 正文
        self.body_input = TextInput(hint_text='正文')
        layout.add_widget(self.body_input)
        
        # 状态
        self.status_label = Label(text='', size_hint_y=0.08)
        layout.add_widget(self.status_label)
        
        self.add_widget(layout)
    
    def send_email(self, instance):
        """发送邮件"""
        to = self.to_input.text.strip()
        subject = self.subject_input.text.strip()
        body = self.body_input.text.strip()
        
        if not to or not subject:
            self.status_label.text = '请填写收件人和主题'
            return
        
        to_addrs = [addr.strip() for addr in to.split(',')]
        
        self.status_label.text = '正在发送...'
        threading.Thread(target=self._send_email, args=(to_addrs, subject, body)).start()
    
    def _send_email(self, to_addrs, subject, body):
        """后台发送邮件"""
        try:
            self.account_manager.load_accounts()
            account = self.account_manager.get_default_account()
            if not account:
                self.status_label.text = '未找到账户'
                return
            
            password = self.account_manager.get_decrypted_password(account['id'])
            
            client = SMTPClient()
            client.connect(
                account['smtp_server'],
                account['smtp_port'],
                account['email'],
                password
            )
            
            client.send_email(account['email'], to_addrs, subject, body)
            client.disconnect()
            
            self.status_label.text = '发送成功！'
            self.clear_form()
        except Exception as e:
            self.status_label.text = f'发送失败: {str(e)}'
    
    def clear_form(self):
        """清空表单"""
        self.to_input.text = ''
        self.subject_input.text = ''
        self.body_input.text = ''
    
    def go_back(self, instance):
        """返回邮件列表"""
        self.manager.current = 'maillist'
