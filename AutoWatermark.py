from PIL import Image, ImageTk, ImageFont, ImageDraw
import tkinter as tk
from tkinter import messagebox, filedialog

def make_draggable(widget):
    # Function to make a widget draggable on the canvas
    canvas.tag_bind(widget, "<Button-1>", on_drag_start)
    canvas.tag_bind(widget, "<B1-Motion>", on_drag_motion)
    canvas.tag_bind(widget, "<ButtonRelease-1>", on_drag_release)

def on_drag_start(event):
    # Event handler for drag start
    widget = event.widget
    widget.startX = event.x
    widget.startY = event.y

def on_drag_motion(event):
    # Event handler for drag motion
    widget = event.widget
    dx = event.x - widget.startX
    dy = event.y - widget.startY
    widget.place(x=widget.winfo_x() + dx, y=widget.winfo_y() + dy)
    widget.startX = event.x
    widget.startY = event.y

def on_drag_release(event):
    # Event handler for drag release
    widget = event.widget
    widget.startX = None
    widget.startY = None

def save_watermark():
    # Function to save the watermarked image
    global finished_image
    watermarked_image = image.copy()
    font_size = font_size_entry.get()

    draw = ImageDraw.Draw(watermarked_image)
    font = ImageFont.truetype("arial.ttf", int(font_size))
    watermark_position = (photo_label.winfo_x(), photo_label.winfo_y())

    draw.text(watermark_position, text_entry.get(), font=font, fill=color_entry.get())
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    watermarked_image.save(save_path)
    finished_image = watermarked_image
    messagebox.showinfo("Watermark Saved", "Watermark saved successfully.")

def open_settings_window():
    # Function to open the settings window
    global text_entry, color_entry, font_size_entry, settings_window
    settings_window = tk.Toplevel(root)
    settings_window.title("Watermark Settings")
    settings_window.geometry("300x200")

    text_label = tk.Label(settings_window, text="Text:")
    text_entry = tk.Entry(settings_window)

    font_size_label = tk.Label(settings_window, text="Font Size:")
    font_size_entry = tk.Entry(settings_window)

    color_label = tk.Label(settings_window, text="Color:")
    color_entry = tk.Entry(settings_window)

    text_label.grid(row=0, column=0, padx=10, pady=5)
    text_entry.grid(row=0, column=1, padx=10, pady=5)

    font_size_label.grid(row=1, column=0, padx=10, pady=5)
    font_size_entry.grid(row=1, column=1, padx=10, pady=5)

    color_label.grid(row=2, column=0, padx=10, pady=5)
    color_entry.grid(row=2, column=1, padx=10, pady=5)

    confirm_button = tk.Button(settings_window, text="Confirm", command=lambda: apply_watermark_settings())
    confirm_button.grid(row=3, column=1, padx=10, pady=5)

def apply_watermark_settings():
    # Function to apply watermark settings
    global settings_window, font_size_entry, text_entry, color_entry
    font_size_value = font_size_entry.get()
    color_value = color_entry.get()
    text_value = text_entry.get()

    update_watermark_image(font_size_value, text_value, color_value)

    save_button = tk.Button(settings_window, text="Save Watermark", command=save_watermark)
    save_button.grid()

def update_watermark_image(font_size_value, text_value, color_value):
    # Function to update the watermark image
    global image
    watermarked_image = image.copy()
    draw = ImageDraw.Draw(watermarked_image)
    font = ImageFont.truetype("arial.ttf", int(font_size_value))
    watermark_position = (int(photo_label.winfo_rootx()), int(photo_label.winfo_rooty()))

    text_bbox = draw.textbbox((0, 0), text_value, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    watermark_text = Image.new("RGBA", watermarked_image.size, (0, 0, 0, 0))
    watermark_draw = ImageDraw.Draw(watermark_text)

    watermark_position = (
        (watermarked_image.width - text_width) // 2,
        (watermarked_image.height - text_height) // 2
    )
    watermark_draw.text((0, 0), text_value, font=font, fill=color_value)

    # Update the watermarked image
    watermarked_image.paste(watermark_text, (0, 0), mask=watermark_text)
    resized_image = watermarked_image.resize((photo_label.winfo_width(), photo_label.winfo_height()))
    image = resized_image

    # Update the image on the photo_label
    photo = ImageTk.PhotoImage(image)
    photo_label.configure(image=photo)
    photo_label.image = photo
    canvas.delete("watermark_overlay")  # Remove existing watermark overlay if present
    overlay_image = ImageTk.PhotoImage(watermark_text)

    overlay_label = canvas.create_image(photo_label.winfo_x(), photo_label.winfo_y(), image=overlay_image, tags="watermark_overlay")
    make_draggable(overlay_label)
    canvas.lower(overlay_label)

image = Image.open("c:\\Users\\User\\OneDrive\\Pictures\\IMG_1620.jpg")

root = tk.Tk()

button_style = {
    'bg': '#e0e0eb',
    'fg': 'black',
    'font': ('Arial', 12),
    'relief': 'raised',
}

new_size = (380, 300)
image = image.resize(new_size)

root.title("Watermark Editor")
root.geometry("400x300")
root.configure(bg="#cce6ff")
add_button = tk.Button(root, text="Add Text", command=open_settings_window, **button_style)
canvas = tk.Canvas(root, width=380, height=300)

photo = ImageTk.PhotoImage(image)
photo_label = tk.Label(root, image=photo)
canvas.create_window(190, 150, anchor='center', window=photo_label, tags='photo_label')

text_label = tk.Label(canvas, text="Sample Text", font=('Arial', 12), bg='white', relief='solid', bd=1)
text_label.place(x=0, y=0, anchor='nw', width=100)

text_label.bind("<ButtonPress-1>", on_drag_start)
text_label.bind("<B1-Motion>", on_drag_motion)
text_label.bind("<ButtonRelease-1>", on_drag_release)

add_button.grid(row=0, column=1, padx=10, pady=10)
photo_label.grid(row=1, column=0, rowspan=2, columnspan=3, sticky="nsew")

root.mainloop()