from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from src.core.account import AccountManager
from src.core.imap_client import IMAPClient
from src.utils.config import MAIL_PROVIDERS
import threading


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.account_manager = AccountManager()
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        layout.add_widget(Label(text='邮件客户端', font_size=24, size_hint_y=0.2))
        
        self.provider_spinner = Spinner(
            text='选择邮箱服务商',
            values=list(MAIL_PROVIDERS.keys()),
            size_hint_y=None,
            height=44
        )
        self.provider_spinner.bind(text=self.on_provider_select)
        layout.add_widget(self.provider_spinner)
        
        self.email_input = TextInput(hint_text='邮箱地址', multiline=False, size_hint_y=None, height=44)
        layout.add_widget(self.email_input)
        
        self.password_input = TextInput(hint_text='密码/授权码', password=True, multiline=False, size_hint_y=None, height=44)
        layout.add_widget(self.password_input)
        
        self.imap_input = TextInput(hint_text='IMAP服务器', multiline=False, size_hint_y=None, height=44)
        layout.add_widget(self.imap_input)
        
        self.smtp_input = TextInput(hint_text='SMTP服务器', multiline=False, size_hint_y=None, height=44)
        layout.add_widget(self.smtp_input)
        
        self.status_label = Label(text='', size_hint_y=0.1)
        layout.add_widget(self.status_label)
        
        login_btn = Button(text='登录', size_hint_y=None, height=50)
        login_btn.bind(on_press=self.do_login)
        layout.add_widget(login_btn)
        
        self.add_widget(layout)
    
    def on_provider_select(self, spinner, text):
        """选择邮箱服务商时自动填充配置"""
        if text in MAIL_PROVIDERS:
            provider = MAIL_PROVIDERS[text]
            self.imap_input.text = f"{provider['imap'][0]}:{provider['imap'][1]}"
            self.smtp_input.text = f"{provider['smtp'][0]}:{provider['smtp'][1]}"
    
    def do_login(self, instance):
        """执行登录"""
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()
        imap_config = self.imap_input.text.strip()
        smtp_config = self.smtp_input.text.strip()
        
        if not all([email, password, imap_config, smtp_config]):
            self.show_error('请填写完整信息')
            return
        
        try:
            imap_server, imap_port = imap_config.split(':')
            smtp_server, smtp_port = smtp_config.split(':')
            imap_port = int(imap_port)
            smtp_port = int(smtp_port)
        except:
            self.show_error('服务器配置格式错误')
            return
        
        self.status_label.text = '正在连接...'
        
        # 在后台线程测试连接
        threading.Thread(target=self._test_connection, args=(
            email, password, imap_server, imap_port, smtp_server, smtp_port
        )).start()
    
    def _test_connection(self, email, password, imap_server, imap_port, smtp_server, smtp_port):
        """测试IMAP连接"""
        try:
            client = IMAPClient()
            client.connect(imap_server, imap_port, email, password)
            client.disconnect()
            
            # 保存账户
            self.account_manager.add_account(
                email=email,
                password=password,
                name=email.split('@')[0],
                imap_server=imap_server,
                imap_port=imap_port,
                smtp_server=smtp_server,
                smtp_port=smtp_port
            )
            
            self.status_label.text = '登录成功！'
            self.manager.current = 'maillist'
        except Exception as e:
            self.status_label.text = f'登录失败: {str(e)}'
    
    def show_error(self, message):
        """显示错误提示"""
        self.status_label.text = message
