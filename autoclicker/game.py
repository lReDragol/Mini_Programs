import pygame
import sys
import random

pygame.init()

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
COLORS = {"white": (255, 255, 255), "black": (0, 0, 0), "red": (255, 0, 0),
          "green": (0, 255, 0), "blue": (0, 0, 255), "yellow": (255, 255, 0)}
KEY_MAPPING = {pygame.K_d: 0, pygame.K_f: 1, pygame.K_j: 2, pygame.K_k: 3}

# Инициализация экрана и компонентов
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Пианино")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

class WhiteRect(pygame.sprite.Sprite):
    def __init__(self, column, speed=5):
        super().__init__()
        self.image = pygame.Surface((50, 20))
        self.image.fill(COLORS["white"])
        self.rect = self.image.get_rect(center=(column * (SCREEN_WIDTH // 4) + (SCREEN_WIDTH // 8), 0))
        self.speed = speed
        self.column = column

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()  # Удаляем спрайт, если он выходит за пределы экрана

def draw_ui():
    screen.fill(COLORS["black"])
    pygame.draw.rect(screen, COLORS["red"], (0, SCREEN_HEIGHT - 70, SCREEN_WIDTH, 2))
    pygame.draw.rect(screen, COLORS["yellow"], (0, SCREEN_HEIGHT - 130, SCREEN_WIDTH, 55))
    for i in range(1, 5):
        pygame.draw.line(screen, COLORS["green"], (i * SCREEN_WIDTH // 4, 0), (i * SCREEN_WIDTH // 4, SCREEN_HEIGHT), 2)

def handle_key_press(key, rects, score):
    if key in KEY_MAPPING:
        column = KEY_MAPPING[key]
        for rect in rects:
            if rect.column == column and rect.rect.colliderect((0, SCREEN_HEIGHT - 130, SCREEN_WIDTH, 55)):
                score += 1
                rect.kill()  # Удаляем спрайт при успешном нажатии
                return score, True
    return score - 1, False

def game_loop():
    score = 0
    all_sprites = pygame.sprite.Group()
    next_rect_time = 0
    rect_delay = 500  # Начальная задержка в миллисекундах

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        if current_time > next_rect_time:
            rect_count = random.randint(1, 3)  # Случайное количество прямоугольников
            columns = random.sample(range(4), rect_count)  # Случайный выбор столбцов без повторений
            for column in columns:
                rect = WhiteRect(column)
                all_sprites.add(rect)
            next_rect_time = current_time + rect_delay + random.randint(0, 1000)  # Следующее появление

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                score, hit = handle_key_press(event.key, all_sprites, score)
                if hit:
                    print(f"Score: {score}")

        all_sprites.update()
        draw_ui()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(50)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
