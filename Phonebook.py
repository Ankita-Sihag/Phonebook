from tkinter import *
from tkinter import messagebox
import sqlite3
from Add_Contact import AddContact
from Edit_Contact import EditContact

con = sqlite3.connect('database.txt')
cur = con.cursor()


class Phonebook:
    def __init__(self, master):
        self.master = master

        # top frame
        self.top_frame = Frame(master, bg="white")
        self.top_frame.pack(fill=X)

        # top image
        self.top_image = PhotoImage(file="Phonebook.png").subsample(x=7, y=7)
        self.top_image_label = Label(self.top_frame, image=self.top_image, bg="white")
        self.top_image_label.grid(row=0, column=0, padx=50, pady=10)

        # heading
        self.heading = Label(self.top_frame, text="My Phonebook", font="Gabriola 30 bold", bg="white", fg="blue")
        self.heading.grid(row=0, column=1, pady=10)

        # bottom frame
        self.bottom_frame = Frame(master, height=450, bg="powder blue")
        self.bottom_frame.pack(pady=5, fil=X)

        # list frame
        self.list_frame = Frame(self.bottom_frame, height=450, bg="powder blue")
        self.list_frame.grid(row=0, column=0)

        self.scroll = Scrollbar(self.list_frame, orient=VERTICAL)
        self.listbox = Listbox(self.list_frame, width=24, height=15, bd=10, relief="ridge", selectmode=SINGLE,
                               font="Calibri 14")
        self.listbox.grid(row=0, column=0, padx=(10, 0))
        self.listbox.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.listbox.yview)
        self.scroll.grid(row=0, column=1, sticky="ns")

        # filling the list
        people = cur.execute("select * from phonebook order by name").fetchall()
        for person in people:
            self.listbox.insert(END, "  " + person[0])

        self.listbox.bind('<<ListboxSelect>>', self.display_details)

        # details frame
        self.details_frame = Frame(self.bottom_frame, height=450, bg="powder blue")
        self.details_frame.grid(row=0, column=1, padx=(10, 0))

        # name
        self.name_pic = PhotoImage(file="User.png").subsample(x=25, y=25)
        self.name_pic_label = Label(image=self.name_pic, bg="powder blue")
        self.name_pic_label.grid(row=0, column=0, pady=4, in_=self.details_frame)
        self.name_pic_label.lower(self.details_frame)
        self.name_label = Label(self.details_frame, text="", font="Calibri 15", bg="powder blue")
        self.name_label.grid(row=0, column=1, pady=4)

        # phone 1
        self.phone_pic = PhotoImage(file="Phone.png").subsample(x=4, y=4)
        self.phone1_pic_label = Label(image=self.phone_pic, bg="powder blue")
        self.phone1_pic_label.grid(row=1, column=0, pady=4, in_=self.details_frame)
        self.phone1_pic_label.lower(self.details_frame)
        self.phone1_label = Label(self.details_frame, text="", font="Calibri 15", bg="powder blue")
        self.phone1_label.grid(row=1, column=1, pady=4)

        # phone 2
        self.phone2_pic_label = Label(image=self.phone_pic, bg="powder blue")
        self.phone2_pic_label.grid(row=2, column=0, pady=4, in_=self.details_frame)
        self.phone2_pic_label.lower(self.details_frame)
        self.phone2_label = Label(self.details_frame, text="", font="Calibri 15", bg="powder blue")
        self.phone2_label.grid(row=2, column=1, pady=4)

        # email
        self.email_pic = PhotoImage(file="Email.png").subsample(x=25, y=25)
        self.email_pic_label = Label(image=self.email_pic, bg="powder blue")
        self.email_pic_label.grid(row=3, column=0, pady=4, in_=self.details_frame)
        self.email_pic_label.lower(self.details_frame)
        self.email_label = Label(self.details_frame, text="", font="Calibri 15", bg="powder blue")
        self.email_label.grid(row=3, column=1, pady=4)

        # edit button
        self.edit_button = Button(text="Edit", font="Tahoma 15", width=6, bd=4, relief="groove",
                                  command=self.edit_function)
        self.edit_button.grid(row=4, column=0, pady=12, padx=2, in_=self.details_frame)
        self.edit_button.lower(self.details_frame)

        # delete button
        self.delete_button = Button(text="Delete", font="Tahoma 15", width=6, bd=4, relief="groove",
                                    command=self.delete_function)
        self.delete_button.grid(row=4, column=1, pady=12, padx=2, in_=self.details_frame)
        self.delete_button.lower(self.details_frame)

        # Add button
        self.add_btn = Button(self.details_frame, text="Add", width=10, font="Tahoma 15", bg="white", fg="blue", bd=3,
                              relief="raised", command=self.add_function)
        self.add_btn.grid(row=5, column=0, columnspan=2, pady=(50, 0))

    def add_function(self):
        add_page = AddContact(self.listbox)

    def display_details(self, event):
        try:
            # get name of the selected person
            widget = event.widget
            selection = widget.curselection()
            person_name = widget.get(selection[0])
            person_name = person_name[2:]

            # get all the data
            query = "select * from phonebook where name='{}'".format(person_name)
            data = cur.execute(query).fetchone()

            # name
            self.name_label.config(text=data[0])
            self.name_pic_label.lift(self.details_frame)

            # phone1
            self.phone1_label.config(text=data[1])
            self.phone1_pic_label.lift(self.details_frame)

            # phone2
            if data[2] is not None:
                self.phone2_pic_label.lift(self.details_frame)
                self.phone2_label.config(text=data[2])
            else:
                self.phone2_pic_label.lower(self.details_frame)
                self.phone2_label.config(text="")

            # email
            if data[3] is not None:
                self.email_pic_label.lift(self.details_frame)
                self.email_label.config(text=data[3])
            else:
                self.email_pic_label.lower(self.details_frame)
                self.email_label.config(text="")

            # buttons
            self.delete_button.lift(self.details_frame)
            self.edit_button.lift(self.details_frame)
        except:
            pass

    def edit_function(self):
        # get the old data
        name = self.name_label['text']
        phone1 = self.phone1_label['text']
        phone2 = self.phone2_label['text']
        email = self.email_label['text']
        edit_page = EditContact(self.listbox, name, phone1, phone2, email)

        # make the details label invisible
        self.name_label.config(text="")
        self.phone1_label.config(text="")
        self.phone2_label.config(text="")
        self.email_label.config(text="")
        self.name_pic_label.lower(self.details_frame)
        self.phone1_pic_label.lower(self.details_frame)
        self.phone2_pic_label.lower(self.details_frame)
        self.email_pic_label.lower(self.details_frame)
        self.delete_button.lower(self.details_frame)
        self.edit_button.lower(self.details_frame)

    def delete_function(self):
        name = self.name_label['text']
        answer = messagebox.askyesno("Phonebook", "Are you sure you want to delete the contact '" + name + "'")
        if not answer:
            return
        try:
            # delete from database
            query = "delete from phonebook where name='{}'".format(name)
            cur.execute(query)
            con.commit()

            # delete from listbox
            selected_index = self.listbox.curselection()
            self.listbox.delete(selected_index)

            # make the detail labels invisible
            self.name_label.config(text="")
            self.phone1_label.config(text="")
            self.phone2_label.config(text="")
            self.email_label.config(text="")
            self.name_pic_label.lower(self.details_frame)
            self.phone1_pic_label.lower(self.details_frame)
            self.phone2_pic_label.lower(self.details_frame)
            self.email_pic_label.lower(self.details_frame)
            self.delete_button.lower(self.details_frame)
            self.edit_button.lower(self.details_frame)
        except:
            messagebox.showerror("Phonebook", "Error occurred !!")


# create table in database
query = "CREATE TABLE IF NOT EXISTS phonebook (name text PRIMARY KEY, phone1 text UNIQUE, phone2 text UNIQUE, email text );"
cur.execute(query)
con.commit()

root = Tk()
app = Phonebook(root)
root.title('Phonebook')
root.geometry("550x500+100+20")
root.resizable(False, False)
root.config(background="powder blue")

root.mainloop()
