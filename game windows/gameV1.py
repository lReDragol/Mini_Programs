import tkinter as tk
from screeninfo import get_monitors
import random


# Получение размера экрана
monitor = get_monitors()[0]
screen_width = monitor.width
screen_height = monitor.height

# Параметры окон
window_size = 100  # Размер каждого окна
grid_size = 3  # Размер сетки (3x3)
spacing = 200  # Расстояние между окнами
swap_count = 15  # Количество смен местами
move_speed = 40  # Скорость перемещения окон (меньше значение = быстрее)
swap_delay = 75  # Задержка между сменами местами в миллисекундах

# Создание основного окна (не будет отображаться, но необходимо для Tkinter)
root = tk.Tk()
root.withdraw()

windows = []
positions = []
black_window_index = None
animation_completed_count = 0  # Счетчик завершенных анимаций

def move_window(win, start_x, start_y, end_x, end_y, on_complete=None):
    steps = 10  # Количество шагов для плавного перемещения
    dx = (end_x - start_x) / steps
    dy = (end_y - start_y) / steps
    for step in range(steps + 1):
        root.after(step * move_speed, lambda s=step: win.geometry(f"{window_size}x{window_size}+{int(start_x + dx * s)}+{int(start_y + dy * s)}"))
        if step == steps and on_complete:
            root.after(step * move_speed, on_complete)

def on_window_click(is_black):
    def change_color():
        for win in windows:
            win.configure(bg='green' if is_black else 'red')
    return change_color

# Создание и размещение окон
for i in range(grid_size):
    for j in range(grid_size):
        x = (screen_width - (grid_size * window_size) - (grid_size - 1) * spacing) / 2 + j * (window_size + spacing)
        y = (screen_height - (grid_size * window_size) - (grid_size - 1) * spacing) / 2 + i * (window_size + spacing)
        win = tk.Toplevel(root, width=window_size, height=window_size)
        win.geometry(f"{window_size}x{window_size}+{int(x)}+{int(y)}")
        windows.append(win)
        positions.append((x, y))

# Выбор и закрашивание случайного окна в черный
black_window_index = random.randint(0, len(windows) - 1)
windows[black_window_index].configure(bg='black')
for i, win in enumerate(windows):
    if i == black_window_index:
        win.bind("<Button-1>", lambda e, is_black=True: on_window_click(is_black)())
    else:
        win.bind("<Button-1>", lambda e, is_black=False: on_window_click(is_black)())

def shuffle_windows(on_all_complete):
    global animation_completed_count
    animation_completed_count = 0
    final_positions = random.sample(positions, len(positions))

    def on_animation_complete():
        global animation_completed_count
        animation_completed_count += 1
        if animation_completed_count == len(windows):
            on_all_complete()

    for win, (new_x, new_y) in zip(windows, final_positions):
        current_geometry = win.geometry().split('+')
        current_x, current_y = int(current_geometry[1]), int(current_geometry[2])
        move_window(win, current_x, current_y, new_x, new_y, on_animation_complete)

def start_shuffle_sequence(count):
    if count > 0:
        shuffle_windows(lambda: root.after(swap_delay, lambda: start_shuffle_sequence(count - 1)))

def turn_white_and_shuffle():
    windows[black_window_index].configure(bg='white')
    # Запуск последовательности перемешивания с заданным количеством смен местами
    root.after(swap_delay, lambda: start_shuffle_sequence(swap_count))

# Через 5 секунд сделать выбранное окно белым и начать смену местами
root.after(5000, turn_white_and_shuffle)

# Запуск основного цикла событий Tkinter
root.mainloop()
