from collections import namedtuple
from datetime import datetime, timedelta
import tkinter as tk
import sqlite3
from .util import resize_window
from .main_portal import MainPortal

STANDARD_HOLD_PERIOD = 14
DATABASE_NAME = "library.sqlite3"

class PlaceHoldFrame(tk.Frame):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.base.title("Place Hold")

        self.connection = sqlite3.connect(DATABASE_NAME)
        resize_window(base)
        tk.Button(self, text="Home", command=self.return_home).pack()

        self.book_var = tk.StringVar(self)
        self.user_var = tk.StringVar(self)
        self.response_message = tk.StringVar(self)
        self.book_options_var = tk.StringVar(self)
        self.book_options_var.trace('w', self.on_book_selected)
        self.user_options_var = tk.StringVar(self)
        self.user_options_var.trace('w', self.on_user_selected)

        lframe = tk.LabelFrame(self, text="Placing Holds Screen")
        
        uid = tk.LabelFrame(lframe,  text="User")
        user_entry = tk.Entry(uid, textvariable=self.user_var)
        user_entry.pack(expand=True, fill=tk.X)

        uf2 = tk.Frame(uid)
        tk.Button(uf2, text="Validate", command=self.validate_user).pack(side=tk.LEFT)
        self.user_options = tk.OptionMenu(uf2, self.user_options_var, [])
        self.user_options.pack(side=tk.LEFT, expand=True, fill=tk.X)
        uf2.pack(fill=tk.X)
        uid.pack(expand=True, fill=tk.X, ipadx=10, ipady=10)

        bid = tk.LabelFrame(lframe,  text="Book")
        book_entry = tk.Entry(bid, textvariable=self.book_var)
        book_entry.pack(expand=True, fill=tk.X)
         # wouldn't using scope be a useful thing here???

        bf2 = tk.Frame(bid)
        tk.Button(bf2, text="Validate", command=self.validate_book).pack(side=tk.LEFT)
        self.book_options = tk.OptionMenu(bf2, self.book_options_var, [])
        self.book_options.pack(side=tk.LEFT, expand=True, fill=tk.X)
        bf2.pack(fill=tk.X)
        bid.pack(expand=True, fill=tk.X, ipadx=10, ipady=10)
        
        tk.Button(lframe, text="Submit", command=self.place_hold).pack()
        lframe.pack(padx=10, pady=10, ipadx=10, ipady=10)

        tk.Label(self, text="", textvariable=self.response_message).pack()
        self.pack(expand=True, fill=tk.BOTH)
        user_entry.bind("<Return>", self.handle_enter_user)
        book_entry.bind("<Return>", self.handle_enter_book)

    def place_hold(self):
        Hold = namedtuple('Hold', ['book_id', 'patron_id', 'date_created', 'date_expires'])
        self.response_message.set("")
        text_user = self.user_var.get().strip()
        text_book = self.book_var.get().strip()
        self.user_var.set("")
        self.book_var.set("")
        searched_name = self.book_options_var.get()
        print("Searched name: ", searched_name)

        if len(text_user) == 0:
            return

        book_id = text_book
        user_id = int(text_user)

        c = self.connection.cursor()
        c.execute("""
            SELECT * 
            From Hold
            WHERE BookID = ? AND PatronID = ?;
        """, [book_id, user_id])
        search_result = c.fetchone()
        current_date = datetime.now().date()
        expiry_date = current_date + timedelta(days=STANDARD_HOLD_PERIOD)
        if search_result is None:
            print("No holds found")
            hold = Hold(book_id, user_id, current_date, expiry_date)
            c.execute("""
                INSERT INTO Hold
                    (BookID, PatronID, DateCreated, DateExpires)
                VALUES
                    (?, ?, ?, ?);
            """, [text_book, int(text_user), current_date, expiry_date])
            self.response_message.set(f"Placed hold that will expire: {expiry_date}")
            print(f"Placed new hold: {hold}")
        else:
            hold = Hold(search_result)
            print("Found existing hold: ", hold)
            hold.date_expires = expiry_date
            c.execute("""
                UPDATE Hold
                SET
                    DateExpires = ?
                WHERE BookID = ? AND PatronID = ?;
            """, [expiry_date, hold.book_id, hold.patron_id])
            self.response_message.set(f"Updated hold: {hold}")

    def validate_book(self):
        b_query = self.book_var.get().strip()
        if len(b_query) == 0:
            return
        if ';' in b_query:
            return
        c = self.connection.cursor()
        statement = f"SELECT * FROM Book WHERE Title LIKE '%{b_query}%';"
        print("Statement:", statement)
        c.execute(statement)
        found = c.fetchall()
        c.close()
        print(f"Results: {found}")
        menu = self.book_options["menu"]
        menu.delete(0, "end")
        self.book_options_var.set("")
        for row in found:
            menu.add_command(\
                label=str(row[1]),\
                command=lambda value = row[1]: self.book_options_var.set(value) \
                )
    def on_book_selected(self, *args):
        c = self.connection.cursor()
        q_value = self.book_options_var.get()
        c.execute("SELECT ID FROM Book WHERE Title=?;", [q_value])
        book_id =  c.fetchone()
        if not book_id is None:
            self.book_var.set(book_id[0])
        print("Got bookid from selection: ", book_id)
    
    def on_user_selected(self, *args):
        c = self.connection.cursor()
        q_value = self.user_options_var.get()
        c.execute("SELECT ID FROM Patron WHERE Name=?;", [q_value])
        user_id =  c.fetchone()
        if not user_id is None:
            self.user_var.set(user_id[0])
        print("Got userid from selection: ", user_id)


    def validate_user(self):
        user_query = self.user_var.get().strip()
        if len(user_query) == 0:
            return
        if ';' in user_query:
            return
        c = self.connection.cursor()
        statement = f"SELECT * FROM Patron WHERE Name LIKE '%{user_query}%';"
        print("Statement:", statement)
        c.execute(statement)
        found = c.fetchall()
        c.close()
        print(f"Results: {found}")
        menu = self.user_options["menu"]
        menu.delete(0, "end")
        self.user_options_var.set("")
        for row in found:
            menu.add_command(\
                label=str(row[1]),\
                command=lambda value = row[1]: self.user_options_var.set(value) \
                )

    
    def handle_enter_book(self, _event):
        self.validate_book()

    def handle_enter_user(self, _event):
        self.validate_user()


    def return_home(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.connection.commit()
        self.connection.close()
        self.unbind("<Return>")
        self.destroy()
        MainPortal(self.base)


if __name__ == "__main__":
    root = tk.Tk()
    root.eval('tk::PlaceWindow . center')
    PlaceHoldFrame(root)
    root.mainloop()