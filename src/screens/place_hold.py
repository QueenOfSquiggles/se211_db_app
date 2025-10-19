from collections import namedtuple
from datetime import datetime, timedelta
import tkinter as tk
import sqlite3
from .util import resize_window
from .main_portal import MainPortal

STANDARD_HOLD_PERIOD = 14

class PlaceHoldFrame(tk.Frame):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.base.title("Place Hold")
        self.connection = sqlite3.connect("db")
        resize_window(base)
        tk.Button(self, text="Home", command=self.return_home).pack()

        self.book_var = tk.StringVar()
        self.user_var = tk.StringVar()
        self.response_message = tk.StringVar()

        lframe = tk.LabelFrame(self, text="Placing Holds Screen")
        
        user_frame = tk.Frame(lframe)
        tk.Label(user_frame, text="User ID").pack(side=tk.LEFT)
        user_entry = tk.Entry(user_frame, textvariable=self.user_var)
        user_entry.pack(side=tk.LEFT)
        user_frame.pack()

        book_frame = tk.Frame(lframe)
        tk.Label(book_frame, text="Book ID").pack(side=tk.LEFT)
        book_entry = tk.Entry(book_frame, textvariable=self.book_var)
        book_entry.pack(side=tk.LEFT)
        book_frame.pack() # wouldn't using scope be a useful thing here???
        
        tk.Button(lframe, text="Submit", command=self.place_hold).pack()
        lframe.pack(padx=10, pady=10, ipadx=10, ipady=10)

        tk.Label(self, text="", textvariable=self.response_message).pack()
        self.pack()
        user_entry.bind("<Return>", self.handle_enter)
        book_entry.bind("<Return>", self.handle_enter)
    
    def place_hold(self):
        Hold = namedtuple('Hold', ['book_id', 'patron_id', 'date_created', 'date_expires'])
        self.response_message.set("")
        text_user = self.user_var.get().strip()
        text_book = self.book_var.get().strip()
        self.user_var.set("")
        self.book_var.set("")

        book_id = text_book
        user_id = int(text_user)

        c = self.connection.cursor()
        c.execute("""
            SELECT * 
            From Hold
            WHERE BookID = ? AND PatronID = ?;
        """, [book_id, user_id])
        hold = Hold(c.fetchone())
        current_date = datetime.now().date()
        expiry_date = current_date + timedelta(days=STANDARD_HOLD_PERIOD)
        if hold is None:
            print("No holds found")
            c.execute("""
                INSERT INTO Hold
                    (BookID, PatronID, DateCreated, DateExpires)
                VALUES
                    (?, ?, ?, ?);
            """, [text_book, int(text_user), current_date, expiry_date])
            self.response_message.set(f"Placed hold that will expire: {expiry_date}")
        else:
            print("Found existing hold: ", hold)
            c.execute("""
                UPDATE Hold
                SET
                    DateExpires = ?
                WHERE BookID = ? AND PatronID = ?;
            """, [expiry_date, hold.book_id, hold.patron_id])
            self.response_message.set(f"Updated hold that will expire: {expiry_date}")



    
    def handle_enter(self, _event):
        self.place_hold()


    def return_home(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.connection.close()
        self.unbind("<Return>")
        self.destroy()
        MainPortal(self.base)

if __name__ == "__main__":
    root = tk.Tk()
    root.eval('tk::PlaceWindow . center')
    PlaceHoldFrame(root)
    root.mainloop()