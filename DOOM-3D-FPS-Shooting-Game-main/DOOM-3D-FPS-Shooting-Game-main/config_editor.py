import configparser
import os
import tkinter as tk
from tkinter import ttk

class ConfigEditorApp:
    def __init__(self, root: tk.Tk) -> None:
        os.chdir(os.path.dirname(__file__))
        self.config = configparser.ConfigParser(allow_no_value=True)
        self.config.optionxform = str  # Сохраняем регистр ключей
        self.config.read("config.ini")
        if 'OPTIONS' not in self.config:
            self.config['OPTIONS'] = {}
        self.config_options = self.config['OPTIONS']

        self.window = tk.Toplevel(root)
        self.window.title("PyMaze Config")
        self.window.iconbitmap(os.path.join("window_icons", "config.ico"))

        # Пример слайдера для изменения разрешения экрана
        self.viewport_width_label = tk.Label(self.window, text="Ширина экрана")
        self.viewport_width_label.pack()
        self.viewport_width_slider = ttk.Scale(
            self.window, from_=500, to=3840,
            value=self.parse_int('VIEWPORT_WIDTH', 1280),
            command=lambda x: self.update_config('VIEWPORT_WIDTH', int(float(x)))
        )
        self.viewport_width_slider.pack()

        # Кнопка сохранения
        self.save_button = tk.Button(self.window, text="Сохранить", command=self.save_config)
        self.save_button.pack()

    def parse_int(self, key: str, default: int) -> int:
        return int(self.config_options.get(key, default))

    def update_config(self, key: str, value: int) -> None:
        self.config_options[key] = str(value)

    def save_config(self) -> None:
        with open("config.ini", "w") as config_file:
            self.config.write(config_file)
        self.window.destroy()