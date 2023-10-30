import sqlite3
import tkinter as tk
from tkinter import messagebox

global listStd
listStd = []

# Function to create the database and student table
def create_database():
    conn = sqlite3.connect("stud.db")
    c = conn.cursor()

    # Create a table if it doesn't exist
    c.execute("CREATE TABLE IF NOT EXISTS students (name TEXT, email TEXT, mobile TEXT)")

    c.execute("SELECT name FROM students")
    rows = c.fetchall()
    for row in rows:
        listStd.append(row[0])

    conn.commit()
    conn.close()

# Function to add a student to the database
def add_student_to_database(name, email, mobile):
    conn = sqlite3.connect("stud.db")
    c = conn.cursor()

    c.execute("INSERT INTO students (name, email, mobile) VALUES (?, ?, ?)", (name, email, mobile))

    conn.commit()
    conn.close()

# Function to remove a student from the database
def remove_student_from_database(name):
    conn = sqlite3.connect("stud.db")
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE name=?", (name,))

    conn.commit()
    conn.close()

# Function to view all students in the database
def view_students():
    conn = sqlite3.connect("stud.db")
    c = conn.cursor()
    c.execute("SELECT name, email, mobile FROM students")
    rows = c.fetchall()
    conn.close()
    return rows

# Function to add a student through the GUI
def add_student_gui():
    new_std = entry_new_student.get()
    email = entry_email.get()
    mobile = entry_mobile.get()

    if new_std and email and mobile:
        if new_std in listStd:
            messagebox.showwarning("Warning", "This student {} already exists in the database.".format(new_std))
        else:
            listStd.append(new_std)
            add_student_to_database(new_std, email, mobile)
            messagebox.showinfo("Success", "New student {} added successfully.".format(new_std))
            entry_new_student.delete(0, tk.END)
            entry_email.delete(0, tk.END)
            entry_mobile.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please enter all fields.")
    refresh_listbox()

# Function to search for a student in the database
def search_student_gui():
    search_option = search_option_var.get()
    search_value = entry_search_value.get()

    if search_value:
        conn = sqlite3.connect("stud.db")
        c = conn.cursor()

        if search_option == 1:
            c.execute("SELECT name, email, mobile FROM students WHERE name=?", (search_value,))
        elif search_option == 2:
            c.execute("SELECT name, email, mobile FROM students WHERE email=?", (search_value,))
        elif search_option == 3:
            c.execute("SELECT name, email, mobile FROM students WHERE mobile=?", (search_value,))
        else:
            messagebox.showwarning("Warning", "Invalid search option.")
            return

        rows = c.fetchall()
        conn.close()

        if rows:
            messagebox.showinfo("Search Results", "Student found:\n\n{}".format(rows))
        else:
            messagebox.showinfo("Search Results", "No matching student found.")
    else:
        messagebox.showerror("Error", "Please enter a search value.")

# Function to delete a student by name
def delete_student_by_name_gui():
    selected_student = entry_delete_student.get()
    if selected_student:
        if selected_student in listStd:
            confirmed = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this student?")
            if confirmed:
                listStd.remove(selected_student)
                remove_student_from_database(selected_student)
                messagebox.showinfo("Success", "Student {} successfully deleted.".format(selected_student))
                refresh_listbox()
        else:
            messagebox.showwarning("Warning", "This student {} does not exist in the database.".format(selected_student))
    else:
        messagebox.showerror("Error", "Please enter a student name to delete.")

# Function to refresh the listbox with student names
def refresh_listbox():
    listbox_students.delete(0, tk.END)
    students = view_students()
    for student in students:
        listbox_students.insert(tk.END, student[0])

# Create the main window
window = tk.Tk()
window.title("Student Management System")
window.configure(bg="#C4DFDF")
window.geometry("900x800")

# Create a frame for student entry
frame_entry = tk.Frame(window)
frame_entry.configure(bg="#C4DFDF")
frame_entry.grid(row=0, column=0, padx=150, pady=5)

# Create labels and entry fields for student information
label_new_student = tk.Label(frame_entry, text="New Student:", bg="#C4DFDF", fg="#643843", font=("Georgia", 14))
label_new_student.grid(row=0, column=0, padx=5, pady=5)
entry_new_student = tk.Entry(frame_entry, width=45, font=("Georgia", 12))
entry_new_student.grid(row=0, column=1, padx=5, pady=5)

label_email = tk.Label(frame_entry, text="Email:", bg="#C4DFDF", fg="#643843", font=("Georgia", 14))
label_email.grid(row=1, column=0, padx=5, pady=5)
entry_email = tk.Entry(frame_entry, width=45, font=("Georgia", 12))
entry_email.grid(row=1, column=1, padx=5, pady=5)

label_mobile = tk.Label(frame_entry, text="Mobile:", bg="#C4DFDF", fg="#643843", font=("Georgia", 14))
label_mobile.grid(row=2, column=0, padx=5, pady=5)
entry_mobile = tk.Entry(frame_entry, width=45, font=("Georgia", 12))
entry_mobile.grid(row=2, column=1, padx=5, pady=5)

# Create a button to add the student
button_add_student = tk.Button(frame_entry, text="Add Student", command=add_student_gui, fg="#643843", bg="#E3F4F4", font=("Georgia", 14))
button_add_student.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Create a frame for search
frame_search = tk.Frame(window)
frame_search.configure(bg="#C4DFDF")
frame_search.grid(row=1, column=0, padx=5, pady=30)

# Create a label and entry field for search value
label_search_value = tk.Label(frame_search, text="Search Value:", bg="#C4DFDF", fg="#643843", font=("Georgia", 14))
label_search_value.grid(row=0, column=0, padx=5, pady=5)
entry_search_value = tk.Entry(frame_search, font=("Georgia", 12))
entry_search_value.grid(row=0, column=1, padx=5, pady=5)

# Create a label and radio buttons for search options
label_search_option = tk.Label(frame_search, text="Search Option:", bg="#C4DFDF", fg="#643843", font=("Georgia", 14))
label_search_option.grid(row=1, column=0, padx=5, pady=5)

search_option_var = tk.IntVar()
radio_name = tk.Radiobutton(frame_search, text="Name", variable=search_option_var, value=1, bg="#C4DFDF", fg="#643843", font=("Georgia", 14))
radio_name.grid(row=1, column=1, padx=5, pady=5)
radio_email = tk.Radiobutton(frame_search, text="Email", variable=search_option_var, value=2, bg="#C4DFDF", fg="#643843", font=("Georgia", 14))
radio_email.grid(row=1, column=2, padx=5, pady=5)
radio_mobile = tk.Radiobutton(frame_search, text="Mobile", variable=search_option_var, value=3, bg="#C4DFDF", fg="#643843", font=("Georgia", 14))
radio_mobile.grid(row=1, column=3, padx=5, pady=5)

# Create a button to search for students
button_search = tk.Button(frame_search, text="Search", command=search_student_gui, bg="#E3F4F4", fg="#643843", font=("Georgia", 14))
button_search.grid(row=2, column=0, columnspan=4, padx=5, pady=5)

# Create a frame for the listbox
frame_listbox = tk.Frame(window, width=45)
frame_listbox.grid(row=2, column=0, padx=5, pady=5)
frame_listbox.configure(bg="white")

# Create a listbox to display the students
listbox_students = tk.Listbox(frame_listbox, width=45, font=("Georgia", 14))
listbox_students.grid(row=0, column=0, padx=5, pady=5)

# Create a frame for deleting students
frame_delete = tk.Frame(window)
frame_delete.grid(row=3, column=0, padx=5, pady=5)
frame_delete.configure(bg="#C4DFDF")

# Create a label and entry field for delete student
label_delete_student = tk.Label(frame_delete, text="Delete Student:", bg="#C4DFDF", fg="#643843", font=("Georgia", 14))
label_delete_student.grid(row=0, column=0, padx=5, pady=5)
entry_delete_student = tk.Entry(frame_delete, width=45, font=("Georgia", 12))
entry_delete_student.grid(row=0, column=1, padx=5, pady=5)

# Create a button to delete a student by name
button_delete_student = tk.Button(frame_delete, text="Delete Student", command=delete_student_by_name_gui, bg="#E3F4F4", fg="#643843", font=("Georgia", 14))
button_delete_student.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# Initialize the database and populate the listbox
create_database()
refresh_listbox()

window.mainloop()
