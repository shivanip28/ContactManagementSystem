from tkinter import *
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox

root = Tk()
root.title("Contact List")
width = 700
height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.config(bg="#20B2AA")

#============================VARIABLES===================================

FIRSTNAME = StringVar()
LASTNAME = StringVar()
CONTACT = StringVar()
OTHER = StringVar()
CITY = StringVar()

#============================FUNCTIONS=====================================

def Database():
    conn = sqlite3.connect("project.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS 'contactsystem' (mem_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT, contact TEXT, other TEXT, city TEXT)")
    cursor.execute("SELECT * FROM 'contactsystem' ORDER BY 'firstname' COLLATE NOCASE ASC") 
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

def SubmitData():
    a =  CONTACT.get()
    if  FIRSTNAME.get() == "" or LASTNAME.get() == "" or CONTACT.get() == "":
        result = tkMessageBox.showwarning('', 'Please Complete The Required Field', icon="warning")
    elif not a.isdigit() or len(a) < 10   :
        result = tkMessageBox.showwarning('', 'Please enter a valid contact number', icon="warning")
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("project.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO `contactsystem` (firstname, lastname, contact, other, city) VALUES(?, ?, ?, ?, ?)", (str(FIRSTNAME.get()), str(LASTNAME.get()), str(CONTACT.get()), str(OTHER.get()), str(CITY.get())))
        conn.commit()
        cursor.execute("SELECT * FROM `contactsystem` ORDER BY `firstname` COLLATE NOCASE ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()

        FIRSTNAME.set("")
        LASTNAME.set("")
        CONTACT.set("")
        OTHER.set("")
        CITY.set("")

        NewWindow.destroy()


def UpdateData():
    a =  CONTACT.get()
    if  FIRSTNAME.get() == "" or LASTNAME.get() == "" or CONTACT.get() == "":
        result = tkMessageBox.showwarning('', 'Please Complete The Required Field', icon="warning")
    elif not a.isdigit() or len(a) < 10   :
        result = tkMessageBox.showwarning('', 'Please enter a valid contact number', icon="warning")
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("project.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE `contactsystem` SET `firstname` = ?, `lastname` = ?, `contact` = ?, `other` = ?, `city` = ? WHERE `mem_id` = ?", (str(FIRSTNAME.get()), str(LASTNAME.get()), str(CONTACT.get()), str(OTHER.get()), str(CITY.get()), int(mem_id)))
        conn.commit()
        cursor.execute("SELECT * FROM `contactsystem` ORDER BY `firstname` COLLATE NOCASE ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()

        FIRSTNAME.set("")
        LASTNAME.set("")
        CONTACT.set("")
        OTHER.set("")
        CITY.set("")

        UpdateWindow.destroy()    
    
def OnSelected(event):
    global mem_id, UpdateWindow
    curItem = tree.focus()
    contents =(tree.item(curItem))
    selecteditem = contents['values']
    mem_id = selecteditem[0]
    FIRSTNAME.set("")
    LASTNAME.set("")
    CONTACT.set("")
    OTHER.set("")
    CITY.set("")

    FIRSTNAME.set(selecteditem[1])
    LASTNAME.set(selecteditem[2])
    CONTACT.set(selecteditem[3])
    OTHER.set(selecteditem[4])
    CITY.set(selecteditem[5])
    
    UpdateWindow = Toplevel()
    UpdateWindow.title("Update  Contact")
    width = 400
    height = 350
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width/2) + 450) - (width/2)
    y = ((screen_height/2) + 20) - (height/2)
    UpdateWindow.resizable(0, 0)
    UpdateWindow.config(bg="pink")
    UpdateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'NewWindow' in globals():
        NewWindow.destroy()

    #===================FRAMES==============================

    FormTitle = Frame(UpdateWindow, bg="pink")
    FormTitle.pack(side=TOP)
    ContactForm = Frame(UpdateWindow, bg="pink")
    ContactForm.pack(side=TOP, pady=10)

    #===================UPDATING LABELS==============================

    lbl_title = Label(FormTitle, text="Updating Contacts", font=('verdana', 14, "bold"), bg="#20B2AA",  width = 300)
    lbl_title.pack(fill=X, pady=15)
    lbl_firstname = Label(ContactForm, text="Firstname*", font=('arial', 14), bd=5, bg="pink")
    lbl_firstname.grid(row=0, sticky=W)
    lbl_lastname = Label(ContactForm, text="Lastname*", font=('arial', 14), bd=5, bg="pink")
    lbl_lastname.grid(row=1, sticky=W)
    lbl_contact = Label(ContactForm, text="Contact_1*", font=('arial', 14), bd=5, bg="pink")
    lbl_contact.grid(row=2, sticky=W)
    lbl_other = Label(ContactForm, text="Contact_2", font=('arial', 14), bd=5, bg="pink")
    lbl_other.grid(row=3, sticky=W)
    lbl_city = Label(ContactForm, text="City/State", font=('arial', 14), bd=5, bg="pink")
    lbl_city.grid(row=4, sticky=W)

    #===================UPDATING ENTRY===============================

    firstname = Entry(ContactForm, textvariable=FIRSTNAME, font=('arial', 14), borderwidth=3, relief="sunken")
    firstname.grid(row=0, column=1, pady=5)
    lastname = Entry(ContactForm, textvariable=LASTNAME, font=('arial', 14), borderwidth=3, relief="sunken")
    lastname.grid(row=1, column=1, pady=5)
    contact = Entry(ContactForm, textvariable=CONTACT,  font=('arial', 14), borderwidth=3, relief="sunken")
    contact.grid(row=2, column=1, pady=5)
    other = Entry(ContactForm, textvariable=OTHER,  font=('arial', 14), borderwidth=3, relief="sunken")
    other.grid(row=3, column=1, pady=5)
    city = Entry(ContactForm, textvariable=CITY,  font=('arial', 14), borderwidth=3, relief="sunken")
    city.grid(row=4, column=1, pady=5) 

    #================== UPDATE BUTTON==============================

    btn_updatecon = Button(ContactForm, text="Update", width=15, command=UpdateData, cursor="hand2", font=("verdana", 11, "bold"), bd=5)
    btn_updatecon.grid(row=6, columnspan=2, pady=10)
  
def DeleteData():
    if not tree.selection():
       result = tkMessageBox.showwarning('', 'Please Select Something First!', icon="warning")
    else:
        result = tkMessageBox.askquestion('', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            conn = sqlite3.connect("project.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM `contactsystem` WHERE `mem_id` = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()
    
def AddNewWindow():
    global NewWindow
    FIRSTNAME.set("")
    LASTNAME.set("")
    CONTACT.set("")
    OTHER.set("")
    CITY.set("")

    NewWindow = Toplevel()
    NewWindow.title("Contact List")
    width = 400
    height = 350
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width/2) - 455) - (width/2)
    y = ((screen_height/2) + 20) - (height/2)
    NewWindow.resizable(0, 0)
    NewWindow.config(bg="BurlyWood")

    NewWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'UpdateWindow' in globals():
        UpdateWindow.destroy()
    
    #===================FRAMES==============================

    FormTitle = Frame(NewWindow, bg="BurlyWood")
    FormTitle.pack(side=TOP)
    ContactForm = Frame(NewWindow, bg="BurlyWood")
    ContactForm.pack(side=TOP, pady=10)
    
    #===================NEW CONTACT LABELS==============================

    lbl_title = Label(FormTitle, text="Adding New Contacts", font=('verdana', 14, "bold"), bg="#20B2AA",  width = 300)
    lbl_title.pack(fill=X, pady=15)
    lbl_firstname = Label(ContactForm, text="Firstname*", font=('arial', 14), bd=5, bg="BurlyWood")
    lbl_firstname.grid(row=0, sticky=W)
    lbl_lastname = Label(ContactForm, text="Lastname*", font=('arial', 14), bd=5, bg="BurlyWood")
    lbl_lastname.grid(row=1, sticky=W)
    lbl_contact = Label(ContactForm, text="Contact_1*", font=('arial', 14), bd=5, bg="BurlyWood")
    lbl_contact.grid(row=2, sticky=W)
    lbl_other = Label(ContactForm, text="Contact_2", font=('arial', 14), bd=5, bg="BurlyWood")
    lbl_other.grid(row=3, sticky=W)
    lbl_city = Label(ContactForm, text="City/State", font=('arial', 14), bd=5, bg="BurlyWood")
    lbl_city.grid(row=4, sticky=W)

    #===================NEW CONTACT ENTRY===============================

    firstname = Entry(ContactForm, textvariable=FIRSTNAME, font=('arial', 14), borderwidth=3, relief="sunken")
    firstname.grid(row=0, column=1, pady=5)
    lastname = Entry(ContactForm, textvariable=LASTNAME, font=('arial', 14), borderwidth=3, relief="sunken")
    lastname.grid(row=1, column=1, pady=5)
    contact = Entry(ContactForm, textvariable=CONTACT,  font=('arial', 14), borderwidth=3, relief="sunken")
    contact.grid(row=2, column=1, pady=5)
    other = Entry(ContactForm, textvariable=OTHER,  font=('arial', 14), borderwidth=3, relief="sunken")
    other.grid(row=3, column=1, pady=5)
    city = Entry(ContactForm, textvariable=CITY,  font=('arial', 14), borderwidth=3, relief="sunken")
    city.grid(row=4, column=1, pady=5) 

    #==================SAVE BUTTON==============================

    btn_addcon = Button(ContactForm, text="Save", width=15, command=SubmitData, cursor="hand2",bd=5, font=("verdana", 11, "bold"))
    btn_addcon.grid(row=5, columnspan=2, pady=15)
    
#============================FRAMES======================================

Top = Frame(root, width=500, bd=1, relief=SOLID)
Top.pack(side=TOP)
Mid = Frame(root, width=500,  bg="#20B2AA")
Mid.pack(side=TOP)
MidLeft = Frame(Mid, width=100)
MidLeft.pack(side=LEFT, pady=10)
Middle = Frame(Mid, width=100)
Middle.pack(side=LEFT, pady=10, padx = 30)
MidRight = Frame(Mid, width=100)
MidRight.pack(side=RIGHT, pady=10)
TableMargin = Frame(root, width=500)
TableMargin.pack(side=TOP)

#============================HEADING LABEL======================================

lbl_title = Label(Top, text="Contact Management System", font=("rockwell", 24), width=500, bg="#20B2AA")
lbl_title.pack(fill=X)

#============================ADD NEW AND DELETE BUTTONS=====================================

btn_add = Button(MidLeft, text="+ ADD NEW", bg="white", fg="green", bd= 5, width=10, font=("verdana", 10, "bold"), command=AddNewWindow, cursor="cross")
btn_add.pack()
btn_delete = Button(MidRight, text="- DELETE", bg="white",fg="red", width=10, bd= 5, font=("verdana", 10, "bold"), command=DeleteData, cursor="hand2")
btn_delete.pack(side=RIGHT)
update = Label(Middle, text="Double click on the contact to UPDATE !!", font=("rockwell", 10), padx=10, pady=5)
update.pack()

#============================TABLES======================================

scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("SR_NO", "FIRST_NAME", "LAST_NAME", "CONTACT_1", "CONTACT_2", "CITY/STATE"), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('SR_NO', text="SR_NO", anchor=W)
tree.heading('FIRST_NAME', text="FIRST_NAME", anchor=W)
tree.heading('LAST_NAME', text="LAST_NAME", anchor=W)
tree.heading('CONTACT_1', text="CONTACT_1", anchor=W)
tree.heading('CONTACT_2', text="CONTACT_2", anchor=W)
tree.heading('CITY/STATE', text="CITY/STATE", anchor=W)

style = ttk.Style()
style.theme_use("clam")
style.map("Treeview")
ttk.Style().configure("Treeview.Heading", background = "bisque", foreground="Black", font = ("verdana", 8, "bold"))

tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=0)
tree.column('#2', stretch=NO, minwidth=0, width=120)
tree.column('#3', stretch=NO, minwidth=0, width=120)
tree.column('#4', stretch=NO, minwidth=0, width=100)
tree.column('#5', stretch=NO, minwidth=0, width=100)
tree.column('#6', stretch=NO, minwidth=0, width=100)

tree.pack()
tree.bind('<Double-Button-1>', OnSelected)

#============================INITIALIZATION==============================

if __name__ == '__main__':
    Database()
    root.mainloop()
    
