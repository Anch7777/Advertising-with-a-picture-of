from ursina import *
import math
import time

# Настройки игры
app = Ursina()

# Параметры игры
PLAYER_SPEED = 5
GEISHA_SPEED = 3
GEISHA_VISION_RANGE = 5
EXIT_DOOR_DISTANCE = 1.5
GEISHA_ACTIVATION_DISTANCE = 8
PLAYER_MAX_HEALTH = 100

# Карта
mini_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 2, 2, 2, 2, 2, 0, 3, 3, 3, 3, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, "G", 0, 0, 0, 0, 0, 0, 0, 0, 1],  # Гейша здесь
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 4, 4, 4, 3, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1],  # Выход
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Создание карты
def create_map():
    for z, row in enumerate(mini_map):
        for x, cell in enumerate(row):
            if cell == 1:  # Стена
                Entity(model='cube', texture='wall_1.png', position=(x, 0, z), scale=(1, 2, 1), collider='box')
            elif cell == 5:  # Выход
                Entity(model='cube', texture='exit_door.png', position=(x, 0, z), scale=(1, 2, 1), collider='box')
            elif cell == "G":  # Гейша
                geisha.position = (x, 0, z)

# Игрок
player = Entity(model='cube', color=color.orange, position=(1, 0, 1), collider='box')
camera.parent = player
camera.position = (0, 1.5, 0)
camera.rotation_x = -30

# Здоровье игрока
player_health = PLAYER_MAX_HEALTH
health_bar = Text(text=f"Health: {player_health}", position=(-0.85, 0.45), origin=(0, 0), scale=2, color=color.red)

# Гейша
geisha = Entity(model='cube', texture='geisha.png', position=(6, 0, 4), collider='box', scale=(1, 2, 1))
geisha_active = True
last_seen_time = 0

# Выход
exit_door = Entity(model='cube', texture='exit_door.png', position=(8, 0, 8), collider='box')

# Обновление игры
def update():
    global player_health, geisha_active, last_seen_time

    # Управление игроком
    if held_keys['w']: player.position += player.forward * PLAYER_SPEED * time.dt
    if held_keys['s']: player.position -= player.forward * PLAYER_SPEED * time.dt
    if held_keys['a']: player.position -= player.right * PLAYER_SPEED * time.dt
    if held_keys['d']: player.position += player.right * PLAYER_SPEED * time.dt

    # Проверка коллизий игрока
    for wall in scene.entities:
        if wall.collider and wall.intersects(player).hit:
            player.position -= player.forward * PLAYER_SPEED * time.dt

    # Логика гейши
    if geisha_active:
        distance_to_player = distance(geisha, player)
        if distance_to_player <= GEISHA_VISION_RANGE:
            geisha.look_at(player)
            geisha.position += geisha.forward * GEISHA_SPEED * time.dt
            last_seen_time = time.time()
        else:
            if time.time() - last_seen_time > 10:
                geisha_active = False
                geisha.visible = False

        # Проверка столкновения с игроком
        if geisha.intersects(player).hit:
            player_health -= 1
            health_bar.text = f"Health: {player_health}"
            if player_health <= 0:
                print("Игра окончена!")
                application.quit()

    # Проверка коллизий гейши
    for wall in scene.entities:
        if wall.collider and wall.intersects(geisha).hit:
            geisha.position -= geisha.forward * GEISHA_SPEED * time.dt

    # Проверка выхода
    if player.intersects(exit_door).hit:
        Text(text="Press E to exit", position=(0, 0.4), origin=(0, 0), scale=2, color=color.white)
        if held_keys['e']:
            print("Выход из игры!")
            application.quit()

# Создание карты
create_map()

# Запуск игры
app.run()