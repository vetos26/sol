"""A small, touch-friendly calculator built with Kivy."""
from kivy.config import Config

Config.set('graphics', 'width', '440')
Config.set('graphics', 'height', '760')
Config.set('graphics', 'minimum_width', '320')
Config.set('graphics', 'minimum_height', '540')

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Ellipse
from kivy.metrics import dp, sp
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from calculator import Calculator


BG = (0.055, 0.067, 0.105, 1)
SURFACE = (0.09, 0.105, 0.16, 1)
KEY = (0.14, 0.16, 0.22, 1)
UTILITY = (0.20, 0.22, 0.29, 1)
OPERATOR = (0.20, 0.23, 0.32, 1)
ACCENT = (0.75, 0.96, 0.47, 1)
TEXT = (0.95, 0.96, 0.98, 1)
MUTED = (0.53, 0.57, 0.66, 1)


class RoundedPanel(BoxLayout):
    def __init__(self, color=SURFACE, radius=24, **kwargs):
        super().__init__(**kwargs)
        self.panel_color = color
        self.radius = radius
        with self.canvas.before:
            Color(*color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(radius)])
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *_):
        self.rect.pos, self.rect.size = self.pos, self.size


class Key(ButtonBehavior, Label):
    def __init__(self, title, color=KEY, text_color=TEXT, action=None, **kwargs):
        super().__init__(text=title, color=text_color, font_size=sp(23), **kwargs)
        self.base_color = color
        self.action = action
        with self.canvas.before:
            self.bg_color = Color(*color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(20)])
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *_):
        self.rect.pos, self.rect.size = self.pos, self.size

    def on_press(self):
        r, g, b, a = self.base_color
        self.bg_color.rgba = (min(r * 1.2, 1), min(g * 1.2, 1), min(b * 1.2, 1), a)
        if self.action:
            self.action()

    def on_release(self):
        self.bg_color.rgba = self.base_color


def aligned_label(**kwargs):
    label = Label(**kwargs)
    label.bind(size=lambda instance, size: setattr(instance, 'text_size', size))
    return label


class CalculatorApp(App):
    def build(self):
        self.title = 'Калькулятор'
        self.calc = Calculator()
        Window.clearcolor = BG
        Window.bind(on_key_down=self.on_keyboard)

        root = FloatLayout()
        # Restrained decorative accents behind the main card.
        with root.canvas.before:
            Color(0.10, 0.13, 0.19, 1)
            self.glow = Ellipse()
        root.bind(size=self._position_glow, pos=self._position_glow)
        self._position_glow(root)

        self.card = RoundedPanel(orientation='vertical', padding=dp(22), spacing=dp(16),
                                 size_hint=(None, None), pos_hint={'center_x': .5, 'center_y': .5})
        root.add_widget(self.card)
        root.bind(size=self._resize_card)
        self._resize_card(root, root.size)

        header = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(12))
        mark = RoundedPanel(color=ACCENT, radius=12, size_hint=(None, None), size=(dp(38), dp(38)))
        mark.add_widget(Label(text='✳', color=BG, font_size=sp(23)))
        header.add_widget(mark)
        titles = BoxLayout(orientation='vertical', spacing=dp(1))
        titles.add_widget(aligned_label(text='CALCULATOR', color=TEXT, font_size=sp(13), bold=True,
                                        halign='left', valign='middle'))
        titles.add_widget(aligned_label(text='ПРОСТО СЧИТАЙ', color=MUTED, font_size=sp(9),
                                        halign='left', valign='middle'))
        header.add_widget(titles)
        header.add_widget(aligned_label(text='●  READY', color=ACCENT, font_size=sp(10),
                                        halign='right', valign='middle', size_hint_x=None, width=dp(80)))
        self.card.add_widget(header)

        display = BoxLayout(orientation='vertical', padding=[dp(4), dp(12), dp(4), dp(4)], spacing=dp(4),
                            size_hint_y=0.95)
        display.add_widget(aligned_label(text='ВАШИ ВЫЧИСЛЕНИЯ', color=MUTED, font_size=sp(10),
                                         halign='left', valign='top', size_hint_y=None, height=dp(24)))
        display.add_widget(Widget())
        self.history_label = aligned_label(text='', color=MUTED, font_size=sp(16),
                                           halign='right', valign='middle', size_hint_y=None, height=dp(30),
                                           shorten=True, shorten_from='left')
        display.add_widget(self.history_label)
        self.result_label = aligned_label(text='0', color=TEXT, font_size=sp(52),
                                          halign='right', valign='middle', size_hint_y=None, height=dp(70),
                                          shorten=True, shorten_from='left')
        display.add_widget(self.result_label)
        self.card.add_widget(display)

        keys = GridLayout(cols=4, spacing=dp(9), size_hint_y=2.4)
        rows = [
            [('AC', 'clear', UTILITY), ('+/−', 'sign', UTILITY), ('%', 'percent', UTILITY), ('÷', '/', OPERATOR)],
            [('7', '7', KEY), ('8', '8', KEY), ('9', '9', KEY), ('×', '*', OPERATOR)],
            [('4', '4', KEY), ('5', '5', KEY), ('6', '6', KEY), ('−', '-', OPERATOR)],
            [('1', '1', KEY), ('2', '2', KEY), ('3', '3', KEY), ('+', '+', OPERATOR)],
            [('0', '0', KEY), ('.', 'decimal', KEY), ('⌫', 'backspace', KEY), ('=', 'equals', ACCENT)],
        ]
        for row in rows:
            for title, command, color in row:
                keys.add_widget(Key(title, color=color, text_color=BG if command == 'equals' else TEXT,
                                    action=lambda cmd=command: self.handle(cmd)))
        self.card.add_widget(keys)
        footer = aligned_label(text='СДЕЛАНО ДЛЯ ВАШИХ ИДЕЙ  ✦', color=MUTED, font_size=sp(9),
                               halign='center', valign='middle', size_hint_y=None, height=dp(14))
        self.card.add_widget(footer)
        return root

    def _position_glow(self, root, *_):
        self.glow.pos = (root.center_x - dp(240), root.top - dp(360))
        self.glow.size = (dp(480), dp(480))

    def _resize_card(self, root, size):
        self.card.size = (min(size[0] - dp(24), dp(440)), min(size[1] - dp(24), dp(740)))

    def handle(self, command):
        if command in '0123456789' and len(command) == 1:
            self.calc.digit(command)
        elif command in ('+', '-', '*', '/'):
            self.calc.operation(command)
        else:
            getattr(self.calc, command)()
        self.history_label.text = self.calc.history
        self.result_label.text = self.calc.display
        length = len(self.calc.display)
        self.result_label.font_size = sp(52 if length <= 9 else 38 if length <= 13 else 28)

    def on_keyboard(self, window, key, scancode, codepoint, modifiers):
        codepoint = codepoint or ''
        mapping = {'+': '+', '-': '-', '*': '*', '/': '/', '.': 'decimal', ',': 'decimal',
                   '%': 'percent', '=': 'equals'}
        if codepoint in '0123456789' and len(codepoint) == 1:
            self.handle(codepoint)
        elif codepoint in mapping:
            self.handle(mapping[codepoint])
        elif key in (13, 271):
            self.handle('equals')
        elif key == 8:
            self.handle('backspace')
        elif key in (27, 127):
            self.handle('clear')
        else:
            return False
        return True

    def on_stop(self):
        Window.unbind(on_key_down=self.on_keyboard)


if __name__ == '__main__':
    CalculatorApp().run()
