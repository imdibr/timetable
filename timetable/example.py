import tkinter as tk
from tkinter import filedialog
import pandas as pd
from threading import Thread

root = tk.Tk()
menubar = tk.Menu(root)
root.config(menu= menubar)
subMenu = tk.Menu(menubar, tearoff=0)

def browse_file():
    filename = filedialog.askopenfilename()
    df = pd.read_excel(filename)
    #whatever you need to do with your df...

menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=lambda: Thread(target=browse_file).start())

root.geometry("600x600")
root.mainloop()