from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class MinimalApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        layout.add_widget(Label(
            text='Kivy Build Test\nGitHub Actions',
            font_size=24,
            halign='center'
        ))
        
        btn = Button(text='Click Me', size_hint_y=0.3)
        btn.bind(on_press=self.on_button_click)
        layout.add_widget(btn)
        
        self.status_label = Label(text='Ready', size_hint_y=0.2)
        layout.add_widget(self.status_label)
        
        return layout
    
    def on_button_click(self, instance):
        self.status_label.text = 'Button Clicked!'


if __name__ == '__main__':
    MinimalApp().run()

