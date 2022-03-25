#!/usr/bin/python3
from tkinter import Toplevel, CENTER, RIGHT, messagebox, Entry, PhotoImage
from tkinter.ttk import Button, Label
from awesometkinter.bidirender import add_bidi_support, render_text
from os import path
from re import compile

from databaseAPI import DataBase as db
import csv

blacklist_file = path.join("data", "blacklist.csv")

class Block(Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.title("إضافة إسم لقائمة الممنوعين من الدخول")
        self.transient(root)
        # centering the widget
        width = int(self.winfo_screenwidth() / 2)
        height = int(self.winfo_screenheight() / 2)
        x_left = int(self.winfo_screenwidth() / 2 - width / 2)
        y_top = int(self.winfo_screenheight() / 2 - height / 2)
        self.geometry(f"{width}x{height}+{x_left}+{y_top}")
        # creating the entry width for all the entries
        entry_width:int = 40
        # creating the name entry and label
        self.name_entry = Entry(self, width=entry_width)
        self.name_label = Label(self, text=render_text("الأسم:"))
        add_bidi_support(self.name_entry)
        # creating the phone number entry and label
        self.phone_number_entry = Entry(self, width=entry_width)
        self.phone_number_label = Label(self, text=render_text("رقم الهاتف:"))
        add_bidi_support(self.phone_number_entry)
        # creating the blocking reason entry and label
        self.blocking_reason_entry = Entry(self, width=entry_width)
        self.blocking_reason_label = Label(self, text=render_text("سبب الحظر:"))
        add_bidi_support(self.blocking_reason_entry)
        # Creating the block button
        self.block_icon = PhotoImage(file=path.join("imgs","block16.png"))
        self.block_btn = Button(self, text=render_text("حظر"),
                                image=self.block_icon, compound=RIGHT, command=self.blockGuest)
        # the distance from the left for the label and the entry
        relx_label:float = 0.7
        relx_entry:float = 0.4
        # putting things on the screen
        self.name_label.place(relx=relx_label, rely=0.2, anchor="w")
        self.name_entry.place(relx=relx_entry, rely=0.2, anchor=CENTER)
        self.phone_number_label.place(relx=relx_label, rely=0.4, anchor="w")
        self.phone_number_entry.place(relx=relx_entry, rely=0.4, anchor=CENTER)
        self.blocking_reason_label.place(relx=relx_label, rely=0.6, anchor="w")
        self.blocking_reason_entry.place(relx=relx_entry, rely=0.6, anchor=CENTER)
        self.block_btn.place(relx=0.5, rely=0.8, anchor=CENTER)

    def blockGuest(self):
        guest_data = {
            'name': self.name_entry.get(),
            'phone_number': self.phone_number_entry.get(),
            'blocking_reason': self.blocking_reason_entry.get()
        }
        if self.invalidInputs(guest_data): return
        if self.duplicateName(guest_data): return
        if not self.confirmationMssg(): return
        with open(blacklist_file, 'a') as blacklist:
            wrtiter = csv.DictWriter(blacklist, fieldnames=guest_data.keys())
            wrtiter.writerows([guest_data])
            print("data written")
        # These two line are used to close the Toplevel()
        self.destroy()
        self.update()

    def confirmationMssg(self) -> bool:
        return messagebox.askyesno("هل تريد إضافة الإسم فعلاً",
                                    render_text(f"""هل تريد فعلاً إضافة
                                    {self.name_entry.get()}
                                    إلى قائمة الحظر؟"""),
                                    parent=self)

    def duplicateName(self, guest_data:dict) -> bool:
        '''
        This helper function checks if the name we are trying to add to the blacklist
        exists in the blacklist already or not.
        '''
        with open(blacklist_file, 'r') as blacklist:
            reader = csv.reader(blacklist)
            for line in reader:
                if line == list(guest_data.values()):
                    messagebox.showinfo("الإسم موجود بالفعل",
                            f"الإسم موجود بالفعل في قائمة الحظر!",
                            parent=self)
                    return True
        return False

    def invalidInputs(self, guest_data:dict) -> bool:
        '''
        This is a helper function to check if there is an empty input field or wrong inputs
        '''
        # checking for empty fields
        if '' in list(guest_data.values()):
            messagebox.showwarning("البيانات ناقصة",
                                    render_text("برجاء إكمال كافة البيانات"),
                                    parent=self)
            return True
        # checking the validity of the phone number field, the number must be an egyptian phone number
        phone_number = guest_data["phone_number"]
        number_re = compile(r"^01[0-2,5]\d{8}")
        if number_re.match(phone_number) is None:
            messagebox.showwarning("خطأ في رقم الهاتف",
                                    render_text("الرجاء إدخال رقم هاتف صحيح!"),
                                    parent=self)
            return True
        return False