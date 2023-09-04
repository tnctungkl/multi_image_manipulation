from tkinter import *
from tkinter import messagebox, ttk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk, ImageFilter, ImageOps
from PIL.Image import Transpose


class ImageManipulation:
    def __init__(self, master):
        self.tk_image = None
        self.master = master
        self.master.title("Image Manipulation")
        self.master.geometry("1080x800")

        self.images = []
        self.current_image_index = -1
        self.selected_image = None
        self.original_images = []

        self.canvas = Canvas(self.master, width=500, height=500)
        self.canvas.pack(side=TOP, pady=10)

        self.image_label = Label(self.master, text="", anchor=CENTER, justify=CENTER)
        self.image_label.pack(side=TOP, padx=20)

        self.button_frame = Frame(self.master)
        self.button_frame.pack(side=TOP, pady=(0, 2))

        self.rotate_button = ttk.Button(self.button_frame, text="Rotate", command=self.rotate_image)
        self.rotate_button.pack(side=LEFT, padx=10)

        self.crop_button = ttk.Button(self.button_frame, text="Crop", command=self.crop_image)
        self.crop_button.pack(side=LEFT, padx=10)

        self.blur_button = ttk.Button(self.button_frame, text="Blur", command=self.blur_image)
        self.blur_button.pack(side=LEFT, padx=10)

        self.resize_button = ttk.Button(self.button_frame, text="Resize", command=self.resize_image)
        self.resize_button.pack(side=LEFT, padx=10)

        self.color_button = ttk.Button(self.button_frame, text="Color", command=self.color_image)
        self.color_button.pack(side=LEFT, padx=10)

        mirror_button = ttk.Button(self.button_frame, text="Mirror", command=self.mirror_effect)
        mirror_button.pack(side=LEFT, padx=10)

        self.load_button = ttk.Button(self.button_frame, text="Load", command=self.load_image)
        self.load_button.pack(side=LEFT, padx=10)

        self.save_button = ttk.Button(self.master, text="Save", command=self.save_file)
        self.save_button.pack(side=RIGHT, padx=20)

        previous_button = ttk.Button(self.master, text="Previous", command=self.previous_image)
        previous_button.pack(side=LEFT, padx=10)

        next_button = ttk.Button(self.master, text="Next", command=self.next_image)
        next_button.pack(side=LEFT, padx=10)

        self.bottom_frame = Frame(self.master, height=2)
        self.bottom_frame.pack(side=BOTTOM)

        reset_button = ttk.Button(self.button_frame, text="Reset", command=self.reset_image)
        reset_button.pack(side=LEFT, padx=10)

    def load_image(self):
        file_path = filedialog.askopenfilename()
        image = Image.open(file_path)
        self.images.append(image)
        self.original_images.append(image.copy())
        self.current_image_index = len(self.images) - 1
        self.update_canvas()
        self.update_image_label(file_path)

    def reset_image(self):
        if self.current_image_index != -1:
            self.images[self.current_image_index] = self.original_images[self.current_image_index].copy()
            self.update_canvas()

    def select_image(self):
        if self.current_image_index != -1:
            selected_image = self.images[self.current_image_index]

    def next_image(self):
        if self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            self.update_canvas()
            self.update_image_label()
            self.select_image()

    def previous_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.update_canvas()
            self.update_image_label()
            self.select_image()

    def mirror_effect(self):
        if self.current_image_index != -1:
            mirror_direction = simpledialog.askstring("Mirror Effect", "Choose mirror direction (x/y/diagonal):")
            if mirror_direction is None:
                return
            if mirror_direction and mirror_direction.lower() == "x":
                self.images[self.current_image_index] = ImageOps.mirror(self.images[self.current_image_index])
            elif mirror_direction and mirror_direction.lower() == "y":
                self.images[self.current_image_index] = ImageOps.flip(self.images[self.current_image_index])
            elif mirror_direction and mirror_direction.lower() == "diagonal":
                degrees = simpledialog.askinteger("Mirror Effect", "Choose rotation degrees (45/135/225/315):")
                if degrees is None:
                    return
                if degrees not in [45, 135, 225, 315]:
                    messagebox.showerror("Error", "Invalid rotation degrees! Valid options: 45, 135, 225, 315.")
                    self.mirror_effect()
                    return
                self.images[self.current_image_index] = self.images[self.current_image_index].transpose(
                    Transpose.TRANSPOSE).rotate(degrees, expand=True)
            else:
                messagebox.showerror("Error", "Invalid mirror direction! Valid options: x, y, diagonal.")
                self.mirror_effect()
            self.update_canvas()

    def rotate_image(self):
        if self.current_image_index != -1:
            current_degrees = 0
            degrees = simpledialog.askinteger("Rotate", "Enter rotation degrees:")
            if degrees is None:
                return
            self.images[self.current_image_index] = self.images[self.current_image_index].rotate(degrees, expand=True)
            self.update_canvas()
            self.fit_to_canvas()

    def undo_rotate(self):
        if self.current_image_index != -1:
            self.images[self.current_image_index] = self.images[self.current_image_index].copy()
            self.update_canvas()
            self.fit_to_canvas()

    def fit_to_canvas(self):
        if self.current_image_index != -1:
            image = self.images[self.current_image_index]
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            image_width, image_height = image.size

            scale_factor = min(canvas_width / image_width, canvas_height / image_height)
            new_width = int(image_width * scale_factor)
            new_height = int(image_height * scale_factor)
            resized_image = image.resize((new_width, new_height))

            x_offset = (canvas_width - new_width) // 2
            y_offset = (canvas_height - new_height) // 2

            self.canvas.delete("all")
            self.tk_image = ImageTk.PhotoImage(resized_image)
            self.canvas.create_image(x_offset, y_offset, anchor=NW, image=self.tk_image)
            self.canvas.update()

    def crop_image(self):
        if self.current_image_index != -1:
            image = self.images[self.current_image_index]
            width = simpledialog.askinteger("Crop", "Enter the width:")
            height = simpledialog.askinteger("Crop", "Enter the height:")
            self.images[self.current_image_index] = image.crop((0, 0, width, height))
            self.update_canvas()

    def blur_image(self):
        if self.current_image_index != -1:
            image = self.images[self.current_image_index]
            self.images[self.current_image_index] = image.filter(ImageFilter.BLUR)
            self.update_canvas()

    def resize_image(self):
        if self.current_image_index != -1:
            image = self.images[self.current_image_index]
            current_width, current_height = image.size

            new_width = simpledialog.askinteger("Resize", "Enter width:", minvalue=1, maxvalue=current_width)
            if new_width is None:
                return
            new_height = simpledialog.askinteger("Resize", "Enter height:", minvalue=1, maxvalue=current_height)
            if new_height is None:
                return
            self.images[self.current_image_index] = image.resize((new_width, new_height))
            self.update_canvas()

    def undo_resize(self):
        if self.current_image_index != -1:
            image = self.images[self.current_image_index]
            width, height = image.size
            self.images[self.current_image_index] = image.resize((width, height))
            self.update_canvas()

    def color_image(self):
        if self.current_image_index != -1:
            image = self.images[self.current_image_index]
            color_dialog = Toplevel(self.master)
            color_dialog.geometry("379x70")

            red_button = Button(color_dialog, text="Red", command=lambda: self.color_filter(image, "red"))
            red_button.pack(side=LEFT, padx=10)

            green_button = Button(color_dialog, text="Green", command=lambda: self.color_filter(image, "green"))
            green_button.pack(side=LEFT, padx=10)

            blue_button = Button(color_dialog, text="Blue", command=lambda: self.color_filter(image, "blue"))
            blue_button.pack(side=LEFT, padx=10)

            negative_button = Button(color_dialog, text="Negative",
                                     command=lambda: self.color_filter(image, "negative"))
            negative_button.pack(side=LEFT, padx=10)

            grayscale_button = Button(color_dialog, text="Grayscale",
                                      command=lambda: self.color_filter(image, "grayscale"))
            grayscale_button.pack(side=LEFT, padx=10)

    def color_filter(self, image, filter_type):
        if filter_type == "red":
            self.images[self.current_image_index] = image.copy()
            pixels = self.images[self.current_image_index].load()
            width, height = self.images[self.current_image_index].size
            for y in range(height):
                for x in range(width):
                    r, g, b = pixels[x, y]
                    pixels[x, y] = r, 0, 0
        elif filter_type == "green":
            self.images[self.current_image_index] = image.copy()
            pixels = self.images[self.current_image_index].load()
            width, height = self.images[self.current_image_index].size
            for y in range(height):
                for x in range(width):
                    r, g, b = pixels[x, y]
                    pixels[x, y] = 0, g, 0
        elif filter_type == "blue":
            self.images[self.current_image_index] = image.copy()
            pixels = self.images[self.current_image_index].load()
            width, height = self.images[self.current_image_index].size
            for y in range(height):
                for x in range(width):
                    r, g, b = pixels[x, y]
                    pixels[x, y] = 0, 0, b
        elif filter_type == "negative":
            self.images[self.current_image_index] = image.copy()
            pixels = self.images[self.current_image_index].load()
            width, height = self.images[self.current_image_index].size
            for y in range(height):
                for x in range(width):
                    r, g, b = pixels[x, y]
                    pixels[x, y] = 255 - r, 255 - g, 255 - b
        elif filter_type == "grayscale":
            self.images[self.current_image_index] = image.copy()
            pixels = self.images[self.current_image_index].load()
            width, height = self.images[self.current_image_index].size
            for y in range(height):
                for x in range(width):
                    r, g, b = pixels[x, y]
                    gray = int(0.2989 * r + 0.587 * g + 0.114 * b)
                    pixels[x, y] = gray, gray, gray
        self.update_canvas()

    def update_canvas(self):
        if self.current_image_index != -1:
            image = self.images[self.current_image_index]
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            image_width, image_height = image.size

            scale_factor = min(canvas_width / image_width, canvas_height / image_height)
            new_width = int(image_width * scale_factor)
            new_height = int(image_height * scale_factor)
            resized_image = image.resize((new_width, new_height))

            x_offset = (canvas_width - new_width) // 2
            y_offset = (canvas_height - new_height) // 2

            self.canvas.delete("all")
            self.tk_image = ImageTk.PhotoImage(resized_image)
            self.canvas.create_image(x_offset, y_offset, anchor=NW, image=self.tk_image)
            self.canvas.update()

    def update_image_label(self, file_path=""):
        if file_path:
            file_name = file_path.split("/")[-1]
            self.image_label.configure(text=file_name)
        else:
            self.image_label.configure(text="")

    def save_file(self):
        if self.current_image_index != -1:
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("JPEG Image", "*.jpg"), ("PNG Image", "*.png")])
            if save_path:
                self.images[self.current_image_index].save(save_path)


if __name__ == "__main__":
    root = Tk()
    ImageManipulation(root)
    root.mainloop()
