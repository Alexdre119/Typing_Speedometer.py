import tkinter as tk
from math import cos, sin, pi
import time

class SpeedometerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speedometer")
        self.root.geometry("400x350")

        # Variables
        self.start_time = None
        self.chars_typed = 0

        # Create canvas
        self.canvas = tk.Canvas(root, width=300, height=300, bg="white")
        self.canvas.pack(side=tk.TOP, padx=10, pady=10)

        # Draw speedometer
        self.draw_speedometer()

        # Initialize moving average
        self.moving_average = 0

        # Create entry widget
        self.entry = tk.Entry(root, width=5, font=('Arial', 24))
        self.entry.pack(side=tk.TOP, padx=10, pady=10)
        self.entry.bind('<Key>', self.on_key_press)

        # Schedule periodic update
        self.update_speedometer()

    def on_key_press(self, event):
        char = event.char
        if char and char.isprintable() and len(char) == 1:  # Check if the typed character is printable and is only one character
            self.start_time = time.time()  # Update start time only if it's not set
            self.chars_typed += 1
            self.entry.delete(0, tk.END)  # Clear the entry after typing one character

    def update_speedometer(self):
        # Calculate elapsed time
        if self.start_time:
            elapsed_time = time.time() - self.start_time
        else:
            elapsed_time = 0

        # Calculate CPM
        if elapsed_time > 0:
            cpm = self.chars_typed * 60 / elapsed_time
        else:
            cpm = 0

        # Calculate moving average
        self.moving_average = 0.9 * self.moving_average + 0.1 * cpm

        # Reset chars_typed and start_time if 3 seconds have passed
        if elapsed_time >= 3:
            self.chars_typed = 0
            self.start_time = None

        # Update dial
        angle = 180 + min(cpm / 20, 2000) * 0.09  # 0.09 degrees per CPM
        self.canvas.delete("dial")  # Delete previous dial
        self.canvas.create_line(150, 150, 150 + 100 * cos(angle * pi / 180), 150 + 100 * sin(angle * pi / 180),
                                fill="red", width=2, tags="dial")

        # Schedule next update
        self.root.after(1000, self.update_speedometer)  # Update every 1000 milliseconds (1 second)

    def draw_speedometer(self):
        # Draw circle
        self.canvas.create_arc(50, 50, 250, 250, start=0, extent=180, outline="black", width=2)

        # Draw markings
        for angle in range(180, 361, 45): # Adjusted for 250 CPM increments
            x1 = 150 + 100 * cos(angle * pi / 180)
            y1 = 150 + 100 * sin(angle * pi / 180)  # Flipped y-coordinate
            x2 = 150 + 90 * cos(angle * pi / 180)
            y2 = 150 + 90 * sin(angle * pi / 180)  # Flipped y-coordinate
            self.canvas.create_line(x1, y1, x2, y2, fill="black")

            # Add numbers
            x_text = 150 + 110 * cos(angle * pi / 180)
            y_text = 150 + 110 * sin(angle * pi / 180)  # Flipped y-coordinate
            self.canvas.create_text(x_text, y_text, text=str((360 - angle) * 250 / 45), fill="black")  # Adjusted for 250 CPM increments



# Create the Tkinter application
root = tk.Tk()
app = SpeedometerApp(root)

# Run the application
root.mainloop()

#Need to consider looking at clock apps