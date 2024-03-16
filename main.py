import tkinter as tk
from math import cos, sin, pi
import time

class SpeedometerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speedometer")
        self.root.geometry("300x300")

        # Variables
        self.start_time = None
        self.chars_typed = 0

        # Create canvas
        self.canvas = tk.Canvas(root, width=300, height=300, bg="white")
        self.canvas.pack()

        # Draw speedometer
        self.draw_speedometer()

        # Bind typing event
        self.root.bind('<Key>', self.on_key_press)

    def on_key_press(self, event):
        if not self.start_time:
            self.start_time = time.time()
        self.chars_typed += 1
        self.update_speedometer()

    def update_speedometer(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        if elapsed_time > 0:
            cpm = (self.chars_typed / elapsed_time) * 60
            self.update_dial(cpm)
        else:
            self.start_time = None
            self.chars_typed = 0
            self.update_dial(0)

    def draw_speedometer(self):
        # Draw circle
        self.canvas.create_arc(50, 50, 250, 250, start=0, extent=180, outline="black", width=2)

        # Draw markings
        for angle in range(0, 181, 20):
            x1 = 150 + 100 * cos(angle * pi / 180)
            y1 = 150 - 100 * sin(angle * pi / 180)  # Flipped y-coordinate
            x2 = 150 + 90 * cos(angle * pi / 180)
            y2 = 150 - 90 * sin(angle * pi / 180)  # Flipped y-coordinate
            self.canvas.create_line(x1, y1, x2, y2, fill="black")

            # Add numbers
            x_text = 150 + 110 * cos(angle * pi / 180)
            y_text = 150 - 110 * sin(angle * pi / 180)  # Flipped y-coordinate
            self.canvas.create_text(x_text, y_text, text=str(angle), fill="black")

    def update_dial(self, cpm):
        angle = cpm * 1.8  # 1.8 degrees per CPM
        self.canvas.delete("dial")  # Delete previous dial
        self.canvas.create_line(150, 150, 150 + 100 * cos(angle * pi / 180), 150 - 100 * sin(angle * pi / 180),
                                fill="red", width=2, tags="dial")

# Create the Tkinter application
root = tk.Tk()
app = SpeedometerApp(root)

# Run the application
root.mainloop()
