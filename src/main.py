import os
# import tkinter as tk
from os import path
import tkinter as tk
from screens import main_portal
from initialize import init

if not path.isfile("db"):
    # Initialize database
    init()

if path.isfile("db"):
    print("WARNING! DELETING DATABASE FOR TESTING PURPOSES REMOVE THIS CODE ONCE TESTING COMPLETED")
    os.remove("db")

root = tk.Tk()
root.eval('tk::PlaceWindow . center')
main_portal.MainPortal(root)
root.mainloop()
