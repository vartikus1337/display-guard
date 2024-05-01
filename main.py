#!/usr/bin/env python3

import imageio, os
from tkinter import Tk, ttk

PASSWORD = '123'

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('Protect by PashaCoder')
        self.geometry('555x555')
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_leave)
        self.bind('<Control_L>', self.on_leave)
        self.bind('<Alt_L>', self.on_leave)
        self.bind('<Return>', self.on_leave)

        self.frame = ttk.Frame(self)
        self.frame.bind('<Leave>', self.on_leave)

        self.entry = ttk.Entry(self.frame)
        self.entry.pack(anchor='center', pady=200)

        self.frame.pack(expand=True, fill='both', anchor='center')

  
    def on_leave(self, *args):
        if self.entry.get() == PASSWORD:
            self.destroy()
        else:
            self.protect_photo()
            os.system("systemctl suspend")

  
    def protect_photo(self):
        reader = imageio.get_reader('<video0>')
        frame = reader.get_next_data()
        imageio.imwrite('protect_photo.png', list(frame))
        reader.close()


if __name__ == "__main__":
    app = App()
    app.mainloop()
  
