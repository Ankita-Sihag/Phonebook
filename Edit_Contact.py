from tkinter import *
import sqlite3
from tkinter import messagebox

con = sqlite3.connect('database.txt')
cur = con.cursor()


class EditContact(Toplevel):
    def __init__(self, listbox, name, phone1, phone2, email):
        Toplevel.__init__(self)

        self.geometry("400x410+200+50")
        self.title("Edit Contact")
        self.resizable(False, False)
        self.config(background="powder blue")

        # fetch details from main page
        self.main_page_listbox = listbox
        self.old_name = name
        self.old_phone1 = phone1
        self.old_phone2 = phone2
        self.old_email = email

        # top frame
        self.top_frame = Frame(self, bg="white")
        self.top_frame.pack(fill=X)

        # top image
        self.top_image = PhotoImage(file="Phonebook.png").subsample(x=8, y=8)
        self.top_image_label = Label(self.top_frame, image=self.top_image, bg="white")
        self.top_image_label.grid(row=0, column=0, padx=50, pady=10)

        # heading
        self.heading = Label(self.top_frame, text="Edit Contact", font="Gabriola 24 bold", bg="white", fg="blue")
        self.heading.grid(row=0, column=1, pady=10)

        # bottom frame
        self.bottom_frame = Frame(self, height=450, bg="powder blue")
        self.bottom_frame.pack(pady=(20, 0), fil=X, padx=20)

        # name
        self.name_label = Label(self.bottom_frame, text="Name : ", font="Calibri 18", bg="powder blue")
        self.name_label.grid(row=0, column=0, pady=10)

        self.name_entry = Entry(self.bottom_frame, width=20, bd=4, font="Calibri 18")
        self.name_entry.grid(row=0, column=1)
        self.name_entry.insert(0, self.old_name)

        # phone1
        self.phone1_label = Label(self.bottom_frame, text="Mobile 1 : ", font="Calibri 18", bg="powder blue")
        self.phone1_label.grid(row=1, column=0, pady=10)

        self.phone1_entry = Entry(self.bottom_frame, width=20, bd=4, font="Calibri 18")
        self.phone1_entry.grid(row=1, column=1)
        self.phone1_entry.insert(0, self.old_phone1)

        # phone2
        self.phone2_label = Label(self.bottom_frame, text="Mobile 2 : ", font="Calibri 18", bg="powder blue")
        self.phone2_label.grid(row=2, column=0, pady=10)

        self.phone2_entry = Entry(self.bottom_frame, width=20, bd=4, font="Calibri 18")
        self.phone2_entry.grid(row=2, column=1)
        self.phone2_entry.insert(0, self.old_phone2)

        # email
        self.email_label = Label(self.bottom_frame, text="Email : ", font="Calibri 18", bg="powder blue")
        self.email_label.grid(row=3, column=0, pady=10)

        self.email_entry = Entry(self.bottom_frame, width=20, bd=4, font="Calibri 18")
        self.email_entry.grid(row=3, column=1)
        self.email_entry.insert(0, self.old_email)

        # edit button
        self.edit_button = Button(self.bottom_frame, text="Save", width=10, font="Tahoma 15", bg="white", fg="blue", bd=3, relief="raised", command=self.edit_function)
        self.edit_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.bind('<Return>', self.edit_function)

    def edit_function(self, event=None):
        name = self.name_entry.get()
        phone1 = self.phone1_entry.get()
        phone2 = self.phone2_entry.get()
        if phone2 == "":
            phone2 = None
        email = self.email_entry.get()
        if email == "":
            email = None

        if name and phone1:
            try:
                # check if contact of same name
                query = "select * from phonebook where  name='{}'".format(name)
                data = cur.execute(query).fetchone()
                if data is not None and data[0] != self.old_name:
                    messagebox.showerror("Phonebook", "Contact exists with this name !! ", parent=self)
                    return

                # check if contact with our phone1 already in phone2 column of database
                query = "select * from phonebook where  phone2='{}'".format(phone1)
                data = cur.execute(query).fetchone()
                if data is not None and data[1] != self.old_phone1 and data[1] != self.old_phone2:
                    messagebox.showerror("Phonebook", "Contact exists with the same phone number : "+data[0]+" !!" , parent=self)
                    return

                # check if contact with our phone2 already in phone1 column of database
                if phone2:
                    query = "select * from phonebook where  phone1='{}'".format(phone2)
                    data = cur.execute(query).fetchone()
                    if data is not None and data[2] != self.old_phone1 and data[2] != self.old_phone2:
                        messagebox.showerror("Phonebook", "Contact exists with the same phone number : " + data[0] + " !!" , parent=self)
                        return

                # check if both contacts of this person are same
                if phone1 == phone2:
                    messagebox.showerror("Phonebook", "Both the phone numbers are same !!", parent=self)
                    return

                # delete the old data
                query = "delete from phonebook where name='{}'".format(self.old_name)
                cur.execute(query)
                con.commit()

                # delete from listbox
                selected_index = 0
                for x in range(self.main_page_listbox.size()):
                    if self.main_page_listbox.get(x)[2:] == self.old_name:
                        selected_index = x
                        break
                self.main_page_listbox.delete(selected_index)

                # insert the new data
                query = 'INSERT INTO phonebook (name,phone1,phone2,email) VALUES(?,?,?,?) '
                cur.execute(query, (name, phone1, phone2, email))
                con.commit()

                # insert into listbox
                self.main_page_listbox.insert(0, "  "+name)

                # delete the edit contact page
                self.destroy()

            except:
                messagebox.showerror("Phonebook", "Error Occurred !!", parent=self)
        else:
            messagebox.showerror("Phonebook", "Name and one mobile number is necessary !!", parent=self)
