from os import path
import tkinter as tk
from screens import main_portal
from initialize import init

if not path.isfile("db"):
    # Initialize database
    init()

root = tk.Tk()
root.eval('tk::PlaceWindow . center')
main_portal.MainPortal(root)
root.mainloop()
