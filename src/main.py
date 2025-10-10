from os import path
import tkinter as tk
from screens import main_portal
from initialize import init

DATABASE_NAME = "library.sqlite3"


if not path.isfile(DATABASE_NAME):
    # Initialize database
    init()

root = tk.Tk()
root.eval('tk::PlaceWindow . center')
main_portal.MainPortal(root)
root.mainloop()
