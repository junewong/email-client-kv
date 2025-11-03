from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from src.core.imap_client import IMAPClient


class MailDetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.email_data = None
        self.imap_client = None
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 顶部工具栏
        toolbar = BoxLayout(size_hint_y=0.08, spacing=10)
        back_btn = Button(text='返回')
        back_btn.bind(on_press=self.go_back)
        toolbar.add_widget(back_btn)
        
        reply_btn = Button(text='回复')
        reply_btn.bind(on_press=self.reply_email)
        toolbar.add_widget(reply_btn)
        
        layout.add_widget(toolbar)
        
        # 邮件信息
        info_layout = BoxLayout(orientation='vertical', size_hint_y=0.3, spacing=5)
        self.from_label = Label(text='', size_hint_y=None, height=30)
        self.subject_label = Label(text='', size_hint_y=None, height=30, bold=True)
        self.date_label = Label(text='', size_hint_y=None, height=30)
        
        info_layout.add_widget(self.from_label)
        info_layout.add_widget(self.subject_label)
        info_layout.add_widget(self.date_label)
        layout.add_widget(info_layout)
        
        # 邮件正文
        scroll = ScrollView()
        self.body_label = Label(text='', size_hint_y=None, text_size=(None, None))
        self.body_label.bind(texture_size=self.body_label.setter('size'))
        scroll.add_widget(self.body_label)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def set_email(self, email_data, imap_client):
        """设置邮件数据"""
        self.email_data = email_data
        self.imap_client = imap_client
        
        self.from_label.text = f"发件人: {email_data.get('from', '')}"
        self.subject_label.text = f"主题: {email_data.get('subject', '')}"
        self.date_label.text = f"时间: {email_data.get('date', '')}"
        self.body_label.text = email_data.get('body', '')
    
    def reply_email(self, instance):
        """回复邮件"""
        if not self.email_data:
            return
        
        compose_screen = self.manager.get_screen('compose')
        compose_screen.to_input.text = self.email_data.get('from', '')
        compose_screen.subject_input.text = f"Re: {self.email_data.get('subject', '')}"
        self.manager.current = 'compose'
    
    def go_back(self, instance):
        """返回邮件列表"""
        self.manager.current = 'maillist'
