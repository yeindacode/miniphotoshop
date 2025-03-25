import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk
import os
import io  # Import the io module
 
class DrawingApp:
    def __init__(self, master):
        self.master = master
        master.title("Drawing Application")
 
        self.width = 1000
        self.height = 1000
        self.brush_color = "black"
        self.eraser_color = "white"  # Match background if needed.  Important!
        self.brush_radius = 5
        self.brush_opacity = 1.0  # Full opacity initially
        self.brush_sharpness = 0.5 # sharpness 0.0 - 1.0 where 0 is blur and 1 is hard edge
        self.tool = "brush"  # Initially the brush is selected
        self.last_x = None
        self.last_y = None
 
        # Create a PIL Image and a Tk PhotoImage
        self.image = Image.new("RGB", (self.width, self.height), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.photo = ImageTk.PhotoImage(self.image)
 
        # Canvas widget to display the image
        self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg="white")
        self.canvas.pack(side=tk.LEFT)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)
 
        # Frame for controls
        self.controls_frame = tk.Frame(master)
        self.controls_frame.pack(side=tk.RIGHT, padx=10)
 
        # Brush Radius Slider
        self.radius_label = tk.Label(self.controls_frame, text="Brush Radius:")
        self.radius_label.pack()
        self.radius_slider = ttk.Scale(self.controls_frame, from_=1, to=50, orient=tk.HORIZONTAL, command=self.update_radius)
        self.radius_slider.set(self.brush_radius) # Set initial value
        self.radius_slider.pack()
 
        # Opacity Slider
        self.opacity_label = tk.Label(self.controls_frame, text="Opacity:")
        self.opacity_label.pack()
        self.opacity_slider = ttk.Scale(self.controls_frame, from_=0, to=1, orient=tk.HORIZONTAL, command=self.update_opacity)
        self.opacity_slider.set(self.brush_opacity)
        self.opacity_slider.pack()
 
        # Sharpness Slider
        self.sharpness_label = tk.Label(self.controls_frame, text="Sharpness:")
        self.sharpness_label.pack()
        self.sharpness_slider = ttk.Scale(self.controls_frame, from_=0, to=1, orient=tk.HORIZONTAL, command=self.update_sharpness)
        self.sharpness_slider.set(self.brush_sharpness)
        self.sharpness_slider.pack()
 
 
 
        # Color Chooser Button
        self.color_button = tk.Button(self.controls_frame, text="Choose Color", command=self.choose_color)
        self.color_button.pack()
 
        # Keybindings
        master.bind("b", self.set_brush)
        master.bind("e", self.set_eraser)
        master.bind("s", self.export_image)
 
 
    def paint(self, event):
        if self.last_x and self.last_y:
            x1, y1 = (self.last_x, self.last_y)
            x2, y2 = (event.x, event.y)
 
            # Get the color based on the active tool
            color = self.brush_color if self.tool == "brush" else self.eraser_color
 
            # Apply opacity
            rgba_color = self.hex_to_rgba(color, self.brush_opacity)
 
            # Draw the line on the PIL Image
            self.draw_line(x1, y1, x2, y2, rgba_color, self.brush_radius, self.brush_sharpness)
 
            # Update the Tk PhotoImage with the modified PIL Image
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
 
        self.last_x = event.x
        self.last_y = event.y
 
 
    def draw_line(self, x1, y1, x2, y2, color, radius, sharpness):
        """Draws a line with variable radius, opacity, and sharpness."""
        line_width = int(radius * 2)
        self.draw.line((x1, y1, x2, y2), fill=color, width=line_width) # Simple drawing
        # Could add more sophisticated blur or blending here based on sharpness
 
 
 
    def reset(self, event):
        self.last_x, self.last_y = None, None
 
 
    def update_radius(self, value):
        self.brush_radius = int(float(value))
 
 
    def update_opacity(self, value):
         self.brush_opacity = float(value)
 
    def update_sharpness(self, value):
        self.brush_sharpness = float(value)
 
    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose brush color")
        if color_code:
            self.brush_color = color_code[1]  # color_code is a tuple; [1] is the hex color
 
 
    def set_brush(self, event=None):
        self.tool = "brush"
 
 
    def set_eraser(self, event=None):
        self.tool = "eraser"
 
 
    def hex_to_rgba(self, hex_color, opacity):
        """Convert hex color to RGBA with opacity."""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return rgb + (int(opacity * 255),)  # RGBA tuple
 
 
    def export_image(self, event=None):
        try:
            download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
            filepath = os.path.join(download_folder, "drawing.png")
            self.image.save(filepath, "PNG")
            print(f"Image saved to {filepath}")
        except Exception as e:
            print(f"Error saving image: {e}")
 
 
root = tk.Tk()
app = DrawingApp(root)
root.mainloop()