from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.core.window import Window
import os
from kivy.uix.image import Image
from kivy.uix.label import Label

from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.behaviors import HoverBehavior



class HoverButton(MDFillRoundFlatButton, HoverBehavior):
    def on_enter(self, *args):
        self.md_bg_color = self.hover_bg

    def on_leave(self, *args):
        self.md_bg_color = self.normal_bg

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hover_bg = (1, 0, 0, 1)
        self.normal_bg = (0, 0.5, 0, 1)


Builder.load_string('''
<SplashScreen>:
    canvas.before:
        Color:
            rgba: 0, 0, 0, 1
        Rectangle:
            pos: self.pos
            size: self.size

    FloatLayout:
        Image:
            id: logo
            source: 'car4cam.png'
            size_hint: 1.5, 1.5
            pos_hint: {'center_x': 0.5, 'center_y': 1.7}

<MainScreen>:
    RelativeLayout:
        id: layout

''')

class SplashScreen(Screen):
    def on_enter(self):
        anim_image = Animation(pos_hint={'center_y': 0.5}, duration=2)
        anim_image.start(self.ids.logo)
        self.screen_manager = self.manager

        # Schedule a transition to the next screen
        Clock.schedule_once(self.show_buttons, 5)

    def on_button_press(self, button, file_path):
       
        # Run the selected Python file
        os.system(f"python {file_path}")

    def show_buttons(self, dt):
        main_screen = MainScreen(name='main')
        self.manager.add_widget(main_screen)
        self.manager.current = 'main'

        # Add the logo to the top left corner
        logo = Image(source='car4cam.png', size_hint=(0.1, 1.5), size=(100, 100), pos=(0.5, 150))
        main_screen.add_widget(logo)
        # Add the logo text
        logo_text = Label(text="Intelli Drive System for Detecting Road Obstacles", font_size=45, font_name='Candara', color=(1, 1, 1, 1), size_hint=(None, None), size=logo.texture_size, pos_hint={'center_x': 0.5, 'center_y': 0.9})
        main_screen.add_widget(logo_text)

        # Add the first two buttons
        button1 = HoverButton(text='Road Lane', font_size=35, font_name='Candara',size_hint=(.2, .2), pos_hint={'x': .2, 'y': .4}, md_bg_color=(0, 0.5, 0, 1))
        button1.bind(on_press=lambda btn, f='road_lane_detection.py': self.on_button_press(btn, f))
        main_screen.add_widget(button1)

        button2 = HoverButton(text='Pothole', font_size=35, font_name='Candara',size_hint=(.2, .2), pos_hint={'x': .6, 'y': .4}, md_bg_color=(0, 0.5, 0, 1))
        button2.bind(on_press=lambda btn, f='pothole_detection.py': self.on_button_press(btn, f))
        main_screen.add_widget(button2)

        button3 = HoverButton(text='Obstacles', font_size=35,font_name='Candara',size_hint=(.2, .2), pos_hint={'x': .2, 'y': .1}, md_bg_color=(0, 0.5, 0, 1))
        button3.bind(on_press=lambda btn, f='object_detection.py': self.on_button_press(btn, f))
        main_screen.add_widget(button3)

        button4 = HoverButton(text='Parking Space', font_size=35, font_name='Candara',size_hint=(.2, .2), pos_hint={'x': .6, 'y': .1}, md_bg_color=(0, 0.5, 0, 1))
        button4.bind(on_press=lambda btn, f='parking_space.py': self.on_button_press(btn, f))
        main_screen.add_widget(button4)
        Window.clearcolor = (0, 0, 0, 1)
        return self.manager


class MainScreen(Screen):
    pass

class ScreenManagerApp(MDApp):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(SplashScreen(name='splash'))
        return screen_manager

ScreenManagerApp().run()


