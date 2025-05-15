import pygame
import sys
import random
from math import sin

pygame.init()
pygame.mixer.init()  # Инициализация аудиосистемы

# Настройки окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Натураломер PRO MAX")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Загрузка звука
try:
    beep_sound = pygame.mixer.Sound("beppn.mp3")
    beep_sound.set_volume(0.3)  # Уменьшаем громкость
except FileNotFoundError:
    print("Ошибка: файл beppn.mp3 не найден")
    sys.exit()

# Шрифты
title_font = pygame.font.SysFont("comicsansms", 48)
percent_font = pygame.font.SysFont("impact", 80)

# Загрузка изображения кнопки
try:
    button_image = pygame.image.load("Clop.png").convert_alpha()
    button_image = pygame.transform.scale(button_image, (180, 180))
except FileNotFoundError:
    print("Ошибка: файл Clop.png не найден")
    sys.exit()

button_rect = button_image.get_rect(center=(WIDTH//2, HEIGHT//2 + 80))

# Переменные состояния
is_pressed = False
percent = 0.0
pulse_scale = 1.0

# Шкала прогресса
BAR_WIDTH = 500
BAR_HEIGHT = 40
bar_x = (WIDTH - BAR_WIDTH) // 2
bar_y = HEIGHT//2 - 120

def get_gradient_color(progress):
    r = int(255 * (progress/100))
    g = int(255 * (1 - progress/100))
    return (r, g, 10)

def draw_progress_bar(progress):
    # Фон шкалы
    pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, BAR_WIDTH, BAR_HEIGHT), border_radius=20)
    
    # Заполнение
    fill_width = int(BAR_WIDTH * (progress/100))
    if fill_width > 0:
        pygame.draw.rect(screen, get_gradient_color(progress), 
                        (bar_x, bar_y, fill_width, BAR_HEIGHT), border_radius=20)

def pulse_animation():
    return 1 + 0.15 * sin(pygame.time.get_ticks() * 0.005)

clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BLACK)
    
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                is_pressed = True
                # Запуск звука с повторением
                if beep_sound.get_num_channels() == 0:
                    beep_sound.play(loops=-1)
        elif event.type == pygame.MOUSEBUTTONUP:
            is_pressed = False
            # Остановка звука
            beep_sound.stop()

    # Логика прогресса
    if is_pressed:
        percent += random.uniform(0.8, 3.2)
        if percent > 100:
            percent = 100
        pulse_scale = pulse_animation()
    else:
        if percent > 0:
            percent -= 4.5
            if percent < 0:
                percent = 0
        pulse_scale = 1.0

    # Отрисовка элементов
    # Заголовок
    title_text = title_font.render("Натураломер", True, WHITE)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 30))

    # Процент
    percent_text = percent_font.render(f"{int(percent)}%", True, WHITE)
    screen.blit(percent_text, (WIDTH//2 - percent_text.get_width()//2, bar_y - 80))

    # Шкала прогресса
    draw_progress_bar(percent)

    # Анимированная кнопка
    scaled_button = pygame.transform.scale(button_image, 
        (int(180 * pulse_scale), int(180 * pulse_scale)))
    btn_rect = scaled_button.get_rect(center=button_rect.center)
    screen.blit(scaled_button, btn_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()