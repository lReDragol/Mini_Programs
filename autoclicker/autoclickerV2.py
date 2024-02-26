import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
import pygetwindow as gw
import pyautogui
import keyboard
import json
import math
import time

class EuclideanDistTracker:
    def __init__(self):
        self.center_points = {}
        self.id_count = 0

    def update(self, objects_rect):
        objects_bbs_ids = []
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])
                if dist < 25:
                    self.center_points[id] = (cx, cy)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break

            if not same_object_detected:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center
        self.center_points = new_center_points.copy()
        return objects_bbs_ids

def load_coordinates(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data.get("areas", {})

def load_pixel_colors(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    pixel_colors_data = data.get("pixel_colors", [])
    if pixel_colors_data:
        max_color_count_pair = max(pixel_colors_data, key=lambda x: x[1])
        return np.array(max_color_count_pair[0])
    return np.array([0, 0, 0])  # Fallback color

def press_key(zone_num):
    key_mapping = {"1": 'd', "2": 'f', "3": 'j', "4": 'k'}
    key = key_mapping.get(zone_num)
    if key:
        print(f"Pressing key: {key}")
        keyboard.send(key)

# Глобальные переменные для управления видимостью окна Frame
frame_visible = True
last_frame = None

# Инициализация Tkinter окна
root = tk.Tk()
root.title("Object Tracking and Control")

# Создаем объект трекера
tracker = EuclideanDistTracker()

def draw_areas_on_frame(frame, areas):
    for area_num, coordinates_list in areas.items():
        for coordinates in coordinates_list:
            x1, y1, x2, y2 = coordinates
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Красный прямоугольник
            cv2.putText(frame, str(area_num), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

def update_window():
    global last_frame, frame_visible
    selected_window = combo.get()
    window = gw.getWindowsWithTitle(selected_window)[0] if gw.getWindowsWithTitle(selected_window) else None
    if window:
        areas = load_coordinates("coordinates.json")
        object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

        while True:
            x, y, width, height = window.left, window.top, window.width, window.height
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            last_frame = frame

            # Обнаружение объектов
            mask = object_detector.apply(frame)
            _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            detections = [cv2.boundingRect(cnt) for cnt in contours if cv2.contourArea(cnt) > 100]

            # Отслеживание объектов
            boxes_ids = tracker.update(detections)
            for box_id in boxes_ids:
                x, y, w, h, id = box_id
                cv2.putText(frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

            # Отрисовка зон на кадре
            for area_num, coordinates_list in areas.items():
                for coordinates in coordinates_list:
                    x1, y1, x2, y2 = coordinates
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(frame, str(area_num), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

            # Проверяем переменную frame_visible перед отображением окна Frame
            if frame_visible:
                cv2.imshow("Frame", frame)
            else:
                cv2.destroyWindow("Frame")

            cv2.imshow("Mask", mask)

            key = cv2.waitKey(30)
            if key == 27:  # ESC для выхода
                break
    else:
        print(f"Окно с заголовком '{selected_window}' не найдено.")



def toggle_frame_visibility():
    global frame_visible
    frame_visible = not frame_visible
    if frame_visible and last_frame is not None:
        cv2.imshow("Frame", last_frame)
    elif not frame_visible:
        cv2.destroyWindow("Frame")

# Создание интерфейса для выбора окна
window_list = [title for title in gw.getAllTitles() if title]
combo = ttk.Combobox(root, values=window_list, width=50)
combo.grid(row=0, column=0, padx=10, pady=10)

update_button = tk.Button(root, text="Start Tracking", command=update_window)
update_button.grid(row=0, column=1, padx=10, pady=10)

toggle_frame_button = tk.Button(root, text="Toggle Frame Visibility", command=toggle_frame_visibility)
toggle_frame_button.grid(row=1, column=0, columnspan=2, pady=10)

root.mainloop()
cv2.destroyAllWindows()
