import pygame
import sys
# import random

pygame.init()

# Размеры экрана
screen_width = 400
screen_height = 600

# Цвета
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# Инициализация экрана
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Пианино")

# Класс для представления белых прямоугольников
class WhiteRect(pygame.sprite.Sprite):
    def __init__(self, column):
        super().__init__()
        self.width = 50
        self.height = 20
        self.color = white
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.column = column
        self.rect.x = self.column * (screen_width // 4) + (screen_width // 8) - (self.width // 2)
        self.rect.y = 0
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > screen_height:
            self.rect.y = 0
            self.rect.x = self.column * (screen_width // 4) + (screen_width // 8) - (self.width // 2)
            self.image.fill(white)  # Возвращаем цвет к белому

# Инициализация группы спрайтов
all_sprites = pygame.sprite.Group()
white_rects = pygame.sprite.Group()

# Создание белых прямоугольников
for i in range(4):
    white_rect = WhiteRect(i)
    white_rect.rect.y = i * (screen_height // 4)
    white_rects.add(white_rect)
    all_sprites.add(white_rect)

# Горизонтальная красная линия
red_line = pygame.Rect(0, screen_height - 70, screen_width, 2)

# Зона для нажатия (жёлтая линия)
yellow_zone = pygame.Rect(0, screen_height - 130, screen_width, 35)

# Основной игровой цикл
clock = pygame.time.Clock()
score = 0

font = pygame.font.Font(None, 36)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                # Логика для клавиши D (первый столбик)
                for white_rect in white_rects:
                    if (
                        (white_rect.column == 0) and
                        (yellow_zone.collidepoint(white_rect.rect.x + white_rect.width // 2, white_rect.rect.y + white_rect.height))
                    ):
                        score += 1
                        print(f"Score: {score}")
                        white_rect.rect.y = 0
                        white_rect.image.fill(white)
                        break
                else:
                    score -= 1
                    print(f"Score: {score}")

            elif event.key == pygame.K_f:
                # Логика для клавиши F (второй столбик)
                for white_rect in white_rects:
                    if (
                        (white_rect.column == 1) and
                        (yellow_zone.collidepoint(white_rect.rect.x + white_rect.width // 2, white_rect.rect.y + white_rect.height))
                    ):
                        score += 1
                        print(f"Score: {score}")
                        white_rect.rect.y = 0
                        white_rect.image.fill(white)
                        break
                else:
                    score -= 1
                    print(f"Score: {score}")

            elif event.key == pygame.K_j:
                # Логика для клавиши J (третий столбик)
                for white_rect in white_rects:
                    if (
                        (white_rect.column == 2) and
                        (yellow_zone.collidepoint(white_rect.rect.x + white_rect.width // 2, white_rect.rect.y + white_rect.height))
                    ):
                        score += 1
                        print(f"Score: {score}")
                        white_rect.rect.y = 0
                        white_rect.image.fill(white)
                        break
                else:
                    score -= 1
                    print(f"Score: {score}")

            elif event.key == pygame.K_k:
                # Логика для клавиши K (четвертый столбик)
                for white_rect in white_rects:
                    if (
                        (white_rect.column == 3) and
                        (yellow_zone.collidepoint(white_rect.rect.x + white_rect.width // 2, white_rect.rect.y + white_rect.height))
                    ):
                        score += 1
                        print(f"Score: {score}")
                        white_rect.rect.y = 0
                        white_rect.image.fill(white)
                        break
                else:
                    score -= 1
                    print(f"Score: {score}")

    # Очистка экрана
    screen.fill(black)

    # Рисование вертикальных линий и клавиш
    for i in range(1, 5):
        pygame.draw.line(screen, green, (i * screen_width // 4, 0), (i * screen_width // 4, screen_height), 2)
        text = font.render(f"{i}", True, white)
        screen.blit(text, (i * screen_width // 4 - 10, screen_height + 30))

    # Рисование горизонтальной красной линии
    pygame.draw.rect(screen, red, red_line)

    # Рисование зоны для нажатия (жёлтая линия)
    pygame.draw.rect(screen, yellow, yellow_zone)

    # Обновление и отрисовка спрайтов
    all_sprites.update()
    all_sprites.draw(screen)

    # Проверка на полное пересечение красной линии и изменение цвета
    for white_rect in white_rects:
        if white_rect.rect.y + white_rect.height >= red_line.y and white_rect.color != blue:
            if white_rect.rect.y + white_rect.height > red_line.y:
                white_rect.image.fill(blue)

    # Обновление дисплея
    pygame.display.flip()

    # Задержка для управления частотой обновления
    clock.tick(50)