
import HIServices

# Force Accessibility API to initialise before pynput loads
HIServices.AXIsProcessTrusted()



import tkinter as tk
from tkinter import ttk
from pynput.mouse import Button, Controller
from pynput import keyboard, mouse
import threading
import time
import math

mouse_controller = Controller()

clicking = False
click_key = 'q'
interval = 0.01
listening_for_key = False


# ---------------- AUTO CLICK FUNCTION ----------------
def auto_click():
    global clicking, interval
    while True:
        if clicking:
            mouse_controller.press(Button.left)
            mouse_controller.release(Button.left)
            time.sleep(interval)
        else:
            time.sleep(0.1)


# ---------------- KEYBOARD LISTENER ----------------
def on_key_press(key):
    global clicking, click_key, listening_for_key

    try:
        key_char = key.char.lower()
    except AttributeError:
        key_char = str(key)

    if listening_for_key:
        set_keybind(key_char)
        return

    if key_char == click_key:
        toggle_clicking()


# ---------------- MOUSE LISTENER ----------------
def on_mouse_click(x, y, button, pressed):
    global clicking, click_key, listening_for_key

    if not pressed:
        return

    button_str = str(button)

    if listening_for_key:
        set_keybind(button_str)
        return

    if button_str == click_key:
        toggle_clicking()


# ---------------- KEYBIND SETTER ----------------
def set_keybind(new_key):
    global click_key, listening_for_key
    click_key = new_key

    display_names = {
        "Button.x1": "Mouse Button 4",
        "Button.x2": "Mouse Button 5"
    }

    display = display_names.get(new_key, new_key)
    key_label.config(text=f"Key: {display}")

    listening_for_key = False


# ---------------- GUI FUNCTIONS ----------------
def toggle_clicking():
    global clicking
    clicking = not clicking
    status_label.config(text=f"Status: {'ON' if clicking else 'OFF'}")


def set_key():
    global listening_for_key
    listening_for_key = True
    key_label.config(text="Press any key or mouse button...")


def update_interval(val):
    global interval
    # Logarithmic scaling from 0.001 → 30 seconds
    min_val = 0.001
    max_val = 30
    scale = float(val)

    interval = min_val * (max_val / min_val) ** scale
    interval_label.config(text=f"Interval: {interval:.4f}s")


# ---------------- START LISTENERS ----------------
def start_listeners():
    keyboard_listener = keyboard.Listener(on_press=on_key_press)
    keyboard_listener.daemon = True
    keyboard_listener.start()

    mouse_listener = mouse.Listener(on_click=on_mouse_click)
    mouse_listener.daemon = True
    mouse_listener.start()


# ---------------- GUI SETUP ----------------
root = tk.Tk()
root.title("Auto Clicker")
root.geometry("320x220")

status_label = ttk.Label(root, text="Status: OFF", font=("Arial", 12))
status_label.pack(pady=10)

toggle_button = ttk.Button(root, text="Start / Stop", command=toggle_clicking)
toggle_button.pack(pady=5)

key_label = ttk.Label(root, text=f"Key: {click_key}")  
key_label.pack(pady=5)

set_key_button = ttk.Button(root, text="Set Key", command=set_key)
set_key_button.pack(pady=5)

interval_label = ttk.Label(root, text=f"Interval: {interval}s")
interval_label.pack(pady=5)

interval_slider = ttk.Scale(
    root,
    from_=0,          
    to=1,             
    value=0.5,        
    command=update_interval
)
interval_slider.pack(pady=5, fill="x", padx=20)


# ---------------- THREADS ----------------
thread = threading.Thread(target=auto_click)
thread.daemon = True
thread.start()

start_listeners()

# ---------------- RUN ----------------
root.mainloop()