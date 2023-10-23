import tkinter as tk
import math

class Knob:
    def __init__(self, root, row, column, num_steps, labels=None):
        self.NUM_STEPS = num_steps  # Number of discrete steps
        self.STEP_ANGLE = 360 / self.NUM_STEPS  # Angle between each step

        self.canvas = tk.Canvas(root, width=40, height=40, bg="systemTransparent")
        self.canvas.grid(row=row, column=column)
        self.oval = self.canvas.create_oval(6, 6, 40, 40, fill='white', outline='black', width=2)
        self.canvas.itemconfig(self.oval, fill='white')
        self.needle = self.canvas.create_line(1, 1, 1, 10, width=2, fill='black')

        self.labels = labels
        self.linked_var = [0]

        self.linked_var_value = tk.StringVar()
        self.update_label()

        self.label = tk.Label(root, textvariable=self.linked_var_value)
        self.label.grid(row=row, column=column-1, padx=0, pady=10, sticky=tk.E)

        self.step = 0
        self.canvas.bind('<B1-Motion>', self.rotate_knob)
    
    def rotate_knob(self, event):
        x = self.canvas.winfo_width() / 2
        y = self.canvas.winfo_height() / 2
        dx = event.x - x
        dy = event.y - y
        angle = math.atan2(dy, dx)
        angle = math.degrees(angle)
        decimal_step = angle/self.STEP_ANGLE
        self.linked_var[0] = int(decimal_step) if decimal_step >= 0 else int(self.NUM_STEPS/2) + int(decimal_step) + (int(self.NUM_STEPS/2) - 1)
        self.update_label()
        self.canvas.coords(self.needle, x, y, x + 18 * math.cos(math.radians(angle)), y + 18 * math.sin(math.radians(angle)))

    def link_var(self, wrapper):
        self.linked_var = wrapper

    def update_label(self):
        if self.labels != None:
            value = self.linked_var[0]
            self.linked_var_value.set(self.labels[value])
        else:
            self.linked_var_value.set(self.linked_var[0]) # if no labels put the plain value