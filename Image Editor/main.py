import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageEnhance, ImageTk, ImageOps

class SimpleImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Image Editor")
        self.root.configure(bg='black')  # Set background color to black

        self.image = None
        self.original_image = None
        self.tk_img = None
        self.filename = None
        self.canvas = None
        self.rect = None
        self.start_x = self.start_y = self.end_x = self.end_y = 0

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_label = tk.Label(self.root, text="Edit Options", bg='black', fg='white', font=('Arial', 16, 'bold'))
        title_label.pack(side=tk.TOP, anchor='w', padx=10, pady=10)

        # Frame for Buttons
        button_frame = tk.Frame(self.root, bg='black')
        button_frame.pack(side=tk.LEFT, padx=10, pady=(20, 10))  # Adjusted vertical padding to lift buttons up

        # Buttons for loading and saving image
        load_btn = tk.Button(button_frame, text="Load Image", command=self.load_image, bg='sky blue', fg='black')
        load_btn.pack(pady=5)

        save_btn = tk.Button(button_frame, text="Save Image", command=self.save_image, bg='lime', fg='black')
        save_btn.pack(pady=5)

        crop_btn = tk.Button(button_frame, text="Crop Image", command=self.activate_crop, bg='white', fg='black')
        crop_btn.pack(pady=5)

        rotate_btn = tk.Button(button_frame, text="Rotate 90°", command=self.rotate_image, bg='white', fg='black')
        rotate_btn.pack(pady=5)

        flip_btn = tk.Button(button_frame, text="Flip Horizontal", command=self.flip_image, bg='white', fg='black')
        flip_btn.pack(pady=5)

        # Effect sliders (bars)
        self.create_sliders()

        # Canvas for displaying the image
        self.canvas = tk.Canvas(self.root, bg='white', highlightbackground='black')
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def create_sliders(self):
        slider_frame = tk.Frame(self.root, bg='black')
        slider_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        # Brightness Slider
        tk.Label(slider_frame, text="Brightness", bg='black', fg='white').pack()
        self.brightness_slider = tk.Scale(slider_frame, from_=1, to=100, orient=tk.HORIZONTAL, command=self.adjust_brightness)
        self.brightness_slider.set(50)  # Default value
        self.brightness_slider.pack()

        # Contrast Slider
        tk.Label(slider_frame, text="Contrast", bg='black', fg='white').pack()
        self.contrast_slider = tk.Scale(slider_frame, from_=1, to=100, orient=tk.HORIZONTAL, command=self.adjust_contrast)
        self.contrast_slider.set(50)  # Default value
        self.contrast_slider.pack()

        # Saturation Slider
        tk.Label(slider_frame, text="Saturation", bg='black', fg='white').pack()
        self.saturation_slider = tk.Scale(slider_frame, from_=1, to=100, orient=tk.HORIZONTAL, command=self.adjust_saturation)
        self.saturation_slider.set(50)  # Default value
        self.saturation_slider.pack()

        # Sharpness Slider
        tk.Label(slider_frame, text="Sharpness", bg='black', fg='white').pack()
        self.sharpness_slider = tk.Scale(slider_frame, from_=1, to=100, orient=tk.HORIZONTAL, command=self.adjust_sharpness)
        self.sharpness_slider.set(50)  # Default value
        self.sharpness_slider.pack()

    def load_image(self):
        filetypes = [("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        self.filename = filedialog.askopenfilename(title="Open Image", filetypes=filetypes)

        if self.filename:
            self.image = Image.open(self.filename)
            self.original_image = self.image.copy()  # Store a copy of the original image
            self.show_image()

    def show_image(self):
        if self.image:
            # Resize image to fit within the canvas size
            self.tk_img = ImageTk.PhotoImage(self.image)
            self.canvas.config(width=self.tk_img.width(), height=self.tk_img.height())
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)
            self.canvas.create_rectangle(0, 0, self.tk_img.width(), self.tk_img.height(), outline='black', width=2)

            # Bind mouse events for cropping
            self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
            self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
            self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

    def activate_crop(self):
        messagebox.showinfo("Crop Mode", "Click and drag on the image to select the crop area.")

    def on_mouse_down(self, event):
        self.start_x = event.x
        self.start_y = event.y

        # If there was a previous rectangle, remove it
        if self.rect:
            self.canvas.delete(self.rect)

        # Start drawing a new rectangle
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def on_mouse_drag(self, event):
        self.end_x = event.x
        self.end_y = event.y

        # Update the rectangle's size dynamically as the mouse moves
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.end_x, self.end_y)

    def on_mouse_up(self, event):
        self.end_x = event.x
        self.end_y = event.y

        # Perform cropping after the user releases the mouse button
        self.perform_crop()

    def perform_crop(self):
        if self.image:
            # Calculate the crop box based on the mouse coordinates
            crop_box = (min(self.start_x, self.end_x), min(self.start_y, self.end_y),
                        max(self.start_x, self.end_x), max(self.start_y, self.end_y))

            # Crop the image
            self.image = self.image.crop(crop_box)
            self.show_image()  # Update the image in the GUI

    # Image Manipulation with sliders
    def adjust_brightness(self, value):
        if self.original_image:
            enhancer = ImageEnhance.Brightness(self.original_image)
            self.image = enhancer.enhance(float(value) / 50)  # Normalize the range
            self.show_image()

    def adjust_contrast(self, value):
        if self.original_image:
            enhancer = ImageEnhance.Contrast(self.original_image)
            self.image = enhancer.enhance(float(value) / 50)  # Normalize the range
            self.show_image()

    def adjust_saturation(self, value):
        if self.original_image:
            enhancer = ImageEnhance.Color(self.original_image)
            self.image = enhancer.enhance(float(value) / 50)  # Normalize the range
            self.show_image()

    def adjust_sharpness(self, value):
        if self.original_image:
            enhancer = ImageEnhance.Sharpness(self.original_image)
            self.image = enhancer.enhance(float(value) / 50)  # Normalize the range
            self.show_image()

    # Other image manipulations
    def rotate_image(self):
        if self.image:
            self.image = self.image.rotate(-90, expand=True)  # Rotate 90 degrees clockwise
            self.original_image = self.image.copy()  # Update the original image after rotating
            self.show_image()

    def flip_image(self):
        if self.image:
            self.image = ImageOps.mirror(self.image)  # Flip horizontally
            self.original_image = self.image.copy()  # Update the original image after flipping
            self.show_image()

    def save_image(self):
        if self.image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            if save_path:
                self.image.save(save_path)
                messagebox.showinfo("Image Saved", "Image saved successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")  # Resize window
    app = SimpleImageEditor(root)
    root.mainloop()
