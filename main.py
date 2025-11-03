from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from src.ui.login import LoginScreen
from src.ui.maillist import MailListScreen
from src.ui.compose import ComposeScreen
from src.ui.maildetail import MailDetailScreen


class MailClientApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MailListScreen(name='maillist'))
        sm.add_widget(ComposeScreen(name='compose'))
        sm.add_widget(MailDetailScreen(name='maildetail'))
        return sm


if __name__ == '__main__':
    MailClientApp().run()
