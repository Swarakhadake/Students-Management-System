import tkinter as tk
from tkinter import messagebox
import sqlite3

# ---------------- DATABASE ----------------
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    course TEXT
)
""")
conn.commit()

# -------- GLOBAL VARIABLE --------
selected_id = None

# ---------------- FUNCTIONS ----------------

def add_student():
    name = entry_name.get()
    age = entry_age.get()
    course = entry_course.get()

    if name == "" or age == "" or course == "":
        messagebox.showerror("Error", "All fields required")
        return

    cursor.execute("INSERT INTO students(name, age, course) VALUES (?, ?, ?)",
                   (name, age, course))
    conn.commit()
    messagebox.showinfo("Success", "Student Added")
    clear_fields()
    show_students()

def show_students():
    listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    for row in rows:
        listbox.insert(tk.END, row)

def update_student():
    global selected_id

    if selected_id is None:
        messagebox.showerror("Error", "No student selected")
        return

    cursor.execute("UPDATE students SET name=?, age=?, course=? WHERE id=?",
                   (entry_name.get(), entry_age.get(), entry_course.get(), selected_id))
    conn.commit()

    messagebox.showinfo("Success", "Student Updated")
    show_students()
    clear_fields()

def delete_student():
    global selected_id

    if selected_id is None:
        messagebox.showerror("Error", "No student selected")
        return

    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete?")
    if confirm:
        cursor.execute("DELETE FROM students WHERE id=?", (selected_id,))
        conn.commit()
        show_students()
        clear_fields()

def select_student(event):
    global selected_id

    if not listbox.curselection():
        return

    selected = listbox.get(listbox.curselection())
    selected_id = selected[0]

    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_course.delete(0, tk.END)

    entry_name.insert(tk.END, selected[1])
    entry_age.insert(tk.END, selected[2])
    entry_course.insert(tk.END, selected[3])

def search_student():
    keyword = entry_name.get()
    listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + keyword + '%',))
    rows = cursor.fetchall()
    for row in rows:
        listbox.insert(tk.END, row)

def clear_fields():
    global selected_id
    selected_id = None

    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_course.delete(0, tk.END)

# ----------- ENTER KEY FUNCTIONS -----------

def focus_age(event):
    entry_age.focus()

def focus_course(event):
    entry_course.focus()

def submit_on_enter(event):
    if selected_id:
        update_student()
    else:
        add_student()

# ---------------- GUI ----------------

root = tk.Tk()
root.title("🎓 Student Manager")
root.geometry("650x500")
root.configure(bg="#2C3E50")

# Title
title = tk.Label(root, text="Student Management System",
                 font=("Arial", 20, "bold"),
                 bg="#2C3E50", fg="#ECF0F1")
title.pack(pady=10)

# Frame for inputs
frame = tk.Frame(root, bg="#34495E", bd=3, relief=tk.RIDGE)
frame.pack(pady=10, padx=10, fill="x")

# Labels & Entries
tk.Label(frame, text="Name", bg="#34495E", fg="white").grid(row=0, column=0, padx=10, pady=10)
entry_name = tk.Entry(frame, font=("Arial", 12), bg="#ECF0F1")
entry_name.grid(row=0, column=1, padx=10)

tk.Label(frame, text="Age", bg="#34495E", fg="white").grid(row=1, column=0, padx=10, pady=10)
entry_age = tk.Entry(frame, font=("Arial", 12), bg="#ECF0F1")
entry_age.grid(row=1, column=1, padx=10)

tk.Label(frame, text="Course", bg="#34495E", fg="white").grid(row=2, column=0, padx=10, pady=10)
entry_course = tk.Entry(frame, font=("Arial", 12), bg="#ECF0F1")
entry_course.grid(row=2, column=1, padx=10)

# -------- ENTER KEY BINDINGS --------
entry_name.bind("<Return>", focus_age)
entry_age.bind("<Return>", focus_course)
entry_course.bind("<Return>", submit_on_enter)

# Buttons Frame
btn_frame = tk.Frame(root, bg="#2C3E50")
btn_frame.pack(pady=10)

def styled_button(text, command, color):
    return tk.Button(btn_frame, text=text, command=command,
                     font=("Arial", 11, "bold"),
                     bg=color, fg="white",
                     width=12, bd=0)

styled_button("Add", add_student, "#27AE60").grid(row=0, column=0, padx=5, pady=5)
styled_button("Update", update_student, "#2980B9").grid(row=0, column=1, padx=5, pady=5)
styled_button("Search", search_student, "#8E44AD").grid(row=0, column=2, padx=5, pady=5)
styled_button("Clear", clear_fields, "#7F8C8D").grid(row=0, column=3, padx=5, pady=5)
styled_button("Delete", delete_student, "#C0392B").grid(row=0, column=4, padx=5, pady=5)

# Listbox
listbox = tk.Listbox(root, font=("Courier", 11),
                     bg="#ECF0F1", fg="#2C3E50",
                     width=70, height=12)
listbox.pack(pady=15)

listbox.bind("<<ListboxSelect>>", select_student)

# Load data
show_students()

# Start focus
entry_name.focus()

root.mainloop()