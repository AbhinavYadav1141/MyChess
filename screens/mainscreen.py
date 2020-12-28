from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput


class MainScreen(Screen):

    def new_offline(self, btn):
        self.manager.new_game()

    def start_online(self, btn, btn2):
        self.go(btn)
        '''
        btn.parent.remove_widget(btn2)
        btn.parent.add_widget(Label(text="Enter Code"))
        tin = TextInput()
        btn.parent.add_widget(tin)
        btn.parent.add_widget(Button(text="Go", on_press=self.go))
        btn.parent.remove_widget(btn)'''

    def go(self, btn):
        Popup(size_hint=(None, None), size=(Window.width/2, Window.height/2),
              content=Label(text="Will be available soon!!"), title="Coming Soon!").open()


class MainScreenApp(App):

    def build(self):
        return MainScreen()


if __name__ == '__main__':
    Builder.load_file("mainscreen.kv")
    app = MainScreenApp()
    app.run()
else:
    Builder.load_file("screens/mainscreen.kv")