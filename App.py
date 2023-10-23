import tkinter as tk
from Controller import Controller

class App:
    def __init__(self):
        self.controller = Controller()
        self.controller.root.mainloop()

# Start the app
app = App()
