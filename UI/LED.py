import tkinter as tk

class LED:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LED, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def initialize(self, root):
        self.canvas = tk.Canvas(root, width=20, height=20, bg="systemTransparent")
        self.canvas.grid(row=1, column=1)
        self.led = self.canvas.create_oval(5, 5, 20, 20, fill='black')

    def flash(self, firstBeat):
        self.canvas.itemconfig(self.led, fill='yellow' if firstBeat else 'red') #maybe there is an issue with this being called in the thread of metronome TODO check
        self.canvas.after(100, lambda: self.canvas.itemconfig(self.led, fill='black'))
        
