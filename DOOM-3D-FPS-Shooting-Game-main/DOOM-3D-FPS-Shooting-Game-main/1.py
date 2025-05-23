import pygame

try:
    n = input()
    if int(n) != float(n):
        raise ValueError

    n = int(n)
    pygame.init()
    size = width, height = 300, 300
    screen = pygame.display.set_mode((width, height))
    screen.fill("yellow")
    s = n // 2
    color = pygame.Color("orange")
    for i in range(0, 300, s * 2):
        for j in range(0, 300, s * 2):
            if i + s * 2 > width or j + s * 2 > height:
                continue

            points = [(i, j + s), (i + s, j), (i + s * 2, j + s), (i + s, j + s * 2)]
            pygame.draw.polygon(screen, color, points)

    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass

    pygame.quit()
except ValueError:
    print("Неправильный формат ввода")