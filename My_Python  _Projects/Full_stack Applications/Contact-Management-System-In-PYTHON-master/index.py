from tkinter import *
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import os

# --- FILE PATH CONFIGURATION ---
# This ensures the DB is always in the same folder as the .py file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "pythontut.db")

# --- INITIALIZATION ---
root = Tk()
root.title("Contact List")
width = 700
height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width) - (width)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.config(bg="#6666ff")

# --- VARIABLES ---
FIRSTNAME = StringVar()
LASTNAME = StringVar()
GENDER = StringVar()
AGE = StringVar()
ADDRESS = StringVar()
CONTACT = StringVar()
mem_id = None 

# --- DATABASE METHODS ---

def Database():
    # Uses the local DB_PATH
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS member (
                        mem_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                        firstname TEXT, lastname TEXT, gender TEXT, 
                        age TEXT, address TEXT, contact TEXT)""")
    cursor.execute("SELECT * FROM member ORDER BY lastname ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=data)
    cursor.close()
    conn.close()

def RefreshTable():
    tree.delete(*tree.get_children())
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM member ORDER BY lastname ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=data)
    conn.close()

# --- DATA MANIPULATION ---

def SubmitData():
    if not all([FIRSTNAME.get(), LASTNAME.get(), GENDER.get(), AGE.get(), ADDRESS.get(), CONTACT.get()]):
        tkMessageBox.showwarning('', 'Please Complete All Fields', icon="warning")
    else:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO member (firstname, lastname, gender, age, address, contact) VALUES(?, ?, ?, ?, ?, ?)", 
                       (FIRSTNAME.get(), LASTNAME.get(), GENDER.get(), AGE.get(), ADDRESS.get(), CONTACT.get()))
        conn.commit()
        conn.close()
        ClearFields()
        RefreshTable()
        if 'NewWindow' in globals(): NewWindow.destroy()

def UpdateData():
    global mem_id
    if not GENDER.get():
        tkMessageBox.showwarning('', 'Please Select Gender', icon="warning")
    else:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE member SET firstname=?, lastname=?, gender=?, age=?, address=?, contact=? WHERE mem_id=?", 
                       (FIRSTNAME.get(), LASTNAME.get(), GENDER.get(), AGE.get(), ADDRESS.get(), CONTACT.get(), mem_id))
        conn.commit()
        conn.close()
        RefreshTable()
        ClearFields()
        if 'UpdateWindow' in globals(): UpdateWindow.destroy()

def DeleteData():
    if not tree.selection():
        tkMessageBox.showwarning('', 'Please Select A Record First!', icon="warning")
    else:
        result = tkMessageBox.askquestion('', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents = tree.item(curItem)
            selecteditem = contents['values']
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM member WHERE mem_id = ?", (selecteditem[0],))
            conn.commit()
            conn.close()
            tree.delete(curItem)

def ClearFields():
    FIRSTNAME.set("")
    LASTNAME.set("")
    GENDER.set("")
    AGE.set("")
    ADDRESS.set("")
    CONTACT.set("")

# --- UI LOGIC (REUSABLE FORM) ---

def BuildContactForm(window, title_text, btn_command):
    window.geometry("400x350")
    window.resizable(0, 0)
    
    FormTitle = Frame(window)
    FormTitle.pack(side=TOP, fill=X)
    lbl_title = Label(FormTitle, text=title_text, font=('arial', 16), bg="#66ff66" if "Add" in title_text else "orange")
    lbl_title.pack(fill=X)
    
    ContactForm = Frame(window)
    ContactForm.pack(side=TOP, pady=10)
    
    fields = [("Firstname", FIRSTNAME), ("Lastname", LASTNAME), ("Age", AGE), ("Address", ADDRESS), ("Contact", CONTACT)]
    for i, (text, var) in enumerate(fields):
        row_idx = i if i < 2 else i+1
        Label(ContactForm, text=text, font=('arial', 12)).grid(row=row_idx, column=0, sticky=W, padx=5)
        Entry(ContactForm, textvariable=var, font=('arial', 12)).grid(row=row_idx, column=1, pady=5)

    Label(ContactForm, text="Gender", font=('arial', 12)).grid(row=2, column=0, sticky=W, padx=5)
    RadioGroup = Frame(ContactForm)
    RadioGroup.grid(row=2, column=1, sticky=W)
    Radiobutton(RadioGroup, text="Male", variable=GENDER, value="Male").pack(side=LEFT)
    Radiobutton(RadioGroup, text="Female", variable=GENDER, value="Female").pack(side=LEFT)

    Button(ContactForm, text="Save" if "Add" in title_text else "Update", width=20, bg="#66ff66", command=btn_command).grid(row=7, columnspan=2, pady=20)

def OnSelected(event):
    global mem_id, UpdateWindow
    curItem = tree.focus()
    contents = tree.item(curItem)
    selecteditem = contents['values']
    mem_id = selecteditem[0]
    
    ClearFields()
    FIRSTNAME.set(selecteditem[1])
    LASTNAME.set(selecteditem[2])
    GENDER.set(selecteditem[3])
    AGE.set(selecteditem[4])
    ADDRESS.set(selecteditem[5])
    CONTACT.set(selecteditem[6])
    
    UpdateWindow = Toplevel()
    UpdateWindow.title("Update Contact")
    BuildContactForm(UpdateWindow, "Updating Contact", UpdateData)

def AddNewWindow():
    global NewWindow
    ClearFields()
    NewWindow = Toplevel()
    NewWindow.title("Add New Contact")
    BuildContactForm(NewWindow, "Adding New Contact", SubmitData)

# --- MAIN UI LAYOUT ---
Top = Frame(root, bd=1, relief=SOLID)
Top.pack(side=TOP, fill=X)
Label(Top, text="Contact Management System", font=('arial', 18)).pack()

Mid = Frame(root, bg="#6666ff")
Mid.pack(side=TOP, fill=X, padx=20)
Button(Mid, text="+ ADD NEW", bg="#66ff66", command=AddNewWindow).pack(side=LEFT, pady=10)
Button(Mid, text="DELETE", bg="red", fg="white", command=DeleteData).pack(side=RIGHT, pady=10)

TableMargin = Frame(root)
TableMargin.pack(side=TOP, fill=BOTH, expand=True)

tree = ttk.Treeview(TableMargin, columns=("ID", "First", "Last", "Sex", "Age", "Addr", "Tel"), show='headings')
tree.heading('ID', text="ID")
tree.heading('First', text="Firstname")
tree.heading('Last', text="Lastname")
tree.heading('Sex', text="Gender")
tree.heading('Age', text="Age")
tree.heading('Addr', text="Address")
tree.heading('Tel', text="Contact")

tree.column('ID', width=30)
for col in ["First", "Last", "Sex", "Age", "Addr", "Tel"]:
    tree.column(col, width=100)

tree.pack(side=LEFT, fill=BOTH, expand=True)
tree.bind('<Double-Button-1>', OnSelected)

if __name__ == '__main__':
    Database()
    root.mainloop()