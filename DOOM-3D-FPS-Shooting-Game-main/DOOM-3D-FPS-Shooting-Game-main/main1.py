import os
import sys
import tkinter.messagebox
import tkinter.simpledialog
from typing import Any, Dict
import pygame
from config_editor import ConfigEditorApp
from level_designer import LevelDesignerApp
from maze_game import maze_game
from screen_drawing import BLUE, GREEN, WHITE
from server import maze_server

def main() -> None:
    """
    Главная функция, предоставляющая пользователю выбор между запуском игры,
    редактора настроек или конструктора уровней.
    """
    # Изменение рабочей директории на директорию скрипта
    os.chdir(os.path.dirname(__file__))
    pygame.init()

    # Создание скрытого корневого окна Tkinter
    root = tkinter.Tk()
    root.withdraw()

    # Минимальное разрешение окна 500×500
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("PyMaze")
    pygame.display.set_icon(
        pygame.image.load(os.path.join("window_icons", "main.png")).convert()
    )

    normal_font = pygame.font.SysFont('Tahoma', 14, True)
    button_font = pygame.font.SysFont('Tahoma', 28, True)
    title_font = pygame.font.SysFont('Tahoma', 36, True)

    title_text = title_font.render("PyMaze", True, BLUE)
    copyright_text = normal_font.render(
        "Copyright © 2022 Ptolemy Hill, Finlay Griffiths, and Tomas Reynolds",
        True, BLUE
    )
    play_text = button_font.render("Play", True, WHITE)
    config_text = button_font.render("Settings", True, WHITE)
    design_text = button_font.render("Designer", True, WHITE)

    button_width = max(x.get_width() for x in (play_text, config_text, design_text)) + 10

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_pos = pygame.mouse.get_pos()

                # Кнопка "Play"
                if 108 <= clicked_pos[1] <= 158:
                    maze_game()

                # Кнопка "Settings"
                elif 224 <= clicked_pos[1] <= 274:
                    _root = tkinter.Tk()
                    _root.withdraw()
                    ConfigEditorApp(_root)

                # Кнопка "Designer"
                elif 340 <= clicked_pos[1] <= 390:
                    _root = tkinter.Tk()
                    _root.withdraw()
                    LevelDesignerApp(_root)

        screen.fill(GREEN)
        screen.blit(title_text, (250 - title_text.get_width() // 2, 5))
        screen.blit(copyright_text, (250 - copyright_text.get_width() // 2, 475))

        pygame.draw.rect(screen, BLUE, (250 - button_width // 2, 108, button_width, 50))
        pygame.draw.rect(screen, BLUE, (250 - button_width // 2, 224, button_width, 50))
        pygame.draw.rect(screen, BLUE, (250 - button_width // 2, 340, button_width, 50))

        screen.blit(play_text, (250 - play_text.get_width() // 2, 113))
        screen.blit(config_text, (250 - config_text.get_width() // 2, 229))
        screen.blit(design_text, (250 - design_text.get_width() // 2, 345))

        pygame.display.update()

if __name__ == "__main__":
    main()