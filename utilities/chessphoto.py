from kivy.base import runTouchApp
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder

Builder.load_string("""
<Button1>:
    canvas.after:
        Color:
            rgb: self.colors
        Rectangle:
            pos: root.pos
            size: root.size

""")


Window.size = (700, 700)


class Dummy:
    colors = (0, 0, 0, 0)

    def __init__(self, colors):
        self.colors = colors


class Button1(Button, Dummy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


layout = GridLayout(cols=8)
for i in range(8):
    for j in range(8):
        clr = (i + j + 1) % 2
        btn = Button1(colors=(clr, clr, clr))
        layout.add_widget(btn)

runTouchApp(layout)
