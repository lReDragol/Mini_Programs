import tkinter as tk
import json
import keyboard
import numpy as np
import time

def load_coordinates(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
        areas = data.get("areas", {})
        return areas

def load_pixel_colors(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
        pixel_colors_data = data.get("pixel_colors", [])
        pixel_colors = np.array([item[0][::-1] for item in pixel_colors_data])
        return pixel_colors

def draw_areas(canvas, areas):
    for area_num, coordinates_list in areas.items():
        for coordinates in coordinates_list:
            x1, y1, x2, y2 = coordinates[0][0], coordinates[0][1], coordinates[1][0], coordinates[1][1]
            canvas.create_rectangle(x1, y1, x2, y2, outline='red', width=2)
            canvas.create_text((x1 + x2) / 2, y1, text=str(area_num), anchor='s', fill='red',
                               font=('Helvetica', 12, 'bold'))

def draw_red_square(canvas, square_size):
    square_x = 0
    square_y = 0
    canvas.create_rectangle(square_x, square_y, square_x + square_size, square_y + square_size, outline='red', width=2)

def press_key(zone_num):
    key_mapping = {1: 'd', 2: 'f', 3: 'j', 4: 'k'}
    key = key_mapping.get(zone_num)
    if key:
        keyboard.press_and_release(key)

def check_areas(areas, pixel_colors, threshold_percentage):
    for area_num, coordinates_list in areas.items():
        for coordinates in coordinates_list:
            x1, y1, x2, y2 = coordinates[0][0], coordinates[0][1], coordinates[1][0], coordinates[1][1]
            area_colors = pixel_colors[y1:y2, x1:x2]
            total_pixels = area_colors.shape[0] * area_colors.shape[1]

            if total_pixels > 0:
                unique_colors, counts = np.unique(area_colors.reshape(-1, area_colors.shape[-1]), axis=0,
                                                  return_counts=True)
                matching_pixels = np.sum(counts)
                percentage = (matching_pixels / total_pixels) * 100

                if percentage >= threshold_percentage:
                    press_key(area_num)

                print(f"[{area_num}] {percentage:.2f}%")
            else:
                print(f"[{area_num}] 0% (No pixels in the area)")

def main():
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    root.wm_attributes("-transparentcolor", "white")

    canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), bg='white',
                       highlightthickness=0)
    canvas.pack()

    areas = load_coordinates("coordinates.json")
    draw_areas(canvas, areas)
    draw_red_square(canvas, 50)

    pixel_colors = load_pixel_colors("pixel_colors.json")
    threshold_percentage = 30

    def on_close():
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    while True:
        check_areas(areas, pixel_colors, threshold_percentage)
        root.update_idletasks()
        root.update()
        time.sleep(0.4)

if __name__ == "__main__":
    main()
