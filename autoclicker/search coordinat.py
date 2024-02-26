from tkinter import Tk, Canvas, filedialog
from PIL import Image, ImageTk
import json

class ImageSelector:
    def __init__(self, root, image_path):
        self.root = root
        self.image_path = image_path
        self.areas = {1: [], 2: [], 3: [], 4: []}
        self.pixel_colors = {}

        self.image = Image.open(image_path)
        self.tk_image = ImageTk.PhotoImage(self.image)

        self.canvas = Canvas(root, width=self.image.width, height=self.image.height)
        self.canvas.pack()

        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

        self.click_counter = 0
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.root.bind("<space>", self.save_config)

    def on_left_click(self, event):
        x, y = event.x, event.y
        self.click_counter += 1
        zone_number = (self.click_counter - 1) % 4 + 1
        self.canvas.create_rectangle(x - 15, y - 15, x + 15, y + 15, outline="red", width=2)
        self.areas[zone_number].append(((x - 15, y - 15), (x + 15, y + 15)))

    def on_right_click(self, event):
        x, y = event.x, event.y
        self.canvas.create_rectangle(x - 15, y - 15, x + 15, y + 15, outline="blue", width=2)

        pixel_colors = [self.image.getpixel((i, j)) for i in range(x - 15, x + 16) for j in range(y - 15, y + 16)]

        for color in pixel_colors:
            self.pixel_colors[color] = self.pixel_colors.get(color, 0) + 1

    def save_config(self, event):
        # Прямое преобразование координат областей в требуемый формат
        modified_areas = {str(zone): [coord for rect in rectangles for pair in rect for coord in pair]
                          for zone, rectangles in self.areas.items()}

        # Сохраняем данные в файл без внешнего ключа "areas"
        with open("coordinates.json", "w") as f_coords:
            json.dump(modified_areas, f_coords, indent=2)

        # Для цветов пикселей сохраняем как и раньше
        with open("pixel_colors.json", "w") as f_colors:
            json.dump({"pixel_colors": [[list(color), count] for color, count in self.pixel_colors.items()]}, f_colors,
                      indent=2)


def select_areas(image_path):
    root = Tk()
    root.title("Выбор областей")

    image_selector = ImageSelector(root, image_path)

    root.mainloop()

if __name__ == "__main__":
    image_path = filedialog.askopenfilename(title="Выберите изображение", filetypes=[("PNG files", "*.png")])

    if image_path:
        select_areas(image_path)




# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# from tkinter import Tk, Canvas, filedialog
# from PIL import Image, ImageTk
# import json
#
# class ImageSelector:
#     def __init__(self, root, image_path):
#         self.root = root
#         self.image_path = image_path
#         self.points = []
#
#         self.image = Image.open(image_path)
#         self.tk_image = ImageTk.PhotoImage(self.image)
#
#         self.canvas = Canvas(root, width=self.image.width, height=self.image.height)
#         self.canvas.pack()
#
#         self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)
#
#         self.canvas.bind("<Button-1>", self.on_left_click)
#         self.root.bind("<space>", self.save_config)
#
#     def on_left_click(self, event):
#         x, y = event.x, event.y
#         self.points.append((x, y))
#         self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="red")  # Отображаем точку
#         self.show_coordinates(x, y)
#
#     def show_coordinates(self, x, y):
#         text = f"({x}, {y})"
#         self.canvas.create_text(x, y - 10, text=text, fill="red")
#
#     def save_config(self, event):
#         with open("coordinates.json", "w") as f_coords:
#             json.dump({"points": self.points}, f_coords, indent=2)
#
# def select_areas(image_path):
#     root = Tk()
#     root.title("Выбор областей")
#
#     image_selector = ImageSelector(root, image_path)
#
#     root.mainloop()
#
# if __name__ == "__main__":
#     image_path = filedialog.askopenfilename(title="Выберите изображение", filetypes=[("PNG files", "*.png")])
#
#     if image_path:
#         select_areas(image_path)




